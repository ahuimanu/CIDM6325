# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app


# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev curl netcat-openbsd gcc

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .
# Set environment to production for Django static files
ENV DJANGO_ENV=production


# Port exposed for Gunicorn
EXPOSE 8000

# Gunicorn entrypoint
CMD ["gunicorn", "logistics_project.wsgi:application", "--bind", "0.0.0.0:8000"]
