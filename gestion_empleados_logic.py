import mysql.connector
from db_connection import DB_CONFIG

# --- 1. CREAR (CREATE) ---
def create_empleado(nombre, puesto, fecha_contratacion):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        INSERT INTO EMPLEADO (nombre, puesto_especialidad, fecha_contratacion)
        VALUES (%s, %s, %s)
        """
        datos_empleado = (nombre, puesto, fecha_contratacion)
        cursor.execute(query, datos_empleado)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 2. LEER (READ) ---
def read_empleados(id_empleado=None):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True) 
        
        query = "SELECT * FROM EMPLEADO ORDER BY id_empleado DESC"
        cursor.execute(query)
        return cursor.fetchall()
        
    except mysql.connector.Error as err:
        print(f"Error de lectura: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 3. ACTUALIZAR (UPDATE) ---
def update_empleado(id_empleado, nombre, puesto, fecha_contratacion):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        UPDATE EMPLEADO 
        SET nombre = %s, puesto_especialidad = %s, fecha_contratacion = %s
        WHERE id_empleado = %s
        """
        valores = (nombre, puesto, fecha_contratacion, id_empleado)
        cursor.execute(query, valores)
        conn.commit()
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 4. ELIMINAR (DELETE) ---
def delete_empleado(id_empleado):
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