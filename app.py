from flask import Flask
from controller.banco_controller import banco_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(banco_blueprint)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
