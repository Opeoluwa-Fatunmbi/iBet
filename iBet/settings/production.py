from .base import *
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ['*']