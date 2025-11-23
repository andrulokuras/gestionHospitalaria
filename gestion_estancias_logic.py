import mysql.connector
from db_connection import DB_CONFIG 

# --- 1. CREAR ESTANCIA ---
def create_estancia(medico_responsable, hora, id_procedimientos):
    """
    Crea un nuevo registro en la tabla DE_ESTANCIA.
    medico_responsable: ID del médico responsable (FK a MEDICO/EMPLEADO)
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        INSERT INTO DE_ESTANCIA (id_medico_responsable, hora, id_procedimientos)
        VALUES (%s, %s, %s)
        """
        valores = (medico_responsable, hora, id_procedimientos)
        cursor.execute(query, valores)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# --- 2. LEER ESTANCIAS ---
def read_estancias():
    """
    Obtiene todas las estancias registradas.
    Alias 'medico_responsable' para que coincida con el template.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            id_de_estancia,
            id_medico_responsable AS medico_responsable,
            hora,
            id_procedimientos
        FROM DE_ESTANCIA
        ORDER BY id_de_estancia DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al leer estancias: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# --- 3. ACTUALIZAR ESTANCIA ---
def update_estancia(id_de_estancia, medico_responsable, hora, id_procedimientos):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        UPDATE DE_ESTANCIA
        SET id_medico_responsable = %s,
            hora = %s,
            id_procedimientos = %s
        WHERE id_de_estancia = %s
        """
        valores = (medico_responsable, hora, id_procedimientos, id_de_estancia)
        cursor.execute(query, valores)
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# --- 4. ELIMINAR ESTANCIA ---
def delete_estancia(id_de_estancia):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM DE_ESTANCIA WHERE id_de_estancia = %s"
        cursor.execute(query, (id_de_estancia,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
