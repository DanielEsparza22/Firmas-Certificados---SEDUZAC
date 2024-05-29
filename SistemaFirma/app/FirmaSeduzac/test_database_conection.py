import os
import django
from django.db import connections

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FirmaSeduzac.settings")

django.setup()

from django.db import connection

def test_database_connection():
    try:
        cursor = connections['mariadb'].cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("Conexión a la base de datos MariaDB correcta. Res:", result)
    except Exception as e:
        print("Error al conectar a la base de datos MariaDB:", e)

def test_query():
    try:
        cursor = connections['mariadb'].cursor()
        cursor.execute("SELECT * FROM alumnos LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        if not rows:
            print("No se encontraron registros en la tabla ALUMNOS.")
    except Exception as e:
        print("Error al ejecutar la consulta:", e)
    finally:
        cursor.close()

def test_query_cambio():
    try:
        cursor = connections['mariadb'].cursor()
        cursor.execute("SELECT * FROM alumnos LIMIT 1")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        if not rows:
            print("No se encontraron registros en la tabla ALUMNOS.")
    except Exception as e:
        print("Error al ejecutar la consulta:", e)
    finally:
        cursor.close()


if __name__ == "__main__":
    test_database_connection()
    test_query_cambio()
    # test_query()
