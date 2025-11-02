# ChattyChatty

ChattyChatty is a backend application written in Python, utilizing FastAPI and MongoDB. It provides a conversational AI service and can be run locally using Docker or a Python virtual environment.

## Table of Contents
- Getting Started
- Running the Application
  - Using Docker
  - Without Docker
- Environment Variables
- Dependencies

## Getting Started

### Prerequisites
- Docker (for running with Docker)
- Python 3.8+ (for running without Docker)
- MongoDB server

## Running the Application

### Using Docker
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ChattyChatty.git
    cd ChattyChatty
    ```

2. Create a `.env` file in the root directory and add the following environment variables:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    MONGODB_URL=your_mongodb_url
    ```

3. Run the application using Docker Compose:
    ```sh
    docker-compose up --build
    ```

### Without Docker
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ChattyChatty.git
    cd ChattyChatty
    ```

2. Create a Python virtual environment & install dependencies:
    ```sh
    pip install uv
    uv sync
    source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dev dependencies:
    ```sh
    uv sync --extra dev
    ```

5. Create a `.env` file in the root directory and add the following environment variables:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    MONGODB_URL=your_mongodb_url
    ```

6. Run the application:
    ```sh
    docker compose -f docker-compose.mongo.yml up -d #to spin up mongodb locally
    fastapi dev chatty_api.main:app
    ```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key.
- `MONGODB_URL`: The URL for your MongoDB server.

## Project folder structure 
├── pyproject.toml
├── README.md
├── chatty_api/
│ ├── pyproject.toml
│ ├── src/
│ │ ├── chatty_api/
│ │ ├── bootstrap/
│ │ ├── api_services/
│ │ │ └── models/
│ │ └── IOC/
│ └── tests/
├── chatty_ai/
│ ├── pyproject.toml
│ ├── src/
│ │ └── chatty_ai/
│ └── tests/
├── chatty_core/
│ ├── pyproject.toml
│ ├── src/
│ │ └── chatty_core/
│ │ ├── models/
│ │ ├── database/
│ │ └── conversations/
│ └── tests/
├── chatty_test_services/
│ ├── pyproject.toml
│ ├── src/
│ │ └── chatty_test_services/
│ │ └── mocks/
│ └── tests/