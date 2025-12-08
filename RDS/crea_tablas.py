import mysql.connector
from dotenv import load_dotenv
from mysql.connector import errorcode
import os

load_dotenv()


def create_bd(endpoint):

    config = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": endpoint
    }

    DB_NAME = os.getenv("DB_NAME")

    TABLES = {}

    TABLES['estudiantes'] = (
        "CREATE TABLE IF NOT EXISTS estudiantes ("
        " id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " nombre VARCHAR(100) NOT NULL,"
        " edad INT,"
        " genero VARCHAR(20),"
        " nivel_socioeconomico VARCHAR(20),"
        " direccion VARCHAR(100),"
        " situacion_familiar VARCHAR(100),"
        " fecha_registro DATE)"
    )

    TABLES['intereses'] = (
        "CREATE TABLE IF NOT EXISTS intereses ("
        " id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " nombre_interes VARCHAR(100),"
        " descripcion TEXT)"
    )

    TABLES['habilidades'] = (
        "CREATE TABLE IF NOT EXISTS habilidades ("
        " id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " nombre_habilidad VARCHAR(100),"
        " tipo_habilidad VARCHAR(50),"
        " descripcion TEXT)"
    )

    TABLES['actividades_extraescolares'] = (
        "CREATE TABLE IF NOT EXISTS actividades_extraescolares ("
        " id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " nombre VARCHAR(255),"
        " tipo VARCHAR(255),"
        " duracion VARCHAR(255),"
        " fecha_ini DATE,"
        " fecha_fin DATE)"
    )

    TABLES['formaciones'] = (
        "CREATE TABLE IF NOT EXISTS formaciones ("
        " id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " nombre_formacion VARCHAR(150),"
        " area_id INT,"
        " nivel_requerido VARCHAR(50),"
        " duracion_meses INT,"
        " centro VARCHAR(150),"
        " direccion VARCHAR(100),"
        " provincia INT,"
        " FOREIGN KEY (area_id) REFERENCES intereses(id))"
    )

    TABLES['historial_academico'] = (
        "CREATE TABLE IF NOT EXISTS historial_academico ("
        " id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " id_estudiante INT,"
        " nombre_curso VARCHAR(150),"
        " calificacion DECIMAL(5,2),"
        " fecha_finalizacion DATE,"
        " FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id))"
    )

    TABLES['estudiantes_intereses'] = (
        "CREATE TABLE IF NOT EXISTS estudiantes_intereses ("
        " id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " id_estudiante INT,"
        " id_interes INT,"
        " nivel_interes INT,"
        " FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id),"
        " FOREIGN KEY (id_interes) REFERENCES intereses(id))"
    )

    TABLES['estudiante_habilidades'] = (
        "CREATE TABLE IF NOT EXISTS estudiante_habilidades ("
        " id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " id_estudiante INT,"
        " id_habilidad INT,"
        " nivel INT,"
        " FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id),"
        " FOREIGN KEY (id_habilidad) REFERENCES habilidades(id))"
    )

    TABLES['preferencias_formaciones_estudiantes'] = (
        "CREATE TABLE IF NOT EXISTS preferencias_formaciones_estudiantes ("
        " id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " id_estudiante INT,"
        " id_formacion INT,"
        " nivel_interes VARCHAR(255),"
        " fecha_registro DATE,"
        " FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id),"
        " FOREIGN KEY (id_formacion) REFERENCES formaciones(id))"
    )

    TABLES['estudiantes_actividades'] = (
        "CREATE TABLE IF NOT EXISTS estudiantes_actividades ("
        " id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " id_estudiante INT,"
        " id_actividad INT,"
        " fecha_inscripcion DATE,"
        " FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id),"
        " FOREIGN KEY (id_actividad) REFERENCES actividades_extraescolares(id))"
    )

    # Conexión y ejecución
    
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    print("Comprobando si la base de datos existe...")

    try:
        cursor.execute(f"USE {DB_NAME}")
        print(f"La base de datos '{DB_NAME}' ya existe.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe. Creándola...")
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            cursor.execute(f"USE {DB_NAME}")
            print(f"Base de datos '{DB_NAME}' creada con éxito.")
        else:
            raise err

    for name, ddl in TABLES.items():
        print(f"Creando tabla {name} si no existe...")
        cursor.execute(ddl)

    print("\nBase de datos y tablas listas.\n")

    cursor.close()
    cnx.close()