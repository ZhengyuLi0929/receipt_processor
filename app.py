from flask import Flask
from routes import init_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
init_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
