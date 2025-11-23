# gestion_pacientes_logic.py
import mysql.connector
# Asegúrate de que este archivo y la variable DB_CONFIG existan
from db_connection import DB_CONFIG

# --- 1. CREAR (CREATE) ---
# Usamos nombre_completo y domicilio para coincidir con tu esquema de BD
def create_paciente(nombre_completo, fecha_nacimiento, genero, domicilio, telefono, seguro_medico):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        INSERT INTO PACIENTE (nombre_completo, fecha_nacimiento, genero, domicilio, telefono, seguro_medico)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # El orden de los datos debe coincidir con el orden de las columnas en la query
        datos = (nombre_completo, fecha_nacimiento, genero, domicilio, telefono, seguro_medico)
        cursor.execute(query, datos)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 2. LEER (READ) ---
# Esta función es la que estaba causando el ImportError
def read_pacientes():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True) 
        query = "SELECT * FROM PACIENTE ORDER BY id_paciente DESC"
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        # En caso de error, devuelve una lista vacía para evitar fallos
        print(f"Error de BD al leer pacientes: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- 3. ACTUALIZAR (UPDATE) ---
# Usamos nombre_completo y domicilio
def update_paciente(id_paciente, nombre_completo, fecha_nacimiento, genero, domicilio, telefono, seguro_medico):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        UPDATE PACIENTE 
        SET nombre_completo = %s, fecha_nacimiento = %s, genero = %s, domicilio = %s, 
            telefono = %s, seguro_medico = %s
        WHERE id_paciente = %s
        """
        valores = (nombre_completo, fecha_nacimiento, genero, domicilio, telefono, seguro_medico, id_paciente)
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
def delete_paciente(id_paciente):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "DELETE FROM PACIENTE WHERE id_paciente = %s"
        cursor.execute(query, (id_paciente,))
        conn.commit()
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()