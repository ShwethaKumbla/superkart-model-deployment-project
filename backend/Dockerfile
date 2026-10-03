FROM python:3.12-slim

WORKDIR /app

# Copy and install dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and model file
COPY . .

# Expose the port Flask listens on
EXPOSE 7860

# Start the Flask application
CMD ["python", "app.py"]
