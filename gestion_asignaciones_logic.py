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
        INSERT INTO ASIGNACION_TURNO (id_empleado, id_area_especifica, asignacion, turno_datetime)
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
def read_asignaciones():
    """
    Lee todas las asignaciones con los nombres del empleado y el área de la tabla ASIGNACION_TURNO.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True) # Siempre usar dictionary=True
        
        # 🔑 CONSULTA CORREGIDA: Hacemos JOINs a las tablas EMPLEADO y AREA_ESPECIFICA
        query = """
        SELECT 
            AT.id_asignacion, 
            AT.id_empleado, 
            AT.id_area_especifica, 
            AT.turno_datetime, 
            AT.asignacion,
            
            E.nombre AS nombre_empleado,         -- Alias para el nombre del empleado
            AE.nombre AS nombre_area             -- Alias para el nombre del área
            
        FROM ASIGNACION_TURNO AT
        LEFT JOIN EMPLEADO E ON AT.id_empleado = E.id_empleado
        LEFT JOIN AREA_ESPECIFICA AE ON AT.id_area_especifica = AE.id_area_especifica
        ORDER BY AT.id_asignacion DESC
        """
        
        cursor.execute(query)
        return cursor.fetchall()
        
    except mysql.connector.Error as err:
        print(f"Error de lectura de asignaciones: {err}") 
        # Crucial: Devolver una lista vacía en caso de error para evitar fallos de Jinja2
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
        UPDATE ASIGNACION_TURNO 
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
        query = "DELETE FROM ASIGNACION_TURNO WHERE id_asignacion = %s"
        cursor.execute(query, (id_asignacion,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()