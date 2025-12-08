import mysql.connector
from dotenv import load_dotenv
import os

def probar_consultas(endpoint):
    # Cargar .env
    load_dotenv()

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")


    try:
        conn = mysql.connector.connect(
            host=endpoint,
            user=user,
            password=password,
            database=database
        )

        cursor = conn.cursor()
        print("Conexión exitosa\n")


        # Top 5 intereses más usados

        print("Consulta 1: Intereses más asignados a estudiantes")
        cursor.execute("""
            SELECT i.nombre_interes, COUNT(ei.id_interes) AS total
            FROM intereses i
            JOIN estudiantes_intereses ei ON i.id = ei.id_interes
            GROUP BY i.id
            ORDER BY total DESC
            LIMIT 5;
        """)
        for fila in cursor.fetchall():
            print("  →", fila)

        # Conteo de estudiantes
        print("\nConsulta 2: Número total de estudiantes")
        cursor.execute("SELECT COUNT(*) FROM estudiantes;")
        print("Total estudiantes:", cursor.fetchone()[0])

        # 3️⃣ Estudiantes con más actividades inscritas
        print("\nConsulta 3: Estudiantes con más actividades")
        cursor.execute("""
            SELECT e.nombre, COUNT(a.id_actividad) AS actividades
            FROM estudiantes e
            JOIN estudiantes_actividades a ON e.id = a.id_estudiante
            GROUP BY e.id
            ORDER BY actividades DESC
            LIMIT 5;
        """)
        for fila in cursor.fetchall():
            print("  →", fila)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print("Error al conectar o consultar:", err)
