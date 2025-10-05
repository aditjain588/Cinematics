# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# Expose Flask port
EXPOSE 5000

# Run backend
CMD ["python", "run.py"]
