# gestion_tratamientos_logic.py
import mysql.connector
from db_connection import DB_CONFIG

# 1. CREATE
def create_tratamiento(id_paciente, tipo, fecha_inicio, estado_actual, id_area_especifica, id_de_tratamiento=None):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        INSERT INTO TRATAMIENTO (id_paciente, tipo, fecha_inicio, estado_actual, id_area_especifica, id_de_tratamiento)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (id_paciente, tipo, fecha_inicio, estado_actual, id_area_especifica, id_de_tratamiento)
        cursor.execute(query, valores)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# 2. READ
def read_tratamientos():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Traemos también nombre del paciente y nombre del área
        query = """
        SELECT 
            t.id_tratamiento,
            t.id_paciente,
            p.nombre_completo AS nombre_paciente,
            t.tipo,
            t.fecha_inicio,
            t.estado_actual,
            t.id_area_especifica,
            a.nombre AS nombre_area,
            t.id_de_tratamiento
        FROM TRATAMIENTO t
        LEFT JOIN PACIENTE p ON t.id_paciente = p.id_paciente
        LEFT JOIN AREA_ESPECIFICA a ON t.id_area_especifica = a.id_area_especifica
        ORDER BY t.id_tratamiento DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al leer tratamientos: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# 3. UPDATE
def update_tratamiento(id_tratamiento, id_paciente, tipo, fecha_inicio, estado_actual, id_area_especifica, id_de_tratamiento=None):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        UPDATE TRATAMIENTO
        SET id_paciente = %s,
            tipo = %s,
            fecha_inicio = %s,
            estado_actual = %s,
            id_area_especifica = %s,
            id_de_tratamiento = %s
        WHERE id_tratamiento = %s
        """
        valores = (id_paciente, tipo, fecha_inicio, estado_actual, id_area_especifica, id_de_tratamiento, id_tratamiento)
        cursor.execute(query, valores)
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# 4. DELETE
def delete_tratamiento(id_tratamiento):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM TRATAMIENTO WHERE id_tratamiento = %s"
        cursor.execute(query, (id_tratamiento,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
