from conexion import *

# Obtiene un estudiante por su nombre
def obtener_estudiante(dynamodb, nombre):
    response = dynamodb.get_item(
        TableName='Estudiantes',
        Key={'nombre': {'S': nombre}}
    )
    return response.get('Item', None)

# Obtiene un estudiante por su nombre
def obtener_actividad(dynamodb, tipo, fecha):
    response = dynamodb.get_item(
        TableName='Actividades',
        Key={'tipo': {'S': tipo}, 'fecha': {'S': fecha}}
    )
    return response.get('Item', None)

# Obtiene un estudiante por su nombre
def obtener_interes(dynamodb, nombre_interes):
    response = dynamodb.get_item(
        TableName='Intereses',
        Key={'nombre_interes': {'S': nombre_interes}}
    )
    return response.get('Item', None)

# Obtiene todos los registros de todas las tablas
def obtener_todos(dynamodb):
    tablas = ["Estudiantes", "Actividades", "Intereses"]

    for nombre_tabla in tablas:
        table = dynamodb.Table(nombre_tabla)
        print(f"\nTodos los registros de {nombre_tabla}:")
        response = table.scan() 
        items = response.get("Items", [])
        if not items:
            print("  No hay registros.")
        else:
            for item in items:
                print("  ", item)

# Realiza un scan con filtros en las tres tablas
def scan_filtrado(dynamodb):

    table_estudiantes = dynamodb.Table("Estudiantes")
    response = table_estudiantes.scan(
        FilterExpression="nivel_socioeconomico = :nivel",
        ExpressionAttributeValues={":nivel": "Alto"}
    )
    print("Estudiantes filtrados por nivel socioeconómico 'Alto':")
    for item in response['Items']:
        print(item)

    table_actividades = dynamodb.Table("Actividades")
    response = table_actividades.scan(
        FilterExpression="tipo = :tipo AND fecha >= :fecha_inicio",
        ExpressionAttributeValues={
            ":tipo": "Deporte",
            ":fecha_inicio": "2023-01-01"
        }
    )
    print("\nActividades deportivas a partir de 2023:")
    for item in response['Items']:
        print(item)


    table_intereses = dynamodb.Table("Intereses")
    response = table_intereses.scan(
        IndexName="NombreInteresIndex",
        FilterExpression="nombre_interes = :interes",
        ExpressionAttributeValues={":interes": "Programación"}
    )
    print("\nIntereses filtrados por 'Programación':")
    for item in response['Items']:
        print(item)

# Obtiene un estudiante usando PartiQL
def partiql_get_estudiante(dynamodb, nombre):
    query = "SELECT * FROM Estudiantes WHERE nombre=?"
    params = [{"S": nombre}]
    response = dynamodb.execute_statement(Statement=query, Parameters=params)
    return response.get("Items", [])

# Obtiene actividades usando PartiQL filtrando por tipo
def partiql_get_actividad(dynamodb, tipo):
    query = "SELECT * FROM Actividades WHERE tipo=?"
    params = [{"S": tipo}]
    response = dynamodb.execute_statement(Statement=query, Parameters=params)
    return response.get("Items", [])

# Obtiene intereses usando PartiQL filtrando por nombre_interes
def partiql_get_interes(dynamodb, nombre_interes):
    query = "SELECT * FROM Intereses WHERE nombre_interes=?"
    params = [{"S": nombre_interes}]
    response = dynamodb.execute_statement(Statement=query, Parameters=params)
    return response.get("Items", [])