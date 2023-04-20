from controllers.configs import Config as cfg

"""Gunicorn configuration."""
bind = '0.0.0.0:5000'

workers = cfg.WORKER
worker_class = 'gevent'

# If you adjust this number, also adjust the MongoClient pool connections
worker_connections = 100
