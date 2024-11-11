import logging
from flask import Flask
from routes import init_routes
from config import Config


# app and config
app = Flask(__name__)
app.config.from_object(Config)

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("receipt processor has started.")

# routes
init_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
