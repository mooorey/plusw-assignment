#!/bin/bash

sudo apt update
sudo apt install python3-pip
pip install django
pip install openai
pip install python-dotenv
pip install typer
pip install openai==0.28
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000

