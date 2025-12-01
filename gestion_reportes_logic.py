# Parte del contenido de este módulo, incluyendo la estructura de las funciones
# de resumen y estadísticas, así como el manejo de conexiones a la base de datos,
# fue generado y asistido mediante ChatGPT (OpenAI, versión GPT-5.1).
#
# El código fue posteriormente revisado, adaptado y ampliado por el estudiante
# para ajustarse al modelo del proyecto, a las métricas requeridas y al correcto
# funcionamiento dentro del sistema.

import mysql.connector
from db_connection import DB_CONFIG


def obtener_resumen_clinico():
    """
    Métricas generales clínicas.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Total de pacientes
        cursor.execute("SELECT COUNT(*) AS total_pacientes FROM paciente")
        total_pacientes = cursor.fetchone()["total_pacientes"]

        # Pacientes hospitalizados actualmente
        cursor.execute("""
            SELECT COUNT(*) AS pacientes_hospitalizados
            FROM hospitalizaciones
            WHERE fecha_egreso IS NULL
        """)
        pacientes_hosp = cursor.fetchone()["pacientes_hospitalizados"]

        # Tratamientos registrados
        cursor.execute("SELECT COUNT(*) AS total_tratamientos FROM tratamiento")
        total_tratamientos = cursor.fetchone()["total_tratamientos"]

        # Procedimientos registrados
        cursor.execute("SELECT COUNT(*) AS total_procedimientos FROM procedimientos")
        total_procedimientos = cursor.fetchone()["total_procedimientos"]

        return {
            "total_pacientes": total_pacientes,
            "pacientes_hospitalizados": pacientes_hosp,
            "total_tratamientos": total_tratamientos,
            "total_procedimientos": total_procedimientos,
        }

    except mysql.connector.Error as err:
        return f"Error en obtener_resumen_clinico: {err}"
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            conn.close()


def obtener_resumen_ocupacion():
    """
    Ocupación por área (hospitalizaciones activas, Top 10).
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            a.id_area_especifica,
            a.nombre AS nombre_area,
            a.tipo AS tipo_area,
            COUNT(h.id_hospitalizaciones) AS pacientes_hospitalizados,
            MIN(h.fecha_ingreso) AS ingreso_mas_antiguo
        FROM area_especifica a
        LEFT JOIN hospitalizaciones h
            ON h.id_area_especifica = a.id_area_especifica
           AND h.fecha_egreso IS NULL
        GROUP BY a.id_area_especifica, a.nombre, a.tipo
        ORDER BY pacientes_hospitalizados DESC, a.nombre ASC
        LIMIT 10
        """
        cursor.execute(query)
        return cursor.fetchall()

    except mysql.connector.Error as err:
        return f"Error en obtener_resumen_ocupacion: {err}"
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            conn.close()


def obtener_productividad_medica(filtro_nombre=None):
    """
    Productividad por médico (Top 10):
    - Número de citas
    - Citas completadas
    - Participaciones en tratamientos / procedimientos
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        base_query = """
        SELECT
            e.id_empleado,
            e.nombre AS nombre_medico,
            COALESCE(COUNT(DISTINCT c.id_cita), 0) AS total_citas,
            COALESCE(SUM(CASE WHEN c.estado = 'Completada' THEN 1 ELSE 0 END), 0) AS citas_completadas,
            COALESCE(COUNT(DISTINCT prt.id_participacion), 0) AS total_participaciones
        FROM empleado e
        LEFT JOIN citas c
            ON c.id_empleado = e.id_empleado
        LEFT JOIN participacion prt
            ON prt.id_empleado = e.id_empleado
        WHERE e.tipo = 'medico'
        """

        params = []
        if filtro_nombre:
            base_query += " AND e.nombre LIKE %s"
            params.append(f"%{filtro_nombre}%")

        base_query += """
        GROUP BY e.id_empleado, e.nombre
        ORDER BY total_citas DESC, total_participaciones DESC
        LIMIT 10
        """

        cursor.execute(base_query, params)
        return cursor.fetchall()

    except mysql.connector.Error as err:
        return f"Error en obtener_productividad_medica: {err}"
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            conn.close()


def obtener_estadisticas_servicios():
    """
    Estadísticas de servicios:
    - Tratamientos por tipo
    - Procedimientos por tipo
    - Hospitalizaciones por mes (últimos 6 meses)
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Tratamientos por tipo
        cursor.execute("""
            SELECT tipo, COUNT(*) AS total
            FROM tratamiento
            GROUP BY tipo
        """)
        tratamientos_por_tipo = cursor.fetchall()

        # Procedimientos por tipo
        cursor.execute("""
            SELECT
                COALESCE(tipo, 'Sin tipo') AS tipo,
                COUNT(*) AS total
            FROM procedimientos
            GROUP BY tipo
        """)
        procedimientos_por_tipo = cursor.fetchall()

        # Hospitalizaciones por mes (agrupado por año-mes)
        cursor.execute("""
            SELECT
                DATE_FORMAT(fecha_ingreso, '%M %Y') AS mes,
                COUNT(*) AS total
            FROM hospitalizaciones
            GROUP BY mes
            ORDER BY mes DESC
            LIMIT 6
        """)

        hospitalizaciones_por_mes = cursor.fetchall()

        return {
            "tratamientos_por_tipo": tratamientos_por_tipo,
            "procedimientos_por_tipo": procedimientos_por_tipo,
            "hospitalizaciones_por_mes": hospitalizaciones_por_mes,
        }

    except mysql.connector.Error as err:
        return f"Error en obtener_estadisticas_servicios: {err}"
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            conn.close()


def obtener_resumen_administrativo():
    """
    Gestión administrativa / financiera:
    - Totales de facturación y pagos
    - Facturas por estado
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Resumen de montos
        cursor.execute("""
            SELECT
                COALESCE(SUM(f.total_neto), 0) AS total_facturado,
                COALESCE(SUM(p.monto), 0) AS total_pagado,
                COALESCE(SUM(f.total_neto), 0) - COALESCE(SUM(p.monto), 0) AS total_pendiente
            FROM factura f
            LEFT JOIN pago p ON p.id_factura = f.id_factura
        """)
        resumen_montos = cursor.fetchone()

        # Facturas por estado
        cursor.execute("""
            SELECT
                estado,
                COUNT(*) AS total
            FROM factura
            GROUP BY estado
        """)
        facturas_por_estado = cursor.fetchall()

        return {
            "resumen_montos": resumen_montos,
            "facturas_por_estado": facturas_por_estado,
        }

    except mysql.connector.Error as err:
        return f"Error en obtener_resumen_administrativo: {err}"
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            conn.close()
