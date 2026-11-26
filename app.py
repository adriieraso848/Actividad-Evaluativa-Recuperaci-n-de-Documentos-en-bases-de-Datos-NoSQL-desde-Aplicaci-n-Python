from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
cliente = MongoClient(MONGO_URI)

db = cliente["CURSOS_CTPI_2026_JULIETH"]
aprendices = db["APRENDICES_MONTERO"]

print("Base de datos:", db.name)
print("Colecciones:", db.list_collection_names())
print("Cantidad de documentos:", aprendices.count_documents({}))
print("Primer documento:", aprendices.find_one())

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
    
# Consulta 10.2: Cantidad de aprendices por nivel de formación
@app.route("/api/aprendices/nivel_formacion", methods=["GET"])
def aprendices_por_nivel():

    resultado = aprendices.aggregate([
        {
            "$group": {
                "_id": "$NIVEL_DE_FORMACION",
                "cantidad": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "nivel_formacion": "$_id",
                "cantidad": 1
            }
        },
        {
            "$sort": {
                "nivel_formacion": 1
            }
        }
    ])

    return jsonify(list(resultado))

# Consulta 10.3: Programas de nivel TECNÓLOGO
@app.route("/api/programas/tecnologo", methods=["GET"])
def programas_tecnologo():

    programas = aprendices.distinct(
        "PROGRAMA",
        {"NIVEL_DE_FORMACION": "TECNÓLOGO"}
    )

    return jsonify({
        "programas": programas
    })

if __name__ == "__main__":
    app.run(debug=True)