from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv('PORT'))
DEBUG = os.getenv('DEBUG').strip().lower() == "true"

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, Flask"


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
