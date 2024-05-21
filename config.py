from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")
DATABASE_URL = getenv("DATABASE_URL")
