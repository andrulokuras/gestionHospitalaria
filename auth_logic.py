import mysql.connector
from db_connection import DB_CONFIG


def validar_login(username, password):
    """
    Valida usuario y contraseña contra la tabla USUARIO.
    Regresa un dict con los datos del usuario si es válido, o None si no.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT * FROM usuario
        WHERE username = %s AND password = %s
        """
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        return user

    except mysql.connector.Error as err:
        print("Error en validar_login:", err)
        return None

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def crear_usuario(username, password, rol, id_empleado=None):
    """
    Crea un usuario nuevo en la tabla USUARIO.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        INSERT INTO usuario (username, password, rol, id_empleado)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (username, password, rol, id_empleado))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        print("Error en crear_usuario:", err)
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
