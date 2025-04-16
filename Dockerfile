FROM python:3.10-slim

# Set working directory
WORKDIR /app
# Add PYTHONPATH for clean imports
ENV PYTHONPATH=/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Expose the redirect URI port
EXPOSE 8888

# Command to run CLI
CMD ["python", "-u", "app/interfaces/cli/main.py"]