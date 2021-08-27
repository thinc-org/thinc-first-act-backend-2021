from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from tinydb import TinyDB, Query, where

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


@app.route("/blogs/all")
def getAllBlogs():
    blogs = db.table('blogs')
    return jsonify(blogs.all())


@app.route("/blogs/header/<string:header>")
def getBlog(header):
    blogs = db.table('blogs')
    blogData = blogs.search(where('header') == header)
    if (len(blogData) == 0):
        return f'Blog "{header}" Not Found', 404
    else:
        return jsonify(blogData[0])


@app.route("/blogs/author/<string:author>")
def getBlogsByAuthor(author):
    blogs = db.table('blogs')
    return jsonify(blogs.search(where('author') == author))


@app.route("/blogs/search")
def searchBlogs():
    blogs = db.table('blogs')
    return jsonify(blogs.search(Query().tags.any([request.args.get('tag')])))


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


@app.route("/blogs/update/<string:header>", methods=['PUT'])
def updateBlog(header):
    blogs = db.table('blogs')
    updateBlogID = blogs.update(
        {"content": request.data.decode('utf-8')}, where('header') == header)
    if len(updateBlogID) == 0:
        return f'Blog "{header}" Not Found', 404
    else:
        return f'Blog "{header}" Updated', 200


@app.route("/blogs/delete/<string:header>", methods=['DELETE'])
def deleteBlog(header):
    blogs = db.table('blogs')
    removeBlogID = blogs.remove(where('header') == header)
    if len(removeBlogID) == 0:
        return f'Blog "{header}" Not Found', 404
    else:
        return f'Blog "{header}" Deleted', 200


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
