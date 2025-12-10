# Use Python slim image - no browser needed, we'll use Selenium Grid
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test files
COPY . .

# Default command (can be overridden)
CMD ["pytest", "-v", "--html=report.html", "--self-contained-html", "tests/"]
