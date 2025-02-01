# Use official Python image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gettext \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Run migrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "backend.wsgi:application"]