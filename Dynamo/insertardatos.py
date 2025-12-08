from conexion import conectarseDynamoDBCliente

"""Inserta 3 registros en la tabla Estudiantes"""
def insertar_estudiantes(dynamodb):
    tabla = 'Estudiantes'
    estudiantes = [
        {"nombre": "Ana Pérez", "edad": "22", "genero": "Femenino", "nivel_socioeconomico": "Alto"},
        {"nombre": "Juan Pérez", "edad": "25", "genero": "Masculino", "nivel_socioeconomico": "Alto"},
        {"nombre": "Lucía García", "edad": "20", "genero": "Femenino", "nivel_socioeconomico": "Bajo"}
    ]
    for e in estudiantes:
        dynamodb.put_item(TableName=tabla, Item={k: {"S": str(v)} for k, v in e.items()})
    print("3 registros insertados en Estudiantes")

"""Inserta 3 registros en la tabla Actividades"""
def insertar_actividades(dynamodb):
    tabla = 'Actividades'
    actividades = [
        {"tipo": "Deporte", "fecha": "2025-12-01", "duracion": "2h"},
        {"tipo": "Arte", "fecha": "2025-12-02", "duracion": "3h"},
        {"tipo": "Música", "fecha": "2025-12-03", "duracion": "1.5h"}
    ]
    for a in actividades:
        dynamodb.put_item(TableName=tabla, Item={k: {"S": str(v)} for k, v in a.items()})
    print("3 registros insertados en Actividades")

"""Inserta 3 registros en la tabla Intereses"""
def insertar_intereses(dynamodb):
    tabla = 'Intereses'
    intereses = [
        {"nombre_interes": "Programación"},
        {"nombre_interes": "Música"},
        {"nombre_interes": "Fútbol"}
    ]
    for i in intereses:
        dynamodb.put_item(TableName=tabla, Item={k: {"S": str(v)} for k, v in i.items()})
    print("3 registros insertados en Intereses")