from pydantic import pydantic_settings, BaseSettings, ConfigDict
from dotenv import load_dotenv
import os

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

