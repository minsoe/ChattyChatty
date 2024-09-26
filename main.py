from dotenv import load_dotenv
from app.database import init_mongodb

load_dotenv()

init_mongodb()