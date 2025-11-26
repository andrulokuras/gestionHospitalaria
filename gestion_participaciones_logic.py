import mysql.connector
from mysql.connector import errorcode
from db_connection import DB_CONFIG


# ----------------------------------------------------------------------
# FUNCIONES DE LECTURA (READ)
# ----------------------------------------------------------------------

def read_participaciones(filtro_tipo_intervencion=None, filtro_nombre_empleado=None):
    """Recupera todas las participaciones con info de empleado, tratamiento y paciente."""
    conn = None
    cursor = None
    participaciones = []
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            p.id_participacion,
            p.tipo_intervencion,
            p.fecha,
            p.rol,
            p.id_tratamiento,
            p.id_empleado,
            e.nombre AS nombre_empleado,
            t.tipo   AS tipo_tratamiento,
            pac.nombre_completo AS nombre_paciente
        FROM participacion p
        JOIN empleado    e   ON p.id_empleado    = e.id_empleado
        JOIN tratamiento t   ON p.id_tratamiento = t.id_tratamiento
        LEFT JOIN paciente pac ON t.id_paciente  = pac.id_paciente
        WHERE 1=1
        """
        valores = []

        # Filtro por tipo de intervención
        if filtro_tipo_intervencion:
            query += " AND p.tipo_intervencion LIKE %s"
            valores.append(f"%{filtro_tipo_intervencion}%")

        # Filtro por nombre de empleado
        if filtro_nombre_empleado:
            query += " AND e.nombre LIKE %s"
            valores.append(f"%{filtro_nombre_empleado}%")

        query += " ORDER BY p.id_participacion DESC"

        cursor.execute(query, tuple(valores))
        participaciones = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error al leer participaciones: {err}")
    except Exception as e:
        print(f"Error inesperado en read_participaciones: {e}")
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
    return participaciones


# ----------------------------------------------------------------------
# FUNCIONES DE CREACIÓN (CREATE)
# ----------------------------------------------------------------------

def create_participacion(tipo_intervencion, fecha, rol, id_tratamiento, id_empleado):
    """Inserta un nuevo registro de participación."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # No incluimos id_participacion ya que debe ser AUTO_INCREMENT
        query = """
        INSERT INTO participacion (tipo_intervencion, fecha, rol, id_tratamiento, id_empleado)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (tipo_intervencion, fecha, rol, id_tratamiento, id_empleado)
        cursor.execute(query, valores)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        # Devuelve el mensaje de error de la BD (útil para el flash en app.py)
        return str(err) 
    except Exception as e:
        return str(e)
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ----------------------------------------------------------------------
# FUNCIONES DE ACTUALIZACIÓN (UPDATE)
# ----------------------------------------------------------------------

def update_participacion(id_participacion, tipo_intervencion, fecha, rol, id_tratamiento, id_empleado):
    """Actualiza un registro de participación existente."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        UPDATE participacion
        SET tipo_intervencion = %s, fecha = %s, rol = %s, id_tratamiento = %s, id_empleado = %s
        WHERE id_participacion = %s
        """
        valores = (tipo_intervencion, fecha, rol, id_tratamiento, id_empleado, id_participacion)
        cursor.execute(query, valores)
        conn.commit()
        # Verificar si se actualizó algún registro
        return cursor.rowcount > 0 or True # Retornar True si la actualización es exitosa o si no se cambió nada
    except mysql.connector.Error as err:
        return str(err)
    except Exception as e:
        return str(e)
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ----------------------------------------------------------------------
# FUNCIONES DE ELIMINACIÓN (DELETE)
# ----------------------------------------------------------------------

def delete_participacion(id_participacion):
    """Elimina un registro de participación por su ID."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM participacion WHERE id_participacion = %s"
        cursor.execute(query, (id_participacion,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return str(err)
    except Exception as e:
        return str(e)
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected():
            conn.close()
