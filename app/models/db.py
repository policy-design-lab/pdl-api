from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from ..controllers.configs import Config as cfg

db = SQLAlchemy()

connection_url = URL.create('postgresql', username=cfg.DB_USERNAME, host=cfg.DB_HOST, port=cfg.DB_PORT, database=cfg.DB_NAME, password=cfg.DB_PASSWORD)
engine = create_engine(connection_url)
Session = sessionmaker(bind=engine)
