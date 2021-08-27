from flask import Flask, request
from dotenv import load_dotenv
import os
from tinydb import TinyDB, Query

load_dotenv()

PORT = int(os.getenv('PORT'))
DEBUG = os.getenv('DEBUG').strip().lower() == "true"
DB = os.getenv('DB').strip()

db = TinyDB(DB)
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


@app.route("/post_method", methods=['POST'])
def postMethod():
    return f"This Is Post Method"


# create blog: require field header, content, author
@app.route("/blogs/create", methods=['POST'])
def createBlog():
    if not request.is_json:
        return "Invalid JSON", 400

    # Basic Validation
    requiredField = [("header", str),
                     ("content", str),
                     ("author", str),
                     ("tags", list)]
    for fieldValue, fieldType in requiredField:
        if fieldValue not in request.json:
            return f"Missing field: {fieldValue}", 400
        elif type(request.json[fieldValue]) != fieldType:
            return f"Invalid field type: {fieldValue} should be {fieldType}", 400
    for tag in request.json["tags"]:
        if type(tag) != str:
            return f"Invalid tag: tag should be string", 400

    blogs = db.table('blogs')
    if blogs.search(Query().header == request.json['header']) != []:
        return f"Can't create blog, blog header already exists.", 409
    else:
        blogs.insert({
            'header': request.json['header'],
            'content': request.json['content'],
            'author': request.json['author'],
            'tags': request.json['tags'],
        })
        return f"Create Blog:\nHeader: {request.json['header']}\nContent: {request.json['content']}\nAuthor: {request.json['author']}\nTags: {', '.join(request.json['tags'])}", 201


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
