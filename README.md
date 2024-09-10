# OWOW Backend

A Python backend service that leverages Predibase to extract and summarize key points from PDF, PPT, and DOCX files.
Seamlessly integrates with your application to provide concise, actionable insights from document contents.

# Run with UV

- Install uv
```bash
curl -sSf https://rye.astral.sh/get | bash
```
- Sync Packages
```bash
rye sync
```
- Run the project
```bash
rye run python -m owow_backend
```

## Docker

You can start the project with docker using this command:

```bash
docker-compose up --build
```

If you want to develop in docker with autoreload and exposed ports add `-f deploy/docker-compose.dev.yml` to your docker
command.
Like this:

```bash
docker-compose -f docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

```bash
docker-compose build
```

## Project structure

```bash
$ tree "owow_backend"
1
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifespan.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

An example of .env file:

```bash
RELOAD="True"
PORT="8000"
ENVIRONMENT="dev"
```

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default, it runs:

* black (formats your code);
* mypy (validates types);
* ruff (spots possible bugs);

You can read more about pre-commit here: https://pre-commit.com/

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose run --build --rm api pytest -vv .
docker-compose down
```

1. Run the pytest.

```bash
pytest -vv .
```
