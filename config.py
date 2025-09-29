import os
import requests

from dotenv import load_dotenv
from auth import get_auth_headers

load_dotenv()

api_url = os.getenv("42_API_URL")
