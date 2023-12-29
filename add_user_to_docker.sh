#!/bin/bash

sudo apt update
sudo apt  install docker.io
sudo usermod -aG docker $USER

# Restart the system
sudo reboot

