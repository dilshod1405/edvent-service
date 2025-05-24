# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (Daphne needs it sometimes)
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Copy project files
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . /app
COPY ./config /app/config


# Expose port
EXPOSE 8000

# Start Daphne server (Channels needs this)
CMD ["gunicorn", "-b", "0.0.0.0", "-p", "8000", "config.wsgi:application"]
