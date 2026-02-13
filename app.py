import os
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

mongo_uri = os.environ.get("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client["meubanco"]
collection = db["filmes"]

@app.route("/")
def home():
    filmes = list(collection.find({}, {"_id": 0}))
    return render_template("index.html", filmes=filmes)