# Parte del contenido de este módulo, incluyendo la estructura base de las 
# funciones CRUD y el manejo de conexiones con la base de datos, fue generado 
# y asistido mediante ChatGPT (OpenAI, versión GPT-5.1).
#
# El código fue posteriormente revisado, adaptado y ampliado por el estudiante
# para ajustarse al funcionamiento requerido dentro del sistema y a la 
# administración de usuarios del proyecto.

import mysql.connector
from db_connection import DB_CONFIG


def create_usuario(username, password, rol, id_empleado=None):
    """
    Crea un nuevo usuario en la tabla USUARIO.
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
        print("Error en create_usuario:", err)
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def read_usuarios(filtro_username=None, filtro_rol=None):
    """
    Lee usuarios de la tabla USUARIO, con filtros opcionales.
    Hace LEFT JOIN con EMPLEADO para mostrar el nombre.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            u.id_usuario,
            u.username,
            u.rol,
            u.id_empleado,
            e.nombre AS nombre_empleado
        FROM usuario u
        LEFT JOIN empleado e ON u.id_empleado = e.id_empleado
        WHERE 1=1
        """
        valores = []

        if filtro_username:
            query += " AND u.username LIKE %s"
            valores.append(f"%{filtro_username}%")

        if filtro_rol:
            query += " AND u.rol = %s"
            valores.append(filtro_rol)

        query += " ORDER BY u.id_usuario DESC"

        cursor.execute(query, tuple(valores))
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print("Error en read_usuarios:", err)
        return []

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def update_usuario(id_usuario, username, password, rol, id_empleado=None):
    """
    Actualiza un usuario existente.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        UPDATE usuario
        SET username = %s,
            password = %s,
            rol = %s,
            id_empleado = %s
        WHERE id_usuario = %s
        """
        cursor.execute(query, (username, password, rol, id_empleado, id_usuario))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        print("Error en update_usuario:", err)
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def delete_usuario(id_usuario):
    """
    Elimina un usuario por id_usuario.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM usuario WHERE id_usuario = %s"
        cursor.execute(query, (id_usuario,))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        print("Error en delete_usuario:", err)
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
