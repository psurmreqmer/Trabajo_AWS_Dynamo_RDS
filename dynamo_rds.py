import boto3
from boto3.dynamodb.conditions import Attr
from dotenv import load_dotenv
import mysql.connector
import os
import json
import datetime

load_dotenv()



session = boto3.session.Session(
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    aws_session_token=os.getenv("SESSION_TOKEN"),
    region_name=os.getenv("REGION")
)

dynamodb = session.resource('dynamodb')
tabla_estudiantes_dynamo = dynamodb.Table("Estudiantes")
tabla_intereses_dynamo = dynamodb.Table("Intereses")
tabla_actividades_dynamo = dynamodb.Table("Actividades")


rds_conn = mysql.connector.connect(
    host=os.getenv("ENDPOINT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=3306
)
rds_cursor = rds_conn.cursor(dictionary=True)



# Consultas DynamoDB
def obtener_estudiantes_dynamo(nivel):
    resp = tabla_estudiantes_dynamo.scan(
        FilterExpression=Attr("nivel_socioeconomico").eq(nivel)
    )
    return resp.get("Items", [])

def obtener_intereses_dynamo(nombre_interes):
    resp = tabla_intereses_dynamo.scan(
        FilterExpression=Attr("nombre_interes").eq(nombre_interes)
    )
    return resp.get("Items", [])

def obtener_actividades_dynamo(tipo, fecha_inicio):
    resp = tabla_actividades_dynamo.scan(
        FilterExpression=Attr("tipo").eq(tipo) & Attr("fecha").gte(fecha_inicio)
    )
    return resp.get("Items", [])

# Consultas RDS MySQL
def obtener_estudiantes_rds():
    query = "SELECT * FROM estudiantes WHERE nivel_socioeconomico = %s"
    rds_cursor.execute(query, ("Alto",))
    return rds_cursor.fetchall()

def obtener_estudiantes_intereses_rds():
    query = """
        SELECT e.nombre AS estudiante, i.nombre_interes, ei.nivel_interes
        FROM estudiantes_intereses ei
        JOIN estudiantes e ON ei.id_estudiante = e.id
        JOIN intereses i ON ei.id_interes = i.id
        WHERE e.nivel_socioeconomico = %s
    """
    rds_cursor.execute(query, ("Alto",))
    return rds_cursor.fetchall()

def obtener_actividades_extraescolares_rds(fecha_inicio):
    query = """
        SELECT ae.nombre, ae.tipo, ae.duracion, ea.fecha_inscripcion, e.nombre AS estudiante
        FROM estudiantes_actividades ea
        JOIN estudiantes e ON ea.id_estudiante = e.id
        JOIN actividades_extraescolares ae ON ea.id_actividad = ae.id
        WHERE ea.fecha_inscripcion >= %s
    """
    rds_cursor.execute(query, (fecha_inicio,))
    return rds_cursor.fetchall()


# Crear JSON combinado
def crear_json_combinado():
    data = {
        "DynamoDB": {
            "Estudiantes": obtener_estudiantes_dynamo("Bajo"),
            "Intereses": obtener_intereses_dynamo("Música"),
            "Actividades": obtener_actividades_dynamo("Música", "2025-12-03")
        },
        "RDS": {
            "Estudiantes": obtener_estudiantes_rds(),
            "Estudiantes_Intereses": obtener_estudiantes_intereses_rds(),
            "Actividades_Extraescolares": obtener_actividades_extraescolares_rds("2025-01-01")
        }
    }

    # Convertir todas las fechas a string
    data_serializable = convertir_fechas(data)

    with open("datos_combinados.json", "w", encoding="utf-8") as f:
        json.dump(data_serializable, f, ensure_ascii=False, indent=4)

    print("Archivo 'datos_combinados.json' creado con éxito.")



#Utilidad
def convertir_fechas(obj):
    if isinstance(obj, list):
        return [convertir_fechas(o) for o in obj]
    elif isinstance(obj, dict):
        return {k: convertir_fechas(v) for k, v in obj.items()}
    elif isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    else:
        return obj

# -------------------------------
# Ejecutar
# -------------------------------
if __name__ == "__main__":
    crear_json_combinado()
    rds_cursor.close()
    rds_conn.close()