# Parte del contenido de este módulo, incluyendo la estructura base del CRUD,
# el manejo de conexiones con la base de datos y la sanitización de datos de entrada,
# fue generado y asistido mediante ChatGPT (OpenAI, versión GPT-5.1).
#
# El código fue posteriormente revisado, adaptado y ampliado por el estudiante
# para ajustarse al modelo del proyecto y asegurar su correcto funcionamiento
# dentro del sistema.

import mysql.connector
from db_connection import DB_CONFIG 

# --- 1. CREAR ASIGNACIÓN ---
def create_asignacion(id_empleado, id_area_especifica, asignacion, turno_datetime):
    """
    Registra la asignación de un empleado a un área específica, incluyendo el turno exacto.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        INSERT INTO asignacion_turno (id_empleado, id_area_especifica, asignacion, turno_datetime)
        VALUES (%s, %s, %s, %s)
        """
        valores = (id_empleado, id_area_especifica, asignacion, turno_datetime)
        cursor.execute(query, valores)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 2. LEER ASIGNACIONES (Con JOINS) ---
def read_asignaciones(filtro_nombre_medico=None):
    """
    Lee todas las asignaciones con los nombres del empleado y el área.
    Permite filtrar por nombre de empleado (médico/enfermera/etc.).
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            AT.id_asignacion, 
            AT.id_empleado, 
            AT.id_area_especifica, 
            AT.turno_datetime, 
            AT.asignacion,
            
            E.nombre AS nombre_empleado,
            AE.nombre AS nombre_area
        FROM asignacion_turno AT
        LEFT JOIN empleado E ON AT.id_empleado = E.id_empleado
        LEFT JOIN area_especifica AE ON AT.id_area_especifica = AE.id_area_especifica
        WHERE 1=1
        """
        valores = []

        if filtro_nombre_medico:
            query += " AND E.nombre LIKE %s"
            valores.append(f"%{filtro_nombre_medico}%")

        query += " ORDER BY AT.id_asignacion DESC"

        cursor.execute(query, tuple(valores))
        return cursor.fetchall()
        
    except mysql.connector.Error as err:
        print(f"Error de lectura de asignaciones: {err}") 
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


            
# --- 3. ACTUALIZAR ASIGNACIÓN ---
def update_asignacion(id_asignacion, id_empleado, id_area_especifica, asignacion, turno_datetime):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        UPDATE asignacion_turno 
        SET id_empleado = %s, id_area_especifica = %s, asignacion = %s, turno_datetime = %s
        WHERE id_asignacion = %s
        """
        valores = (id_empleado, id_area_especifica, asignacion, turno_datetime, id_asignacion)
        cursor.execute(query, valores)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 4. ELIMINAR ASIGNACIÓN ---
def delete_asignacion(id_asignacion):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "DELETE FROM asignacion_turno WHERE id_asignacion = %s"
        cursor.execute(query, (id_asignacion,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
