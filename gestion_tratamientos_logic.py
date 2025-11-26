import mysql.connector
from db_connection import DB_CONFIG


# -----------------------------------------
# LEER TRATAMIENTOS
# -----------------------------------------
def read_tratamientos(filtro_nombre_paciente=None):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # --- CORRECCIÓN AQUÍ ---
        # Cambié 't.id_de_tratamiento' por 't.id_procedimiento'
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
            t.id_procedimiento 
        FROM tratamiento t
        LEFT JOIN paciente p ON t.id_paciente = p.id_paciente
        LEFT JOIN area_especifica a ON t.id_area_especifica = a.id_area_especifica
        WHERE 1 = 1
        """
        valores = []

        if filtro_nombre_paciente:
            query += " AND p.nombre_completo LIKE %s"
            valores.append(f"%{filtro_nombre_paciente}%")

        query += " ORDER BY t.id_tratamiento DESC"

        cursor.execute(query, tuple(valores))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        # Revisa tu terminal/consola, aquí debe estar apareciendo el error
        print(f"Error al leer tratamientos: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# -----------------------------------------
# CREAR TRATAMIENTO
# -----------------------------------------
def create_tratamiento(id_paciente, tipo, fecha_inicio, estado_actual,
                       id_area_especifica, id_procedimiento):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
            INSERT INTO tratamiento
            (id_paciente, tipo, fecha_inicio, estado_actual,
             id_area_especifica, id_procedimiento)
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        cursor.execute(query, (
            id_paciente,
            tipo,
            fecha_inicio,
            estado_actual,
            id_area_especifica,
            id_procedimiento if id_procedimiento else None
        ))

        conn.commit()

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as err:
        return str(err)


# -----------------------------------------
# ACTUALIZAR TRATAMIENTO
# -----------------------------------------
def update_tratamiento(id_tratamiento, id_paciente, tipo, fecha_inicio,
                       estado_actual, id_area_especifica, id_procedimiento):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
            UPDATE tratamiento
            SET id_paciente = %s,
                tipo = %s,
                fecha_inicio = %s,
                estado_actual = %s,
                id_area_especifica = %s,
                id_procedimiento = %s
            WHERE id_tratamiento = %s;
        """

        cursor.execute(query, (
            id_paciente,
            tipo,
            fecha_inicio,
            estado_actual,
            id_area_especifica,
            id_procedimiento if id_procedimiento else None,
            id_tratamiento
        ))

        conn.commit()

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as err:
        return str(err)


# -----------------------------------------
# ELIMINAR TRATAMIENTO
# -----------------------------------------
def delete_tratamiento(id_tratamiento):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tratamiento WHERE id_tratamiento = %s;", (id_tratamiento,))
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as err:
        return str(err)
