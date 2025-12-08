from Dynamo.operaciones import *
from insertardatos import *
from crea_tablas import *
from obtenerdatos import *

dynamodbc = conectarseDynamoDBCliente()
dynamodbr = conectarseDynamoDBResource()

print("===== CREANDO TABLAS =====")
crear_tabla_estudiantes(dynamodbc)
crear_tabla_actividades(dynamodbc)
crear_tabla_intereses(dynamodbc)

espera_tablas(dynamodbc)
print()
print("===== INSERTAR DATOS EN TABLAS =====")
insertar_estudiantes(dynamodbc)
insertar_actividades(dynamodbc)
insertar_intereses(dynamodbc)

print("===== OBTENER  UN REGISTRO DE CADA TABLA =====")
print("-"*50)
print(obtener_estudiante(dynamodbc, "Juan Pérez"))
print("-"*50)
print(obtener_actividad(dynamodbc, "Deporte", "2025-12-01"))
print("-"*50)
print(obtener_interes(dynamodbc, "Fútbol"))
print("-"*50)

print("===== ACTUALIZAR UN REGISTRO DE CADA TABLA =====")
actualizar_estudiante(dynamodbc, "Juan Pérez", {"edad": "26", "genero": "Masculino"})
actualizar_actividad(dynamodbc, "Deporte", "2025-12-01", {"duracion": "6 meses"})
actualizar_interes(dynamodbc, "Fútbol", {"descripcion": "Interés en deportes colectivos"})


print("===== ELIMINAR UN REGISTRO DE CADA TABLA =====")

eliminar_estudiante(dynamodbc, "Juan Pérez")
eliminar_actividad(dynamodbc, "Deporte", "2025-12-01")
eliminar_interes(dynamodbc, "Fútbol")

print("===== OBTENER TODOS LOS REGISTROS =====")
obtener_todos(dynamodbr)

print("===== OBTENER CONJUNTO REGISTROS FILTRADOS CON SCAN =====")
scan_filtrado(dynamodbr)

print("===== ELIMINACION CONDICIONAL =====")
eliminar_condicional_estudiante(dynamodbc, "Ana Pérez", "Alto")
eliminar_condicional_actividad(dynamodbc, "Arte", "2025-12-02", "3h")
eliminar_condicional_interes(dynamodbr, dynamodbc, "Programación")

print("===== PartiQL =====")
print(partiql_get_estudiante(dynamodbc, "Lucía García"))
print(partiql_get_actividad(dynamodbc, "Música"))
print(partiql_get_interes(dynamodbc, "Música"))