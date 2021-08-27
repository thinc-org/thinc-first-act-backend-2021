from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv('PORT'))
DEBUG = os.getenv('DEBUG').strip().lower() == "true"

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, Flask"


@app.route("/path_parameter/<int:id>")  # /blogs/{id}
def pathParameter(id):
    return f"From Path Parameter\nRequest For ID: {id}"


@app.route("/query_parameter")  # /blogs?id=1
def queryParameter():
    return f"From Query Parameter\nRequest For ID: {request.args.get('id')}"


@app.route("/request_body")
def requestBody():
    return f"From Request Body\nRequest For ID: {request.json['id']}"


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
