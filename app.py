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
    
# Consulta 10.4: Aprendices certificados de ADSO
@app.route("/api/aprendices/adso/certificados", methods=["GET"])
def aprendices_adso_certificados():

    resultado = aprendices.find(
        {
            "PROGRAMA": "ANALISIS Y DESARROLLO DE SOFTWARE.",
            "ESTADO_APRENDIZ": "Certificado"
        },
        {
            "_id": 0,
            "FICHA": 1,
            "NOMBRE": 1,
            "PRIMER_APELLIDO": 1,
            "SEGUNDO_APELLIDO": 1
        }
    )

    return jsonify(list(resultado))

# Consulta 10.5: Aprendices por ficha en estado Por certificar
@app.route("/api/aprendices/ficha/<int:ficha>/por-certificar/<int:cantidad>", methods=["GET"])
def aprendices_por_certificar(ficha, cantidad):
    print("Ficha consultada:", ficha)
    print(
        "Total de aprendices en la ficha:",
        aprendices.count_documents({"FICHA": ficha})
    )
    print(
        "Estados de los aprendices:",
        aprendices.distinct("ESTADO_APRENDIZ", {"FICHA": ficha})
    )
    resultado = aprendices.find(
        {
            "FICHA": ficha,
            "ESTADO_APRENDIZ": "Por certificar"
        },
        {
            "_id": 0,
            "FICHA": 1,
            "PROGRAMA": 1,
            "NUMERO_DOCUMENTO": 1,
            "NOMBRE": 1,
            "PRIMER_APELLIDO": 1,
            "SEGUNDO_APELLIDO": 1
        }
    ).sort("PRIMER_APELLIDO", -1).limit(cantidad)
    return jsonify(list(resultado))

# Consulta 10.6: Aprendices con ficha terminada por unificación
@app.route("/api/aprendices/fichas/unificacion", methods=["GET"])
def aprendices_unificacion():

    resultado = aprendices.find(
        {
            "ESTADO_FICHA": "Terminada por unificación"
        },
        {
            "_id": 0,
            "FICHA": 1,
            "NUMERO_DOCUMENTO": 1,
            "NOMBRE": 1,
            "PRIMER_APELLIDO": 1,
            "SEGUNDO_APELLIDO": 1
        }
    )

    return jsonify(list(resultado))

# Consulta 10.7: Aprendices del programa Power BI
@app.route("/api/aprendices/programa/power-bi", methods=["GET"])
def aprendices_power_bi():

    resultado = aprendices.find(
        {
            "PROGRAMA": "VISUALIZACION DE DATOS USANDO POWER BI"
        },
        {
            "_id": 0,
            "PROGRAMA": 1,
            "FICHA": 1,
            "NOMBRE": 1,
            "PRIMER_APELLIDO": 1,
            "SEGUNDO_APELLIDO": 1
        }
    )

    return jsonify(list(resultado))

# Consulta 10.8: Cantidad de aprendices certificados de Power BI
@app.route("/api/aprendices/programa/power-bi/certificados", methods=["GET"])
def cantidad_certificados_power_bi():

    cantidad = aprendices.count_documents({
        "PROGRAMA": "VISUALIZACION DE DATOS USANDO POWER BI",
        "ESTADO_APRENDIZ": "Certificado"
    })

    return jsonify({
        "programa": "VISUALIZACION DE DATOS USANDO POWER BI",
        "cantidad_certificados": cantidad
    })
    
    
# Consulta 10.9: Aprendices agrupados por estado
@app.route("/api/aprendices/ficha/3312932/estados", methods=["GET"])
def aprendices_por_estado():

    resultado = aprendices.aggregate([
        {
            "$match": {
                "FICHA": 3312932
            }
        },
        {
            "$group": {
                "_id": "$ESTADO_APRENDIZ",
                "cantidad": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "estado": "$_id",
                "cantidad": 1
            }
        },
        {
            "$sort": {
                "estado": 1
            }
        }
    ])

    return jsonify(list(resultado))

# Consulta 10.10: Programas de formación complementaria virtual
@app.route("/api/programas/complementaria-virtual", methods=["GET"])
def programas_complementaria_virtual():

    programas = aprendices.distinct(
        "PROGRAMA",
        {
            "NIVEL_DE_FORMACION": "COMPLEMENTARIA VIRTUAL"
        }
    )

    return jsonify({
        "programas": programas
    })

if __name__ == "__main__":
    app.run(debug=True)
    
