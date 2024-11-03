import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV", "dev")
env_file = f".env.{env}"
load_dotenv(env_file, override=True)

ENV = os.getenv("ENV", "dev")
ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN", "http://localhost:8000")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
