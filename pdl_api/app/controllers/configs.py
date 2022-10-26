import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()

# this has to be have the file path to the folder for saving image files and other necessary files from rest service
FLASK_APP = os.getenv('FLASK_APP', 'app')
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
API_LOC = os.getenv('API_LOC', '../')
PROFILE_URL_PREFIX = os.getenv('PROFILE_URL_PREFIX', '')
DEBUG = bool(os.getenv('DEBUG', 'False') == 'True')
