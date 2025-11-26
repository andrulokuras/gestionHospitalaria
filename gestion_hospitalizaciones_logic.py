import mysql.connector
from db_connection import DB_CONFIG


# ============================================
# CREAR HOSPITALIZACIÓN
# ============================================
def create_hospitalizacion(fecha_ingreso, fecha_egreso, motivo, habitacion, id_paciente, id_estancia, id_area):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        INSERT INTO hospitalizaciones
        (fecha_ingreso, fecha_egreso, motivo_ingreso, habitacion, id_paciente, id_de_estancia, id_area_especifica)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (fecha_ingreso, fecha_egreso, motivo, habitacion, id_paciente, id_estancia, id_area))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# ============================================
# LEER HOSPITALIZACIONES (con filtro opcional por nombre de paciente)
# ============================================
def read_hospitalizaciones(filtro_nombre=None):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            H.*,
            P.nombre_completo AS nombre_paciente,
            A.nombre AS nombre_area,
            E.id_de_estancia
        FROM hospitalizaciones H
        LEFT JOIN paciente P
            ON H.id_paciente = P.id_paciente
        LEFT JOIN area_especifica A
            ON H.id_area_especifica = A.id_area_especifica
        LEFT JOIN de_estancia E
            ON H.id_de_estancia = E.id_de_estancia
        WHERE 1 = 1
        """

        valores = []

        # Si viene un nombre para filtrar, agregamos condición
        if filtro_nombre:
            query += " AND P.nombre_completo LIKE %s"
            valores.append(f"%{filtro_nombre}%")

        query += " ORDER BY H.id_hospitalizaciones DESC"

        cursor.execute(query, tuple(valores))
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print("Error leyendo hospitalizaciones:", err)
        return []

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# ============================================
# ACTUALIZAR HOSPITALIZACIÓN
# ============================================
def update_hospitalizacion(id_hosp, fecha_ingreso, fecha_egreso, motivo, habitacion, id_paciente, id_estancia, id_area):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        UPDATE hospitalizaciones
        SET fecha_ingreso = %s,
            fecha_egreso = %s,
            motivo_ingreso = %s,
            habitacion = %s,
            id_paciente = %s,
            id_de_estancia = %s,
            id_area_especifica = %s
        WHERE id_hospitalizaciones = %s
        """

        cursor.execute(query, (fecha_ingreso, fecha_egreso, motivo, habitacion, id_paciente, id_estancia, id_area, id_hosp))
        conn.commit()
        return cursor.rowcount > 0

    except mysql.connector.Error as err:
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# ============================================
# ELIMINAR HOSPITALIZACIÓN
# ============================================
def delete_hospitalizacion(id_hosp):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hospitalizaciones WHERE id_hospitalizaciones = %s", (id_hosp,))
        conn.commit()
        return cursor.rowcount > 0

    except mysql.connector.Error as err:
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
