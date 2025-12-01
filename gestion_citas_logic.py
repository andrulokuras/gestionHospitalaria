# Parte del contenido de este módulo, incluyendo la estructura base del CRUD,
# el manejo de conexiones con la base de datos y la sanitización de datos de entrada,
# fue generado y asistido mediante ChatGPT (OpenAI, versión GPT-5.1).
#
# El código fue posteriormente revisado, adaptado y ampliado por el estudiante
# para ajustarse al modelo del proyecto y asegurar su correcto funcionamiento
# dentro del sistema.

import mysql.connector
from db_connection import DB_CONFIG

# -----------------------------------------------------------------------------
# FUNCIÓN AUXILIAR: VALIDAR MÉDICO
# -----------------------------------------------------------------------------
def es_medico(cursor, id_empleado):
    """
    Verifica si el ID dado existe en la tabla empleado y si su tipo es 'medico'.
    Retorna (True, None) si es válido.
    Retorna (False, Mensaje de error) si no lo es.
    """
    query_check = "SELECT nombre, tipo FROM empleado WHERE id_empleado = %s"
    cursor.execute(query_check, (id_empleado,))
    resultado = cursor.fetchone()

    if not resultado:
        return False, f"Error: El empleado con ID {id_empleado} no existe."
    
    # Ajusta 'medico' según cómo lo tengas en tu BD (puede ser 'Medico', 'médico', etc.)
    tipo_empleado = resultado['tipo'] if isinstance(resultado, dict) else resultado[1]
    
    if tipo_empleado.lower() != 'medico':
        return False, f"Error: El empleado '{resultado[0]}' (ID {id_empleado}) no es médico. Es: {tipo_empleado}."

    return True, None

# -----------------------------------------------------------------------------
# 1. CREATE
# -----------------------------------------------------------------------------
def create_cita(id_paciente, id_empleado, id_area_especifica, fecha_hora_inicio, duracion_minutos, motivo_consulta, estado):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # --- VALIDACIÓN: ¿Es médico? ---
        es_valido, mensaje_error = es_medico(cursor, id_empleado)
        if not es_valido:
            return mensaje_error
        # -------------------------------

        query = """
        INSERT INTO citas (id_paciente, id_empleado, id_area_especifica, fecha_hora_inicio, duracion_minutos, motivo_consulta, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (id_paciente, id_empleado, id_area_especifica, fecha_hora_inicio, duracion_minutos, motivo_consulta, estado)
        cursor.execute(query, valores)
        conn.commit()
        return True

    except mysql.connector.Error as err:
        return f"Error SQL: {err}"
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# -----------------------------------------------------------------------------
# 2. READ
# -----------------------------------------------------------------------------
def read_citas(filtro_estado=None):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            c.id_cita,
            c.id_paciente,
            p.nombre_completo AS nombre_paciente,
            c.id_empleado,
            e.nombre AS nombre_medico,
            c.id_area_especifica,
            a.nombre AS nombre_area,
            c.fecha_hora_inicio,
            c.duracion_minutos,
            c.motivo_consulta,
            c.estado
        FROM citas c
        LEFT JOIN paciente p ON c.id_paciente = p.id_paciente
        LEFT JOIN empleado e ON c.id_empleado = e.id_empleado
        LEFT JOIN area_especifica a ON c.id_area_especifica = a.id_area_especifica
        WHERE 1=1
        """

        valores = []

        # Si viene un estado (y no es "Todas"), filtramos
        if filtro_estado and filtro_estado.lower() != 'todas':
            query += " AND c.estado = %s"
            valores.append(filtro_estado)

        query += " ORDER BY c.fecha_hora_inicio DESC"

        cursor.execute(query, tuple(valores))
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error al leer citas: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# -----------------------------------------------------------------------------
# 3. UPDATE
# -----------------------------------------------------------------------------
def update_cita(id_cita, id_paciente, id_empleado, id_area_especifica, fecha_hora_inicio, duracion_minutos, motivo_consulta, estado):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # --- VALIDACIÓN: ¿Es médico? ---
        # Validamos también al editar, por si intentan asignar la cita a una enfermera por error
        es_valido, mensaje_error = es_medico(cursor, id_empleado)
        if not es_valido:
            return mensaje_error
        # -------------------------------

        query = """
        UPDATE citas
        SET id_paciente = %s,
            id_empleado = %s,
            id_area_especifica = %s,
            fecha_hora_inicio = %s,
            duracion_minutos = %s,
            motivo_consulta = %s,
            estado = %s
        WHERE id_cita = %s
        """
        valores = (id_paciente, id_empleado, id_area_especifica, fecha_hora_inicio, duracion_minutos, motivo_consulta, estado, id_cita)
        cursor.execute(query, valores)
        conn.commit()
        
        if cursor.rowcount == 0:
            return "No se encontró la cita o no hubo cambios."
            
        return True

    except mysql.connector.Error as err:
        return f"Error SQL: {err}"
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# -----------------------------------------------------------------------------
# 4. DELETE
# -----------------------------------------------------------------------------
def delete_cita(id_cita):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM citas WHERE id_cita = %s"
        cursor.execute(query, (id_cita,))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        return f"Error SQL: {err}"
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
