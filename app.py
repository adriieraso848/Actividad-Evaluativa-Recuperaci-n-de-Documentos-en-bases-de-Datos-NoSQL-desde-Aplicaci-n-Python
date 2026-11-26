from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

cliente = MongoClient(MONGO_URI)

db = cliente["CURSOS_CTPI_2026-ADRIANA"]

aprendices = db["APRENDICES_ERASO"]

@app.route("/")
def inicio():
    return "API de aprendices CTPI funcionando"


# Consulta 10.1: Cantidad total de aprendices
@app.route("/api/aprendices/cantidad", methods=["GET"])
def cantidad_aprendices():
    cantidad = aprendices.count_documents({})

    return jsonify({
        "cantidad_aprendices": cantidad
    })


if __name__ == "__main__":
    app.run(debug=True)
    