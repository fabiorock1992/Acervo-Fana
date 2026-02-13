from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Meu acervo de filmes está online!"