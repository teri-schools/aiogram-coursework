"""
This module provides configuration settings for the application.

It loads environment variables from a `.env` file using the `python-dotenv` library.

Attributes:
    TOKEN (str): The Telegram Bot API token, loaded from the `TOKEN` environment variable.
    DATABASE_URL (str): The URL for connecting to the database, loaded from the `DATABASE_URL` environment variable.
"""
from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")
DATABASE_URL = getenv("DATABASE_URL")
