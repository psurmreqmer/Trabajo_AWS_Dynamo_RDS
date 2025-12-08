import time

TABLAS = ["Estudiantes", "Actividades", "Intereses"]

# Tabla Estudiantes
def crear_tabla_estudiantes(dynamodb):
    try:
        tabla_estudiantes = dynamodb.create_table(
            TableName='Estudiantes',
            AttributeDefinitions=[{'AttributeName': 'nombre', 'AttributeType': 'S'}],
            KeySchema=[{'AttributeName': 'nombre', 'KeyType': 'HASH'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Tabla Estudiantes creada.")
    except dynamodb.exceptions.ResourceInUseException:
        print("Tabla Estudiantes ya existe.")

# Tabla Actividades
def crear_tabla_actividades(dynamodb):
    try:
        tabla_actividades = dynamodb.create_table(
            TableName='Actividades',
            AttributeDefinitions=[
                {'AttributeName': 'tipo', 'AttributeType': 'S'},
                {'AttributeName': 'fecha', 'AttributeType': 'S'}
            ],
            KeySchema=[
                {'AttributeName': 'tipo', 'KeyType': 'HASH'},
                {'AttributeName': 'fecha', 'KeyType': 'RANGE'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Tabla Actividades creada.")
    except dynamodb.exceptions.ResourceInUseException:
        print("Tabla Actividades ya existe.")

# Tabla Intereses
def crear_tabla_intereses(dynamodb):
    try:
        tabla_intereses = dynamodb.create_table(
            TableName='Intereses',
            AttributeDefinitions=[{'AttributeName': 'nombre_interes', 'AttributeType': 'S'}],
            KeySchema=[{'AttributeName': 'nombre_interes', 'KeyType': 'HASH'}],
            GlobalSecondaryIndexes=[{
                'IndexName': 'NombreInteresIndex',
                'KeySchema':[{'AttributeName': 'nombre_interes', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            }],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Tabla Intereses creada.")
    except dynamodb.exceptions.ResourceInUseException:
        print("Tabla Intereses ya existe.")

# Espera hasta que todas las tablas estén activas
def espera_tablas(dynamodb):
    print("Esperando a que las tablas estén activas...")
    while True:
        todas_activas = True
        for tabla in TABLAS:
            try:
                status = dynamodb.describe_table(TableName=tabla)['Table']['TableStatus']
                if status != 'ACTIVE':
                    todas_activas = False
                    print(f"Tabla {tabla} todavía no está activa (status={status})")
            except dynamodb.exceptions.ResourceNotFoundException:
                todas_activas = False
                print(f"Tabla {tabla} aún no creada.")
        
        if todas_activas:
            print("Todas las tablas están activas.")
            break
        time.sleep(3)
