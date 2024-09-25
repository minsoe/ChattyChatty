from dotenv import load_dotenv

from app.openai_service import init_mongodb

load_dotenv()

init_mongodb()