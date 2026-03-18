# Deploy to EC2

Overview: This project runs as a FastAPI app using `uvicorn`. The repo includes a convenience script to provision and run the service on an Amazon Linux EC2 instance.

Notes: Installing all Python dependencies (especially `torch`, `transformers`, and large NLP packages) can take a long time and may require a GPU-enabled AMI if you want GPU support. The provided script attempts a CPU install; consider using an appropriate AWS Deep Learning AMI for GPU workloads.

Quick deploy (recommended flow)

1. Provision an Amazon Linux EC2 instance (20GB+ disk, t3.medium or larger). SSH as `ec2-user`.
2. On the EC2 instance, run the setup script (replace `<repo>` and `<app_dir>`):

```bash
# Run on the EC2 instance (example):
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/<your-user>/<your-repo>/main/deploy/setup_ec2.sh)" \
  https://github.com/<your-user>/<your-repo>.git /home/ec2-user/pitch-deck-analyzer main

# OR copy the repository to the instance and run locally on the instance:
# ssh ec2-user@ec2-ip
# sudo ./deploy/setup_ec2.sh https://github.com/<your-user>/<your-repo>.git /home/ec2-user/pitch-deck-analyzer main
```

The script will:
  - install system packages
  - clone/pull the repo into the provided path
  - create a Python virtualenv and install `requirements.txt`
  - run `train.py` to generate the model artifacts required by the API
  - create a `systemd` unit and start the service

Check service status:

```bash
sudo systemctl status pitch-deck-analyzer.service
sudo journalctl -u pitch-deck-analyzer.service -f
```

Manual steps (if you prefer)

1. SSH to the EC2 instance and update packages:
```bash
sudo dnf update -y
sudo dnf install -y python3 python3-pip git gcc gcc-c++ make openssl-devel libffi-devel libxml2-devel libxslt-devel zlib-devel libjpeg-turbo-devel poppler-utils
```

2. Clone the repo and create venv:
```bash
git clone https://github.com/<your-user>/<your-repo>.git /home/ec2-user/pitch-deck-analyzer
cd /home/ec2-user/pitch-deck-analyzer
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. Train the models before starting the API:
```bash
python train.py
```

4. Create the systemd unit (example):
```bash
sudo cp deploy/pitch-deck-analyzer.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pitch-deck-analyzer.service
sudo systemctl start pitch-deck-analyzer.service
```

If anything fails during `pip install`, check the logs and install problematic packages individually. If `torch` GPU support is needed later, use an AWS Deep Learning AMI or install matching CUDA packages separately.
