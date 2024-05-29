from django.db import connection, connections

def test_consulta_datos():
    with connections['mariadb'].cursor() as cursor:
        cursor.execute("SELECT * FROM alumnos LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            print(row)