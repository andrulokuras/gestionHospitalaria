import mysql.connector
from db_connection import DB_CONFIG 

# --- 1. CREAR (CREATE) ---
def create_area(tipo, nombre, ubicacion):
    """
    Registra una nueva área específica en la base de datos.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        INSERT INTO AREA_ESPECIFICA (tipo, nombre, ubicacion)
        VALUES (%s, %s, %s)
        """
        valores = (tipo, nombre, ubicacion)
        cursor.execute(query, valores)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        # Se devuelve el error para ser mostrado en Flask
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 2. LEER (READ) ---
def read_areas():
    """
    Lee todos los registros de áreas específicas de la base de datos.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True) 
        
        query = "SELECT * FROM AREA_ESPECIFICA ORDER BY id_area_especifica DESC"
        cursor.execute(query)
        # Devolvemos la lista de áreas (como diccionarios)
        return cursor.fetchall()
        
    except mysql.connector.Error as err:
        print(f"Error de lectura de áreas: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 3. ACTUALIZAR (UPDATE) ---
def update_area(id_area_especifica, tipo, nombre, ubicacion):
    """
    Actualiza la información de un área específica existente.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        UPDATE AREA_ESPECIFICA 
        SET tipo = %s, nombre = %s, ubicacion = %s
        WHERE id_area_especifica = %s
        """
        valores = (tipo, nombre, ubicacion, id_area_especifica)
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
def delete_area(id_area_especifica):
    """
    Elimina un área específica por su ID.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "DELETE FROM AREA_ESPECIFICA WHERE id_area_especifica = %s"
        
        cursor.execute(query, (id_area_especifica,))
        conn.commit()
        # Verificar si se eliminó alguna fila
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()