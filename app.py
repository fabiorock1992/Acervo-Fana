from flask import Flask, request, jsonify, send_from_directory
import sqlite3, os
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

DB_FILE = "filmes.db"

# Criar tabela se não existir
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            ator TEXT,
            quantidade INTEGER,
            estado TEXT,
            tipo TEXT,
            idioma TEXT,
            prateleira TEXT
        )
    """)
    conn.commit()
    conn.close()

# Listar filmes
@app.route("/listar")
def listar():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, ator, quantidade, estado, tipo, idioma, prateleira FROM filmes")
    rows = cur.fetchall()
    conn.close()
    filmes = [dict(zip(["id","titulo","ator","quantidade","estado","tipo","idioma","prateleira"], r)) for r in rows]
    return jsonify(filmes)

# Adicionar filme
@app.route("/adicionar", methods=["POST"])
def adicionar():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""INSERT INTO filmes (titulo, ator, quantidade, estado, tipo, idioma, prateleira)
                   VALUES (?,?,?,?,?,?,?)""",
                (data["titulo"], data["ator"], data["quantidade"], data["estado"],
                 data["tipo"], data["idioma"], data["prateleira"]))
    conn.commit()
    conn.close()
    return jsonify({"status":"ok"})

# Pesquisar filme
@app.route("/pesquisar")
def pesquisar():
    termo = request.args.get("q","").lower()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, ator, quantidade, estado, tipo, idioma, prateleira FROM filmes")
    rows = cur.fetchall()
    conn.close()
    filmes = [dict(zip(["id","titulo","ator","quantidade","estado","tipo","idioma","prateleira"], r)) for r in rows]
    filtrados = [f for f in filmes if termo in f["titulo"].lower() or termo in f["ator"].lower()]
    return jsonify(filtrados)

# Apagar filme
@app.route("/apagar/<int:id>", methods=["DELETE"])
def apagar(id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM filmes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status":"apagado"})

# Editar filme
@app.route("/editar/<int:id>", methods=["PUT"])
def editar(id):
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""UPDATE filmes SET titulo=?, ator=?, quantidade=?, estado=?, tipo=?, idioma=?, prateleira=? WHERE id=?""",
                (data["titulo"], data["ator"], data["quantidade"], data["estado"],
                 data["tipo"], data["idioma"], data["prateleira"], id))
    conn.commit()
    conn.close()
    return jsonify({"status":"atualizado"})

# Servir o frontend
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)