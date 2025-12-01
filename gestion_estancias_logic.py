# Parte del contenido de este módulo, incluyendo la estructura base del CRUD,
# el manejo de conexiones con la base de datos y la sanitización de datos de entrada,
# fue generado y asistido mediante ChatGPT (OpenAI, versión GPT-5.1).
#
# El código fue posteriormente revisado, adaptado y ampliado por el estudiante
# para ajustarse al modelo del proyecto y asegurar su correcto funcionamiento
# dentro del sistema.

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
def read_estancias(filtro_medico=None):
    """
    Obtiene todas las estancias registradas.
    Trae también el nombre del médico y el tipo de procedimiento.
    Puede filtrar opcionalmente por nombre de médico.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            de.id_de_estancia,
            de.id_medico_responsable,
            emp.nombre AS nombre_medico,
            de.hora,
            de.id_procedimientos,
            proc.tipo AS tipo_procedimiento
        FROM de_estancia de
        LEFT JOIN empleado emp
            ON de.id_medico_responsable = emp.id_empleado
        LEFT JOIN procedimientos proc
            ON de.id_procedimientos = proc.id_procedimiento
        WHERE 1 = 1
        """

        valores = []

        # Filtro por nombre de médico (LIKE)
        if filtro_medico:
            query += " AND emp.nombre LIKE %s"
            valores.append(f"%{filtro_medico}%")

        query += " ORDER BY de.id_de_estancia DESC"

        cursor.execute(query, tuple(valores))
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
        UPDATE de_estancia
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

        query = "DELETE FROM de_estancia WHERE id_de_estancia = %s"
        cursor.execute(query, (id_de_estancia,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
