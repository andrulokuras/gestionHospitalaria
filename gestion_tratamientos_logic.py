import mysql.connector
from db_connection import DB_CONFIG


# -----------------------------------------
# LEER TRATAMIENTOS
# -----------------------------------------
def read_tratamientos():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT t.id_tratamiento,
                   t.id_paciente,
                   t.tipo,
                   t.fecha_inicio,
                   t.estado_actual,
                   t.id_area_especifica,
                   t.id_procedimiento,
                   p.nombre_completo AS nombre_paciente,
                   a.nombre AS nombre_area
            FROM tratamiento t
            LEFT JOIN paciente p ON p.id_paciente = t.id_paciente
            LEFT JOIN area_especifica a ON a.id_area_especifica = t.id_area_especifica
            ORDER BY t.id_tratamiento DESC;
        """

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except mysql.connector.Error as err:
        return str(err)


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
