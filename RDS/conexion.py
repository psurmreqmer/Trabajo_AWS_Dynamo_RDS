import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import os

load_dotenv()

session = boto3.session.Session(
aws_access_key_id=os.getenv("ACCESS_KEY"),
aws_secret_access_key=os.getenv("SECRET_KEY"),
aws_session_token=os.getenv("SESSION_TOKEN"),
region_name=os.getenv("REGION"))

rds = session.client('rds')


def conexion_rds():

    try:
        print("Comprobando si la instancia RDS ya existe...")
        info = rds.describe_db_instances(DBInstanceIdentifier=os.getenv("DB_INSTANCE_ID"))
        print(f"La instancia '{os.getenv('DB_INSTANCE_ID')}' ya existe.")
    except ClientError as e:
        print("Creando instancia RDS...")
        rds.create_db_instance(
                DBInstanceIdentifier="estudiantes", #Nombre de la instancia del RDS
                AllocatedStorage= 20, #El tamaño del RDS
                DBInstanceClass="db.t4g.micro", #Tipo de clase de la base de datos
                Engine="mariadb", # motor de base de datos
                MasterUsername=os.getenv("DB_USER"), #usuario de la base de datos
                MasterUserPassword=os.getenv("DB_PASSWORD"), #password del usuario admin
                PubliclyAccessible=True #Publicar el RDS
        )

        print("Usamos los waiters para esperar a que la instancia esté disponible")
        waiter = rds.get_waiter('db_instance_available') #Usaremos el waiter para continuar con el código cuando esté disponible el RDS
        waiter.wait(DBInstanceIdentifier=os.getenv("DB_INSTANCE_ID"))
        print("La instancia RDS está disponible")

    info = rds.describe_db_instances(DBInstanceIdentifier=os.getenv("DB_INSTANCE_ID")) 
    endpoint = info['DBInstances'][0]['Endpoint']['Address'] #IMPORTANTE, necesitamos el endpoint para conectarnos a la base de datos

    print(endpoint)

    return endpoint