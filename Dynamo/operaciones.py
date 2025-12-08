from boto3.dynamodb.conditions import Key
from Dynamo.obtenerdatos import obtener_actividad, obtener_estudiante, obtener_interes
from boto3.dynamodb.conditions import Attr



#Eliminar estudiante por nombre
def eliminar_estudiante(dynamodb, nombre):
    dynamodb.delete_item(
        TableName="Estudiantes",
        Key={"nombre": {"S": nombre}}
    )
    print(f"Estudiante '{nombre}' eliminado.")
    print(obtener_estudiante(dynamodb, nombre))


#Eliminar actividad por tipo y fecha
def eliminar_actividad(dynamodb, tipo, fecha):
    dynamodb.delete_item(
        TableName="Actividades",
        Key={"tipo": {"S": tipo}, "fecha": {"S": fecha}}
    )
    print(f"Actividad '{tipo}' del {fecha} eliminada.")
    print(obtener_actividad(dynamodb, tipo, fecha))


# Eliminar interés por nombre_interes
def eliminar_interes(dynamodb, nombre_interes):
    dynamodb.delete_item(
        TableName="Intereses",
        Key={"nombre_interes": {"S": nombre_interes}}
    )
    print(f"Interés '{nombre_interes}' eliminado.")
    print(obtener_interes(dynamodb, nombre_interes))


# Estudiantes
def eliminar_condicional_estudiante(dynamodb, nombre, nivel_socioeconomico_esperado):
    try:
        dynamodb.delete_item(
            TableName='Estudiantes',
            Key={'nombre': {'S': nombre}},
            ConditionExpression="nivel_socioeconomico = :nivel",
            ExpressionAttributeValues={":nivel": {"S": nivel_socioeconomico_esperado}}
        )
        print(f"Estudiante {nombre} eliminado condicionalmente")
    except dynamodb.exceptions.ConditionalCheckFailedException:
        print(f"No se eliminó {nombre}, la condición no se cumplió")

    print(obtener_estudiante(dynamodb, nombre))


# Actividades
def eliminar_condicional_actividad(dynamodb, tipo, fecha, duracion_esperada):
    try:
        dynamodb.delete_item(
            TableName='Actividades',
            Key={'tipo': {'S': tipo}, 'fecha': {'S': fecha}},
            ConditionExpression="duracion = :duracion",
            ExpressionAttributeValues={":duracion": {"S": duracion_esperada}}
        )
        print(f"Actividad {tipo} del {fecha} eliminada condicionalmente")
    except dynamodb.exceptions.ConditionalCheckFailedException:
        print(f"No se eliminó {tipo} del {fecha}, la condición no se cumplió")
    print(obtener_actividad(dynamodb, tipo, fecha))


# Intereses (con índice global)
def eliminar_condicional_interes(dynamodb, dynamodbc, nombre_interes):

    tabla = dynamodb.Table("Intereses")
    response = tabla.query(
        IndexName="NombreInteresIndex",
        KeyConditionExpression=Key("nombre_interes").eq(nombre_interes)
    )

    items = response.get("Items", [])

    if not items:
        print(f"No se encontró el interés '{nombre_interes}' en el índice")
        return

    for item in items:
        try:
            tabla.delete_item(
                Key={"nombre_interes": item["nombre_interes"],},
            )
            print(f"Interés '{nombre_interes}' eliminado condicionalmente")
        except Exception as e:
            print("No se pudo eliminar condicionalmente:", e)

    print(obtener_interes(dynamodbc, nombre_interes))


#Actualizaciones

# Actualizar un estudiante
def actualizar_estudiante(dynamodb, nombre, nuevos_datos):
    update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in nuevos_datos.keys())
    expression_values = {f":{k}": {"S": str(v)} for k, v in nuevos_datos.items()}

    dynamodb.update_item(
        TableName='Estudiantes',
        Key={'nombre': {'S': nombre}},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values
    )
    print(obtener_estudiante(dynamodb, nombre))


# Actualizar una actividad
def actualizar_actividad(dynamodb, tipo, fecha, nuevos_datos):
    update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in nuevos_datos.keys())
    expression_values = {f":{k}": {"S": str(v)} for k, v in nuevos_datos.items()}

    dynamodb.update_item(
        TableName='Actividades',
        Key={'tipo': {'S': tipo}, 'fecha': {'S': fecha}},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values
    )

    print(obtener_actividad(dynamodb, tipo, fecha))


# Actualizar un interés
def actualizar_interes(dynamodb, nombre_interes, nuevos_datos):
    update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in nuevos_datos.keys())
    expression_values = {f":{k}": {"S": str(v)} for k, v in nuevos_datos.items()}

    dynamodb.update_item(
        TableName='Intereses',
        Key={'nombre_interes': {'S': nombre_interes}},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values
    )
    print(obtener_interes(dynamodb, nombre_interes))