# Deploy to EC2

Overview: This project runs as a FastAPI app using `uvicorn`. The repo includes a convenience script to provision and run the service on an Ubuntu EC2 instance.

Notes: Installing all Python dependencies (especially `torch`, `transformers`, and large NLP packages) can take a long time and may require a GPU-enabled AMI if you want GPU support. The provided script attempts a CPU install; consider using an appropriate AWS Deep Learning AMI for GPU workloads.

Quick deploy (recommended flow)

1. Provision an Ubuntu EC2 instance (20GB+ disk, t3.medium or larger). SSH as `ubuntu` user.
2. On the EC2 instance, run the setup script (replace `<repo>` and `<app_dir>`):

```bash
# Run on the EC2 instance (example):
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/<your-user>/<your-repo>/main/deploy/setup_ec2.sh)" \
  https://github.com/<your-user>/<your-repo>.git /home/ubuntu/pitch-deck-analyzer main

# OR copy the repository to the instance and run locally on the instance:
# ssh ubuntu@ec2-ip
# sudo ./deploy/setup_ec2.sh https://github.com/<your-user>/<your-repo>.git /home/ubuntu/pitch-deck-analyzer main
```

The script will:
  - install system packages
  - clone/pull the repo into the provided path
  - create a Python virtualenv and install `requirements.txt`
  - create a `systemd` unit and start the service

Check service status:

```bash
sudo systemctl status pitch-deck-analyzer.service
sudo journalctl -u pitch-deck-analyzer.service -f
```

Manual steps (if you prefer)

1. SSH to the EC2 instance and update packages:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git build-essential poppler-utils
```

2. Clone the repo and create venv:
```bash
git clone https://github.com/<your-user>/<your-repo>.git /home/ubuntu/pitch-deck-analyzer
cd /home/ubuntu/pitch-deck-analyzer
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. (Optional) If `torch` installation fails due to CUDA mismatch, either install a CPU-only wheel or use an AWS Deep Learning AMI.

4. Create the systemd unit (example):
```bash
sudo cp deploy/pitch-deck-analyzer.service /etc/systemd/system/
# Edit /etc/systemd/system/pitch-deck-analyzer.service to update paths if needed
sudo systemctl daemon-reload
sudo systemctl enable pitch-deck-analyzer.service
sudo systemctl start pitch-deck-analyzer.service
```

If anything fails during `pip install`, check the logs and install problematic packages individually (GPU drivers, CUDA, or CPU-only wheels for `torch`).
