from flask import Flask
from controller.banco_controller import banco_blueprint, PORTA

def create_app():
    app = Flask(__name__)
    app.register_blueprint(banco_blueprint)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=PORTA)
