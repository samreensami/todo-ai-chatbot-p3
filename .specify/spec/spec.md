# Project Specification

## Framework

The project will use the **FastAPI** framework for building the API.

## Rationale

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Key Features of FastAPI to be Leveraged:

- **Automatic interactive API documentation:** (via Swagger UI and ReDoc)
- **Validation:** Data validation using Pydantic models.
- **Dependency Injection:** FastAPI's dependency injection system will be used to manage dependencies.
- **Asynchronous support:** Endpoints will be asynchronous where appropriate to handle I/O-bound operations efficiently.

## CLI Application

### Functional Requirements

- **CLI-001**: The system MUST provide a command-line interface (CLI) application named `cli_app.py`.
- **CLI-002**: The `cli_app.py` MUST offer a single interactive terminal menu.
- **CLI-003**: From the terminal menu, users MUST be able to add new tasks.
- **CLI-004**: From the terminal menu, users MUST be able to view existing tasks.
- **CLI-005**: From the terminal menu, users MUST be able to delete tasks.
