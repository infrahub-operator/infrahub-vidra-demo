# Use an official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY ./webserver /app/webserver
COPY ./python_scripts /app/python_scripts

# Ensure the app root is in the Python path
ENV PYTHONPATH=/app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy only the poetry files to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Expose the Flask port
EXPOSE 5000

# Run the Flask application
CMD ["python3", "webserver/webserver.py"]
