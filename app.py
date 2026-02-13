import os
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Pega a string de conexão do ambiente do Vercel
mongo_uri = os.environ.get("MONGODB_URI")
client = MongoClient(mongo_uri)

# Substitua "meubanco" pelo nome do banco que você criou no Atlas
db = client["meubanco"]

# Substitua "filmes" pelo nome da coleção
collection = db["filmes"]

@app.route("/")
def home():
    # Busca todos os documentos da coleção, sem mostrar o _id
    filmes = list(collection.find({}, {"_id": 0}))
    return jsonify(filmes)