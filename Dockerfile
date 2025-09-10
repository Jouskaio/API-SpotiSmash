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

# Command to run CLI
# TODO : Remove --reload for production
CMD ["uvicorn", "app.interfaces.api.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
#CMD ["python", "-u", "app/interfaces/cli/main.py"]