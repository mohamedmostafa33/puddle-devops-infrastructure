# Use the official Python 3.12 slim image as the base image
FROM python:3.12-slim

# Set environment variables to improve performance and prevent bytecode files
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1        

# Install build dependencies and PostgreSQL libraries for working with Postgres databases
RUN apt-get update && apt-get install -y \
    build-essential \          
    gcc \                      
    libpq-dev \                   
    && rm -rf /var/lib/apt/lists/* 

# Create a new user and group for running the application (to avoid running as root)
RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Change the ownership of the app files to the appuser (non-root user)
RUN chown -R appuser:appgroup /app

# Switch to the non-root user for security reasons
USER appuser

# Expose port 8000 for the application to be accessible
EXPOSE 8000

# Set the command to run Gunicorn with the Django app as the entry point
CMD ["gunicorn", "puddle.wsgi:application", "--bind", "0.0.0.0:8000"]
