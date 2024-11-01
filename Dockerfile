# Base image with Python 3.12
FROM python:3.12

# Expose port 3000 for the application
EXPOSE 3000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set environment variables to avoid issues with root user in Chrome
ENV DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99

# Install basic utilities and Chrome dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    tar \
    xvfb \
    alsa-utils \
    libatk1.0-0 \
    libcups2 \
    libgtk-3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxi6 \
    libxtst6 \
    libpangocairo-1.0-0 \
    libxss1 \
    xdg-utils \
    libgbm-dev \
    fonts-liberation \
    libappindicator3-1 \
    lsb-release \
    libnss3 \
    libasound2 \
    libdrm2 \
    libxrandr2 \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome or Chromium depending on architecture
RUN set -eux; \
    ARCH=$(uname -m); \
    if [ "$ARCH" = "x86_64" ]; then \
        wget -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; \
        apt-get update; \
        apt-get install -y /tmp/google-chrome.deb; \
        rm /tmp/google-chrome.deb; \
    elif [ "$ARCH" = "aarch64" ]; then \
        # Find the latest build number
        BUILD_NUMBER=$(curl -s https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_ARM64/LAST_CHANGE); \
        # Download Chromium ARM64 build
        wget -O /tmp/chromium.zip https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_ARM64/${BUILD_NUMBER}/chrome-linux.zip; \
        unzip /tmp/chromium.zip -d /opt/; \
        mv /opt/chrome-linux /opt/chromium; \
        ln -s /opt/chromium/chrome /usr/bin/chromium; \
        rm /tmp/chromium.zip; \
    else \
        echo "Unsupported architecture: $ARCH"; \
        exit 1; \
    fi

# Install ChromeDriver matching the browser version and architecture
RUN set -eux; \
    ARCH=$(uname -m); \
    if [ "$ARCH" = "x86_64" ]; then \
        ARCH_DL="linux64"; \
        CHROME_VERSION=$(google-chrome --version | awk '{print $3}'); \
    elif [ "$ARCH" = "aarch64" ]; then \
        ARCH_DL="linux-arm64"; \
        CHROME_VERSION=$(chromium --version | awk '{print $2}'); \
    else \
        echo "Unsupported architecture: $ARCH"; \
        exit 1; \
    fi; \
    CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d '.' -f 1); \
    # Handle Chromium version formatting
    if [ "$ARCH" = "aarch64" ]; then \
        CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d '.' -f 1 | cut -d '-' -f 1); \
    fi; \
    CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}); \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_${ARCH_DL}.zip"; \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/; \
    rm /tmp/chromedriver.zip; \
    chmod +x /usr/local/bin/chromedriver

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install pip requirements
RUN pip install --no-cache-dir -r requirements.txt

# Creates a non-root user and sets permissions for the /app folder
RUN adduser --uid 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]
