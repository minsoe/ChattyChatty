# ChattyChatty

ChattyChatty is a backend application written in Python, utilizing FastAPI and MongoDB. It provides a conversational AI service and can be run locally using Docker or a Python virtual environment.

## Table of Contents
- Getting Started
- Running the Application
  - Using Docker
  - Without Docker
- Environment Variables
- Dependencies
- Folder Structure
- Contributing
- Suggestions for Improvement

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

2. Create a Python virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Install FastAPI CLI:
    ```sh
    pip install "fastapi[standard]"
    ```

5. Create a `.env` file in the root directory and add the following environment variables:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    MONGODB_URL=your_mongodb_url
    ```

6. Run the application:
    ```sh
   fastapi dev main.py
    ```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key.
- `MONGODB_URL`: The URL for your MongoDB server.

## Dependencies
- `openai==1.47.1`
- `pymongo==4.9.1`
- `pydantic==2.9.2`
- `python-dotenv==1.0.1`
- `motor==3.6.0`
- `beanie==1.26.0`
- `fastapi==0.115.0`

## Folder Structure
```
- ChattyChatty
 - docker-compose.yml
 - main.py
 - requirements.txt
 - app
    - api-services
      - conversation_router.py
      - prompt.py
    - database
      - conversation_manager.py
      - datbase.py
      - models.py
    - open_ai
      - openai_service.py
  - tests
    - conversation_manager_tests.py
    - conversation_router_tests.py
    - openai_service_tests.py
```