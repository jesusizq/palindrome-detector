# Palindrome Detector

## Overview

Design and develop a service that allows us to detect palindromes.

It is exposed using a REST API with JSON that allows us to:

- Detect if a random string is a palindrome from a language field and a text field.
- List all the detections on the system, allowing filters by date and language.
- Get the results of one palindrome detection.
- Remove a detection.

## Dependencies

### System Prerequisites

Before you begin, ensure you have the following system-level tools installed:

- **Docker Engine:** Required for building and running the application containers. Follow the official installation guide for your operating system: [Install Docker Engine](https://docs.docker.com/engine/install/)
- **Docker Compose:** Used to manage the multi-container application environment (app, db, redis, nginx, etc.). It's typically included with Docker Desktop but might require a separate installation otherwise. See: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **A POSIX-compliant shell (sh):** Required for running scripts (like `docker/run.sh`) or `Makefile` commands.

### Python Project Dependencies (Poetry)

Install project dependencies using `poetry` (version >=1.5.0 recommended). If you don't have Poetry, it needs to be [installed](https://python-poetry.org/docs/#installing-with-the-official-installer) first.

Depending on your IDE, you may need to configure the python interpreter to use the poetry environment (i.e. [PyCharm](https://www.jetbrains.com/help/pycharm/poetry.html))

Use the Makefile to install dependencies:

```sh
make install
```

Activate `poetry environment` (if not using `make run` or other `make` targets that handle it):

```sh
poetry shell
```

## Architectural Summary

The system is a microservice with a layered architecture:

- **API Layer**: Flask & APIFairy for handling HTTP requests and validation.
- **Service Layer**: Core business logic.
- **Data Access Layer**: SQLAlchemy ORM for PostgreSQL database interactions.
- **Cache Layer**: Redis for caching.
- **Nginx**: Acts as a reverse proxy in the Docker setup, handling incoming traffic. It can also be configured for SSL termination, basic load balancing (if scaled), and serving static files if needed.

This modular design supports independent development, testing, and scaling. 


## Makefile

A `Makefile` is provided in the project root to simplify common development and operational tasks. It serves as a convenient entry point for commands related to dependency management, running the application, executing tests, and managing Docker containers.

## Environment variables

The application requires the following environment variables, typically managed via a `.env` file in the project root. Take a look at the [.env.example](.env.example) file for reference.

**Important Notes**

- **Localhost Configuration**: When working against localhost, ensure to update the service names in the `.env` file to `localhost`. For example, change `postgresql://user:password@db:5432/event_integrator` to `postgresql://user:password@localhost:5432/event_integrator`.
- **Version Control**: **Do not commit** the `.env` file to version control.

## Database Migrations

This project uses Flask-Migrate (which relies on Alembic) to manage database schema changes.

### Initial Setup (One-Time Only)

Before you can create or apply migrations for the first time, you need to initialize the migration environment. This creates a `migrations` directory in your project root that will store all migration scripts and configurations.

1.  **Ensure the `migrations` directory exists with correct permissions:**
    This step is crucial to avoid permission errors when Docker tries to write to this directory from within the container. From your project root:

    ```bash
    mkdir -p migrations
    sudo chown -R $(id -u):$(id -g) migrations
    ```

2.  **Initialize the Flask-Migrate environment:**
    From the project root again, run this command to initialize the migration environment with:

    ```bash
    make init-migrations
    ```

    This command will populate the `./migrations` directory on your host with essential migration files.

    You should commit the initially generated `migrations` directory and all its contents. For this project, **commit all generated migration scripts in `migrations/versions/`**.

Once these steps are completed and committed, you can use the Makefile targets like `make create-migration` and `make migrate` to manage your database schema changes.

### Creating New Migrations

Whenever you make changes to your SQLAlchemy models (defined in `app/models/*.py`), you must generate a new migration script to reflect these changes.

**Generate the migration script:**

Use the provided Makefile command:

```bash
    make create-migration message="<message>"
```

Replace `<message>` with a short, clear summary of the schema changes you made, and you will see the migration script generated in `migrations/versions/`.

### Applying Migrations

Applying migrations to execute the generated scripts to update your database schema to the desired state.

1.  **Automatically on `docker compose up` (via `make up`):**
    The `migrations` service defined in `docker/docker-compose.yml` is configured to automatically run `flask db upgrade` every time your services are started.

2.  **Manually using Makefile:**
    If you need to apply migrations manually (e.g., after pulling new changes from Git that include new migration scripts, without restarting all services), you can use:

    ```bash
    make migrate
    ```

## Running the app

Ensure environment variables are set or available in a `.env` file.

Using Makefile with Docker Compose is recommended. This method uses the [docker/docker-compose.yml](docker/docker-compose.yml) file which runs the Flask app along with an Nginx proxy, PostgreSQL database, and Redis.

Ensure your `.env` file is in the project root, as `docker-compose.yml` depends on it.

Build and start the containers in detached mode with:

```sh
source .env && make build && make up
```

The app will be available via Nginx at `http://localhost:8080`


## Running Tests

Ensure development dependencies are installed (this is handled by `make install` if you haven't run it yet, or it's included if you've run `make up`).

Configure a `TEST_DATABASE_URL` in your environment or `.env` file, so tests automatically run against that database.

To run tests:

```sh
source .env.test && poetry run pytest
```

or, using the Makefile against the dockerized test environment:

```sh
source .env.test && make build test_env=true && make test
```

**IMPORTANT**: ensure you have sourced your test environment variables first with `source .env.test`. That command relies on `docker/run.sh`, which depends on `--env-file=.env.test` for the test environment to work. That file is hardcoded in the run.sh script.
