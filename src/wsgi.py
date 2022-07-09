from flask import Flask

def create_app():
    print('create_app')
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    return app

from src.main import app

if __name__ == "__main__":
    app.run()