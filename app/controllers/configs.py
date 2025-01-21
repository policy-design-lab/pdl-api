import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """
    class to list all configuration settings required for preprocessing and formatting for EddyPro and PyFluxPro
    """
    # app parameters
    FLASK_APP = os.getenv('FLASK_APP', 'app')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    API_LOC = os.getenv('API_LOC', '.')
    URL_PREFIX = os.getenv('URL_PREFIX', '')
    DEBUG = bool(os.getenv('DEBUG', 'False') == 'True')
    WORKER = os.getenv('WORKER', 2)

    # database parameters
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    # If API_PORT is not set or is empty (null), default to 5000
    api_port_env = os.environ.get('API_PORT')
    API_PORT = int(api_port_env) if api_port_env else 5000
