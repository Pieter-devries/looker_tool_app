from flask import Flask
import secrets

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

from routes import *



if __name__ == "__main__":
    app.run(debug=True)
