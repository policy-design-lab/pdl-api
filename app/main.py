import connexion
import logging

from time import gmtime
from pdlapiresolver import PdlApiResolver
from controllers.configs import Config as cfg
from app.models.db import db
from flask_cors import CORS

db_connection_url = "postgresql://%s:%s@%s:%s/%s" % \
                    (cfg.DB_USERNAME, cfg.DB_PASSWORD, cfg.DB_HOST, cfg.DB_PORT, cfg.DB_NAME)

debug = cfg.DEBUG

log = logging.getLogger('werkzeug')
log.disabled = True

logging.Formatter.converter = gmtime
log_format = '%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s'

if debug:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.DEBUG)
else:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.INFO)

connexion_app = connexion.App("__name__", specification_dir='./')
connexion_app.add_api('pdl.yaml', base_path=cfg.URL_PREFIX, arguments={'title': 'Policy Design Lab API'},
                      resolver=PdlApiResolver('controllers'), resolver_error=501)

app = connexion_app.app

app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JSON_SORT_KEYS'] = False

db.init_app(app)

CORS(app)

if __name__ == '__main__':
    app.run(port=cfg.API_PORT, host=None, debug=debug)
