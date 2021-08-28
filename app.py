from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from tinydb import TinyDB, Query, where

load_dotenv()

PORT = int(os.getenv('PORT'))
DEBUG = os.getenv('DEBUG').strip().lower() == "true"
DB = os.getenv('DB').strip()

db = TinyDB(DB)
app = Flask(__name__)
#CORS 
cors = CORS(app)

#First route request
@app.route("/")
def hello_world():
    return "Hello, Flask"

#Get id from parameter
@app.route("/path_parameter/<int:id>")  # /blogs/{id}
def pathParameter(id):
    return f"From Path Parameter\nRequest For ID: {id}"

#Get id from query
@app.route("/query_parameter")  # /blogs?id=1
def queryParameter():
    return f"From Query Parameter\nRequest For ID: {request.args.get('id')}"

#Get id from json body
@app.route("/request_body")
def requestBody():
    return f"From Request Body\nRequest For ID: {request.json['id']}"

#POST method
@app.route("/post_method", methods=['POST'])
def postMethod():
    return f"This Is Post Method"

#Get all blogs
@app.route("/blogs/all")
def getAllBlogs():
    blogs = db.table('blogs')
    data = {"blogs" : blogs.all()}
    return jsonify(data)

#Search blog from header
@app.route("/blogs/header/<string:header>")
def getBlog(header):
    blogs = db.table('blogs')
    blogData = blogs.search(where('header') == header)
    if (len(blogData) == 0):
        return f'Blog "{header}" Not Found', 404
    else:
        return jsonify(blogData[0])

#Search blog from author
@app.route("/blogs/author/<string:author>")
def getBlogsByAuthor(author):
    blogs = db.table('blogs')
    wanted_blogs = blogs.search(where('author') == author)
    data = {"blogs":wanted_blogs}
    return jsonify(data)

#Search blogs from tags
@app.route("/blogs/search")
def searchBlogs():
    blogs = db.table('blogs')
    return jsonify(blogs.search(Query().tags.any([request.args.get('tag')])))


# create blog: require field header, content, author
@app.route("/blogs/create", methods=['POST'])
def createBlog():
    blogs = db.table('blogs')
    blogs.insert({
        'header': request.json['header'],
        'content': request.json['content'],
        'author': request.json['author'],
        'tags': request.json['tags'],
    })
    return f"Create Blog:\nHeader: {request.json['header']}", 201

#Update blog
@app.route("/blogs/update/<string:header>", methods=['PUT'])
def updateBlog(header):
    blogs = db.table('blogs')
    updateBlogID = blogs.update(
        {"content": request.data.decode('utf-8')}, where('header') == header)
    if len(updateBlogID) == 0:
        return f'Blog "{header}" Not Found', 404
    else:
        return f'Blog "{header}" Updated', 200

#Delete blog
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
