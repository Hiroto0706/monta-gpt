import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV", "dev")
env_file = f".env.{env}"
load_dotenv(env_file, override=True)

# DB
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "")
POSTGRES_NAME = os.getenv("POSTGRES_NAME", "")
POSTGRES_URL = os.getenv("POSTGRES_URL", "")

# Google Cloud OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "")
SECRET_KEY = os.getenv("SECRET_KEY", "")

# Others
ENV = os.getenv("ENV", "dev")
DEFAULT_SESSION_EXPIRATION_DAY = os.getenv("DEFAULT_SESSION_EXPIRATION_DAY", 7)
