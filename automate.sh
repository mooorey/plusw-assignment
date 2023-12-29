#!/bin/bash

sudo apt  install docker.io


# Define the Dockerfile content
DOCKERFILE_CONTENT=$(cat <<-EOF
# Use an official Python runtime as a base image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update and install system packages
RUN apt-get update && apt-get install -y \
    # Add any additional system packages you may need here

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install django openai python-dotenv typer==0.4.0 openai==0.28 click==7.1.2

# Run Django migrations
RUN python manage.py migrate

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
EOF
)

# Save Dockerfile content to a file
echo "$DOCKERFILE_CONTENT" > Dockerfile

# Build Docker image
sudo docker build -t my-django-app .

# Run Docker container
docker run -p 8001:8001 my-django-app

