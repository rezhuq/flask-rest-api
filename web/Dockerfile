# Pull image from Docker Hub
FROM python:3

# Maintainer
MAINTAINER Rezwanul Huq

# Set PYTHONUNBUFFERED so output is displayed in the Docker log instantly without buffering them
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

# Copy all files to working directory
COPY . .

# Run app.py
CMD ["python", "app.py"]