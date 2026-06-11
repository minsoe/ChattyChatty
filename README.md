# ChattyChatty

ChattyChatty is a backend application written in Python, utilizing FastAPI and MongoDB. It provides a conversational AI service and can be run locally using Docker or a Python virtual environment with `uv`.

## Table of Contents
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
  - [Using Docker](#using-docker)
  - [Without Docker](#without-docker)
- [Running Tests](#running-tests)
- [Environment Variables](#environment-variables)
- [Project Folder Structure](#project-folder-structure)

## Getting Started

### Prerequisites
- Docker (for running with Docker or spinning up MongoDB)
- Python 3.11+
- `uv` (for Python package management)
- `just` (command runner, optional but recommended)

## Running the Application

### Using Docker
1. Clone the repository:
    ```sh
    git clone https://github.com/minsoe/ChattyChatty.git
    cd ChattyChatty
    ```

2. Create a `.env` file in the root directory (or in `chatty_services/`) and add the following environment variables:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    MONGODB_URL=mongodb://mongo:27017
    ```

3. Run the application using Docker Compose:
    ```sh
    docker-compose -f chatty_services/docker-compose.yml up --build
    ```

### Without Docker
1. Clone the repository:
    ```sh
    git clone https://github.com/minsoe/ChattyChatty.git
    cd ChattyChatty
    ```

2. Install dependencies for all projects in the workspace:
    ```sh
    just sync
    ```
    *(Alternatively, run `uv sync --project <project-dir>` for each directory as defined in the `Justfile`)*

3. Create a `.env` file in the root directory and add the following environment variables:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    MONGODB_URL=mongodb://localhost:27017
    ```

4. Spin up the MongoDB container locally:
    ```sh
    docker compose -f chatty_services/docker-compose.mongo.yml up -d
    ```

5. Run the FastAPI application in development mode:
    ```sh
    uv run --project chatty_services fastapi dev chatty_services/src/chatty_api/main.py
    ```

## Running Tests
You can run all the tests across the workspace using:
```sh
just test
```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key.
- `MONGODB_URL`: The connection URL for your MongoDB server.

## Project Folder Structure

```
├── pyproject.toml
├── README.md
├── Justfile
├── chatty_services/
│   ├── pyproject.toml
│   ├── docker-compose.yml
│   ├── docker-compose.mongo.yml
│   ├── src/
│   │   └── chatty_api/
│   │       ├── main.py
│   │       ├── IOC/
│   │       ├── bootstrap/
│   │       ├── conversation_services/
│   │       └── pyproject.toml
│   └── tests/
└── packages/
    ├── chatty_ai/
    │   ├── pyproject.toml
    │   ├── src/
    │   │   └── chatty_ai/
    │   │       ├── ai_service.py
    │   │       └── openai_service.py
    │   └── tests/
    ├── chatty_core/
    │   ├── pyproject.toml
    │   ├── src/
    │   │   └── chatty_core/
    │   │       ├── models/
    │   │       ├── database/
    │   │       └── conversations/
    │   └── tests/
    └── chatty_test_services/
        ├── pyproject.toml
        ├── src/
        │   └── chatty_test_services/
        │       └── mocks/
        └── tests/
```