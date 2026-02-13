import os
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/")
def home():
    try:
        mongo_uri = os.environ.get("MONGODB_URI")
        client = MongoClient(mongo_uri)
        db = client["meubanco"]  # ajuste para o nome real do banco
        collection_names = db.list_collection_names()
        return f"Conectado ao MongoDB! Coleções: {collection_names}"
    except Exception as e:
        return f"Erro na conexão: {str(e)}"