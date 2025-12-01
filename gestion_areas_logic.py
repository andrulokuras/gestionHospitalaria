# Parte del contenido de este módulo, incluyendo la estructura base del CRUD,
# el manejo de conexiones con la base de datos y la sanitización de datos de entrada,
# fue generado y asistido mediante ChatGPT (OpenAI, versión GPT-5.1).
#
# El código fue posteriormente revisado, adaptado y ampliado por el estudiante
# para ajustarse al modelo del proyecto y asegurar su correcto funcionamiento
# dentro del sistema.

import mysql.connector
from db_connection import DB_CONFIG 

# --- 1. CREAR (CREATE) ---
def create_area(tipo, nombre, ubicacion, id_empleado, recursos_clave): # Agrega los nuevos parámetros
    """
    Registra una nueva área específica en la base de datos.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        INSERT INTO area_especifica (tipo, nombre, ubicacion, id_empleado, recursos_clave)
        VALUES (%s, %s, %s, %s, %s)
        """ # Agrega las nuevas columnas
        valores = (tipo, nombre, ubicacion, id_empleado, recursos_clave) # Agrega los nuevos valores
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
def read_areas(filtro_tipo=None, filtro_nombre=None):
    """
    Lee todos los registros de áreas, incluyendo info de Jefatura.
    Permite filtrar por tipo de área y por nombre.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            AE.*,
            E.nombre AS nombre_jefe,
            E.tipo   AS puesto_jefe
        FROM area_especifica AE
        LEFT JOIN empleado E ON AE.id_empleado = E.id_empleado
        WHERE 1=1
        """
        valores = []

        # Filtro por tipo de área
        if filtro_tipo:
            query += " AND AE.tipo = %s"
            valores.append(filtro_tipo)

        # Filtro por nombre de área (LIKE)
        if filtro_nombre:
            query += " AND AE.nombre LIKE %s"
            valores.append(f"%{filtro_nombre}%")

        query += " ORDER BY AE.id_area_especifica DESC"

        cursor.execute(query, tuple(valores))
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error de lectura de áreas: {err}")
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 3. ACTUALIZAR (UPDATE) ---
def update_area(id_area_especifica, tipo, nombre, ubicacion, id_empleado, recursos_clave):
    """
    Actualiza la información de un área específica existente.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        UPDATE area_especifica 
        SET tipo = %s, nombre = %s, ubicacion = %s, id_empleado = %s, recursos_clave = %s
        WHERE id_area_especifica = %s
        """
        # 🔑 CORRECCIÓN CLAVE AQUÍ: La tupla debe tener 6 valores, incluyendo los nuevos campos y el ID al final.
        valores = (tipo, nombre, ubicacion, id_empleado, recursos_clave, id_area_especifica) 
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
