#!/bin/bash
cd /home/ubuntu/ticketing-system
git pull origin main
docker stop ticketing_app || true
docker rm ticketing_app || true
docker build -t ticketing-system:latest .
docker run -d --name ticketing_app -p 127.0.0.1:5000:5000 ticketing-system:latest
sudo nginx -t
sudo systemctl reload nginx