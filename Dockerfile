FROM python:3.11-slim

# Install system dependencies including Firefox and GeckoDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Install GeckoDriver (Firefox WebDriver)
RUN GECKODRIVER_VERSION=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d '"' -f 4) && \
    wget -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test files
COPY . .

# Run tests with HTML report generation
CMD ["pytest", "-v", "--html=report.html", "--self-contained-html", "tests/"]
