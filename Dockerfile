# Base image for building the application
FROM python:3.12.0-slim-bullseye as base

# Install system dependencies and remove cache to reduce image size
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Set the working directory
WORKDIR /app/src

# Copy only the dependency files first to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install production dependencies
RUN poetry install --only main

# Remove development tools to reduce image size
RUN apt-get purge -y gcc && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . .

# Install remaining dependencies (if any)
RUN poetry install --only main

# Set the command to run the application
CMD ["/usr/local/bin/python", "-m", "owow_backend"]

# Development stage
FROM base as dev

# Install all dependencies including development dependencies
RUN poetry install

# Expose the application port (if required)
EXPOSE 8000

# Set the command for the development environment
CMD ["/usr/local/bin/python", "-m", "owow_backend"]
