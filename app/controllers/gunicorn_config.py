from controllers.configs import Config as cfg

"""Gunicorn configuration."""
bind = f'0.0.0.0:{cfg.API_PORT}'

workers = cfg.WORKER
worker_class = 'gevent'

# If you adjust this number, also adjust the MongoClient pool connections
worker_connections = 100
