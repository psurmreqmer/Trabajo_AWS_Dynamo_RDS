from consultas import probar_consultas
from conexion import conexion_rds
from crea_tablas import create_bd
from rellenadatos import insertar_datos


print("Iniciando proceso")
endpoint = conexion_rds()
create_bd(endpoint)
insertar_datos(endpoint)
probar_consultas(endpoint)