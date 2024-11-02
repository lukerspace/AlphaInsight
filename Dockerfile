# Base image with Python 3.12
FROM python:3.12

# Expose port 3000 for the application
EXPOSE 3000

# Install basic utilities and Chrome dependencies
RUN apt-get update && \
    apt-get install -y wget unzip curl nano cron && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install pip requirements
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]
