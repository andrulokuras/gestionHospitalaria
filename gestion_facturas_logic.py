import mysql.connector
from mysql.connector import errorcode
from db_connection import DB_CONFIG

# ----------------------------------------------------------------------
# FACTURAS
# ----------------------------------------------------------------------

def create_factura(
    id_paciente,
    fecha_emision,
    fecha_vencimiento=None,
    estado="Pendiente",
    metodo_pago_preferido=None,
    observaciones=None,
    total_neto=0.0,
):
    """
    Crea una factura en la tabla FACTURA.
    El parámetro total_neto es opcional, por defecto 0.0
    para ser compatible con la vista actual.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
            INSERT INTO FACTURA (
                id_paciente,
                fecha_emision,
                fecha_vencimiento,
                estado,
                total_neto,
                metodo_pago_preferido,
                observaciones
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            id_paciente,
            fecha_emision,
            fecha_vencimiento,
            estado,
            total_neto,
            metodo_pago_preferido,
            observaciones,
        )
        cursor.execute(query, valores)
        conn.commit()
        return True

    except mysql.connector.Error as err:
        return str(err)
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def read_facturas():
    """
    Lee TODAS las facturas y, para cada una, calcula:
      - total_pagado = suma de pagos en tabla PAGO
      - saldo = total_neto - total_pagado (si total_neto <= 0, saldo = 0)
    Devuelve una lista de diccionarios lista para usar en facturas.html
    """
    conn = None
    cursor = None
    facturas = []

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                id_factura,
                id_paciente,
                fecha_emision,
                fecha_vencimiento,
                estado,
                metodo_pago_preferido,
                observaciones,
                total_neto
            FROM FACTURA
            ORDER BY id_factura DESC
        """
        cursor.execute(query)
        facturas = cursor.fetchall()

        # Para cada factura, sumar pagos y calcular saldo
        for f in facturas:
            fid = f["id_factura"]
            pagos = read_pagos_por_factura(fid)

            total_pagado = sum(float(p["monto"]) for p in pagos) if pagos else 0.0
            total_neto = float(f.get("total_neto") or 0.0)

            # Guardamos estos campos extras para mostrarlos en el template
            f["total_pagado"] = total_pagado

            if total_neto > 0:
                f["saldo"] = total_neto - total_pagado
            else:
                # Si no estamos manejando aún el total de la factura,
                # dejamos el saldo en 0 para que no salga negativo.
                f["saldo"] = 0.0

    except mysql.connector.Error as err:
        print(f"Error al leer facturas: {err}")
    except Exception as e:
        print(f"Error inesperado en read_facturas: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return facturas


def delete_factura(id_factura):
    """
    Elimina una factura. (OJO: asumimos que primero se eliminan pagos
    dependientes si la FK no está en ON DELETE CASCADE).
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Primero eliminamos pagos asociados
        cursor.execute("DELETE FROM PAGO WHERE id_factura = %s", (id_factura,))
        # Luego la factura
        cursor.execute("DELETE FROM FACTURA WHERE id_factura = %s", (id_factura,))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        return str(err)
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ----------------------------------------------------------------------
# PAGOS
# ----------------------------------------------------------------------

def create_pago(id_factura, fecha_pago, monto, metodo_pago, referencia=None):
    """
    Inserta un pago asociado a una factura.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
            INSERT INTO PAGO (
                id_factura,
                fecha_pago,
                monto,
                metodo_pago,
                referencia
            )
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (id_factura, fecha_pago, monto, metodo_pago, referencia)
        cursor.execute(query, valores)
        conn.commit()
        return True

    except mysql.connector.Error as err:
        return str(err)
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def read_pagos_por_factura(id_factura):
    """
    Devuelve la lista de pagos (diccionarios) de una factura.
    """
    conn = None
    cursor = None
    pagos = []

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                id_pago,
                id_factura,
                fecha_pago,
                monto,
                metodo_pago,
                referencia
            FROM PAGO
            WHERE id_factura = %s
            ORDER BY fecha_pago ASC, id_pago ASC
        """
        cursor.execute(query, (id_factura,))
        pagos = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error al leer pagos de factura {id_factura}: {err}")
    except Exception as e:
        print(f"Error inesperado en read_pagos_por_factura: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return pagos


def delete_pago(id_pago):
    """
    Elimina un pago por su ID.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM PAGO WHERE id_pago = %s", (id_pago,))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        return str(err)
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ----------------------------------------------------------------------
# DETALLES DE FACTURA (stubs para que no den error las importaciones)
# ----------------------------------------------------------------------

def create_detalle_factura(*args, **kwargs):
    """Stub: por ahora no usamos detalle, devolvemos True para no romper nada."""
    return True


def read_detalles_por_factura(*args, **kwargs):
    """Stub: sin detalles, devolvemos lista vacía."""
    return []


def update_detalle_factura(*args, **kwargs):
    """Stub de actualización de detalle."""
    return True


def delete_detalle_factura(*args, **kwargs):
    """Stub de eliminación de detalle."""
    return True
