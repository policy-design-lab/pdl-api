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

    # API port, default to 5000
    API_PORT = int(os.getenv('API_PORT', '5000'))

    # PDL data duration parameters
    # NOTE: these are the minimum and maximum years for which data will be retrieved from the database for different endpoints
    ALL_PROGRAMS_START_YEAR = int(os.getenv('ALL_PROGRAMS_START_YEAR', '2018'))  # Landing Page endpoint
    ALL_PROGRAMS_END_YEAR = int(os.getenv('ALL_PROGRAMS_END_YEAR', '2022'))  # Landing Page endpoint

    TITLE_I_START_YEAR = int(os.getenv('TITLE_I_START_YEAR', '2014'))
    TITLE_I_END_YEAR = int(os.getenv('TITLE_I_END_YEAR', '2021'))

    TITLE_II_START_YEAR = int(os.getenv('TITLE_II_START_YEAR', '2014'))
    TITLE_II_END_YEAR = int(os.getenv('TITLE_II_END_YEAR', '2023'))

    CROP_INSURANCE_START_YEAR = int(os.getenv('CROP_INSURANCE_START_YEAR', '2014'))
    CROP_INSURANCE_END_YEAR = int(os.getenv('CROP_INSURANCE_END_YEAR', '2023'))

    SNAP_START_YEAR = int(os.getenv('SNAP_START_YEAR', '2018'))
    SNAP_END_YEAR = int(os.getenv('SNAP_END_YEAR', '2022'))
