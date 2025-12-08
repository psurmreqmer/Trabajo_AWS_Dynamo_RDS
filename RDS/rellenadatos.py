from faker import Faker
import mysql.connector
import os
import random

fake = Faker("es_ES")

def insertar_datos(endpoint):

    config = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": endpoint,
        "database": os.getenv("DB_NAME")
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    print("\nInsertando datos en la BD...\n")

    # ---------- ESTUDIANTES ----------
    for _ in range(10):
        cursor.execute("""
            INSERT INTO estudiantes (nombre, edad, genero, nivel_socioeconomico, direccion, situacion_familiar, fecha_registro)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            fake.name(),
            random.randint(18, 30),
            random.choice(["Masculino", "Femenino", "Otro"]),
            random.choice(["Bajo", "Medio", "Alto"]),
            fake.address(),
            fake.sentence(),
            fake.date_this_decade()
        ))

    # ---------- INTERESES ----------
    for _ in range(10):
        cursor.execute("""
            INSERT INTO intereses (nombre_interes, descripcion)
            VALUES (%s, %s)
        """, (fake.word(), fake.sentence()))

    # ---------- HABILIDADES ----------
    for _ in range(10):
        cursor.execute("""
            INSERT INTO habilidades (nombre_habilidad, tipo_habilidad, descripcion)
            VALUES (%s, %s, %s)
        """, (
            fake.word(),
            random.choice(["Técnica", "Social", "Creativa"]),
            fake.sentence()
        ))

    # ---------- ACTIVIDADES EXTRAESCOLARES ----------
    for _ in range(10):
        cursor.execute("""
            INSERT INTO actividades_extraescolares (nombre, tipo, duracion, fecha_ini, fecha_fin)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            fake.word(),
            random.choice(["Deporte", "Arte", "Música", "Voluntariado"]),
            f"{random.randint(1,12)} meses",
            fake.date_this_decade(),
            fake.date_this_decade()
        ))

    # ---------- FORMACIONES ----------
    for _ in range(10):
        cursor.execute("""
            INSERT INTO formaciones (nombre_formacion, area_id, nivel_requerido, duracion_meses, centro, direccion, provincia)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            fake.job(),
            random.randint(1, 10),
            random.choice(["Básico", "Medio", "Avanzado"]),
            random.randint(3, 24),
            fake.company(),
            fake.address(),
            random.randint(1, 50)
        ))

    # ---------- HISTORIAL ----------
    for _ in range(10):
        cursor.execute("""
            INSERT INTO historial_academico (id_estudiante, nombre_curso, calificacion, fecha_finalizacion)
            VALUES (%s,%s,%s,%s)
        """, (
            random.randint(1, 10),
            fake.word(),
            round(random.uniform(5, 10), 2),
            fake.date_this_decade()
        ))

    # ---------- RELACIONES ----------
    for _ in range(10):
        cursor.execute("""
            INSERT INTO estudiantes_intereses (id_estudiante, id_interes, nivel_interes)
            VALUES (%s,%s,%s)
        """, (
            random.randint(1, 10),
            random.randint(1, 10),
            random.randint(1, 5)
        ))

    for _ in range(10):
        cursor.execute("""
            INSERT INTO estudiante_habilidades (id_estudiante, id_habilidad, nivel)
            VALUES (%s,%s,%s)
        """, (
            random.randint(1, 10),
            random.randint(1, 10),
            random.randint(1, 5)
        ))

    for _ in range(10):
        cursor.execute("""
            INSERT INTO preferencias_formaciones_estudiantes (id_estudiante, id_formacion, nivel_interes, fecha_registro)
            VALUES (%s,%s,%s,%s)
        """, (
            random.randint(1, 10),
            random.randint(1, 10),
            random.choice(["Alta", "Media", "Baja"]),
            fake.date_this_decade()
        ))

    for _ in range(10):
        cursor.execute("""
            INSERT INTO estudiantes_actividades (id_estudiante, id_actividad, fecha_inscripcion)
            VALUES (%s,%s,%s)
        """, (
            random.randint(1, 10),
            random.randint(1, 10),
            fake.date_this_decade()
        ))

    cnx.commit()
    cursor.close()
    cnx.close()

    print("✔ Datos insertados correctamente.\n")
