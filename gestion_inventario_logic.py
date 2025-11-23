import mysql.connector
# Importa la configuración de la conexión (asegúrate de que este archivo exista)
from db_connection import DB_CONFIG 

# ============================================
# CREAR ARTÍCULO DE INVENTARIO
# ============================================
def create_articulo(nombre, tipo, stock_actual, stock_minimo, ubicacion, numero_lote_serie, fecha_vencimiento, fecha_mantenimiento, descripcion):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        INSERT INTO INVENTARIO (
            nombre, tipo, stock_actual, stock_minimo, ubicacion, 
            numero_lote_serie, fecha_vencimiento, fecha_mantenimiento, descripcion
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Manejo de valores nulos: si las cadenas están vacías, se pasan como None a la base de datos
        fv = fecha_vencimiento if fecha_vencimiento else None
        fm = fecha_mantenimiento if fecha_mantenimiento else None
        
        cursor.execute(query, (
            nombre, tipo, stock_actual, stock_minimo, ubicacion, 
            numero_lote_serie, fv, fm, descripcion
        ))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        # Devuelve el error de la base de datos como una cadena
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ============================================
# LEER TODO EL INVENTARIO
# ============================================
def read_inventario():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True) # Devuelve los resultados como diccionarios

        query = "SELECT * FROM INVENTARIO ORDER BY nombre ASC"

        cursor.execute(query)
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print("Error leyendo el inventario:", err)
        # En caso de error, devuelve una lista vacía
        return []

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ============================================
# ACTUALIZAR ARTÍCULO DE INVENTARIO
# ============================================
def update_articulo(id_articulo, nombre, tipo, stock_actual, stock_minimo, ubicacion, numero_lote_serie, fecha_vencimiento, fecha_mantenimiento, descripcion):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        UPDATE INVENTARIO 
        SET nombre = %s, tipo = %s, stock_actual = %s, stock_minimo = %s, 
            ubicacion = %s, numero_lote_serie = %s, fecha_vencimiento = %s, 
            fecha_mantenimiento = %s, descripcion = %s
        WHERE id_articulo = %s
        """
        
        fv = fecha_vencimiento if fecha_vencimiento else None
        fm = fecha_mantenimiento if fecha_mantenimiento else None

        cursor.execute(query, (
            nombre, tipo, stock_actual, stock_minimo, ubicacion, 
            numero_lote_serie, fv, fm, descripcion, id_articulo
        ))
        conn.commit()
        # Devuelve True si se actualizó al menos una fila
        return cursor.rowcount > 0

    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ============================================
# ELIMINAR ARTÍCULO DE INVENTARIO
# ============================================
def delete_articulo(id_articulo):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = "DELETE FROM INVENTARIO WHERE id_articulo = %s"
        cursor.execute(query, (id_articulo,))
        conn.commit()
        # Devuelve True si se eliminó al menos una fila
        return cursor.rowcount > 0

    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        return str(err)

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
