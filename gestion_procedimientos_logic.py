# Parte del contenido de este módulo, incluyendo la estructura base del CRUD,
# el manejo de conexiones con la base de datos y la sanitización de datos de entrada,
# fue generado y asistido mediante ChatGPT (OpenAI, versión GPT-5.1).
#
# El código fue posteriormente revisado, adaptado y ampliado por el estudiante
# para ajustarse al modelo del proyecto y asegurar su correcto funcionamiento
# dentro del sistema.

import mysql.connector
# Importamos la configuración de la base de datos
from db_connection import DB_CONFIG 

# --- 1. CREAR (CREATE) ---
def create_procedimiento(fecha, tipo, resultados):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        INSERT INTO procedimientos (fecha, tipo, resultados)
        VALUES (%s, %s, %s)
        """
        valores = (fecha, tipo, resultados)
        cursor.execute(query, valores)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 2. LEER (READ) ---
def read_procedimientos(filtro_tipo=None):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True) 
        
        query = """
        SELECT 
            id_procedimiento, 
            DATE_FORMAT(fecha, '%Y-%m-%d') AS fecha,
            tipo, 
            resultados 
        FROM procedimientos
        WHERE 1=1
        """
        valores = []

        if filtro_tipo:
            query += " AND tipo LIKE %s"
            valores.append(f"%{filtro_tipo}%")

        query += " ORDER BY fecha DESC"

        cursor.execute(query, tuple(valores))
        return cursor.fetchall()
        
    except mysql.connector.Error as err:
        print(f"Error de lectura de procedimientos: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# --- 3. ACTUALIZAR (UPDATE) ---
def update_procedimiento(id_procedimiento, fecha, tipo, resultados):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        UPDATE procedimientos 
        SET fecha = %s, tipo = %s, resultados = %s
        WHERE id_procedimiento = %s
        """
        valores = (fecha, tipo, resultados, id_procedimiento)
        cursor.execute(query, valores)
        conn.commit()
        # Verificar si la actualización afectó alguna fila
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 4. ELIMINAR (DELETE) ---
def delete_procedimiento(id_procedimiento):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "DELETE FROM procedimientos WHERE id_procedimiento = %s"
        
        cursor.execute(query, (id_procedimiento,))
        conn.commit()
        # Verificar si se eliminó alguna fila
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
