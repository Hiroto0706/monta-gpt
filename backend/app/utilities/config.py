import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV", "dev")
env_file = f".env.{env}"
load_dotenv(env_file, override=True)

# DB
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_NAME = os.getenv("POSTGRES_NAME")
POSTGRES_URL = os.getenv("POSTGRES_URL")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_URL = os.getenv("REDIS_URL")

# Google Cloud OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Others
ENV = os.getenv("ENV", "dev")
DEFAULT_SESSION_EXPIRATION_DAY = os.getenv("DEFAULT_SESSION_EXPIRATION_DAY", 7)
ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN").split(",")
