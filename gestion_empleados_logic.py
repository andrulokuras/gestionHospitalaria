import mysql.connector
from db_connection import DB_CONFIG


# --- 1. CREAR EMPLEADO ---
def create_empleado(nombre, puesto, fecha_contratacion, tipo):
    """
    Crea un nuevo registro en la tabla EMPLEADO.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        INSERT INTO EMPLEADO (nombre, puesto_especialidad, fecha_contratacion, tipo)
        VALUES (%s, %s, %s, %s)
        """
        datos_empleado = (nombre, puesto, fecha_contratacion, tipo)
        cursor.execute(query, datos_empleado)
        conn.commit()
        return True

    except mysql.connector.Error as err:
        # Regresa el texto del error para mostrarlo con flash()
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# --- 2. LEER EMPLEADOS ---
def read_empleados(id_empleado=None):
    """
    Obtiene todos los empleados (o uno en particular si se da id_empleado).
    Regresa una lista de diccionarios para usarse directo en Jinja.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        if id_empleado is not None:
            query = "SELECT * FROM EMPLEADO WHERE id_empleado = %s"
            cursor.execute(query, (id_empleado,))
            return cursor.fetchone()
        else:
            query = "SELECT * FROM EMPLEADO ORDER BY id_empleado DESC"
            cursor.execute(query)
            return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error de lectura de empleados: {err}")
        return []

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# --- 3. ACTUALIZAR EMPLEADO ---
def update_empleado(id_empleado, nombre, puesto, fecha_contratacion, tipo):
    """
    Actualiza los datos de un empleado existente.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        UPDATE EMPLEADO
        SET nombre = %s,
            puesto_especialidad = %s,
            fecha_contratacion = %s,
            tipo = %s
        WHERE id_empleado = %s
        """
        valores = (nombre, puesto, fecha_contratacion, tipo, id_empleado)
        cursor.execute(query, valores)
        conn.commit()
        return cursor.rowcount > 0

    except mysql.connector.Error as err:
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# --- 4. ELIMINAR EMPLEADO ---
def delete_empleado(id_empleado):
    """
    Elimina un empleado por ID.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM EMPLEADO WHERE id_empleado = %s"
        cursor.execute(query, (id_empleado,))
        conn.commit()
        return cursor.rowcount > 0

    except mysql.connector.Error as err:
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
