#!/usr/bin/env bash
set -euo pipefail

# Usage:
# sudo ./setup_ec2.sh <git_repo_url> <app_dir> [branch]
# Example: sudo ./setup_ec2.sh https://github.com/you/repo.git /home/ubuntu/pitch-deck-analyzer main

REPO_URL="$1"
APP_DIR="$2"
BRANCH="${3:-main}"
APP_USER="ubuntu"

echo "Updating apt and installing packages..."
apt-get update -y
apt-get install -y python3 python3-venv python3-pip git build-essential libssl-dev libffi-dev \
    poppler-utils libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev

echo "Cloning repository..."
if [ ! -d "$APP_DIR" ]; then
    git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
else
    echo "Directory $APP_DIR exists — pulling latest"
    cd "$APP_DIR"
    git fetch --all
    git checkout "$BRANCH"
    git pull origin "$BRANCH"
fi

chown -R "$APP_USER":"$APP_USER" "$APP_DIR"

echo "Creating Python virtualenv..."
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel setuptools

echo "Installing Python dependencies (this may take a while)..."
if [ -f requirements.txt ]; then
    pip install --no-cache-dir -r requirements.txt || true
else
    echo "requirements.txt not found in $APP_DIR"
fi

echo "Creating systemd service file (you may need to edit paths in the unit file)..."
SERVICE_NAME="pitch-deck-analyzer.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"
cat > "$SERVICE_PATH" <<EOF
[Unit]
Description=Pitch Deck Analyzer API
After=network.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/api_server.py
Restart=on-failure
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

echo "Reloading systemd, enabling and starting service..."
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

echo "Deployment finished. Check service status with: systemctl status $SERVICE_NAME"
