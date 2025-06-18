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

Install dependencies:

```sh
poetry install
```

Activate `poetry environment` (if not using `make run` or other `make` targets that handle it):

```sh
poetry shell
```
