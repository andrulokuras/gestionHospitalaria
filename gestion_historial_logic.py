# gestion_historial_logic.py
import mysql.connector
from db_connection import DB_CONFIG

def get_historial_completo(id_paciente):
    conn = None
    data = {
        "paciente": None,
        "tratamientos": [],
        "hospitalizaciones": [],
        "citas": []
    }
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # 1. Datos Personales
        query_paciente = "SELECT * FROM paciente WHERE id_paciente = %s"
        cursor.execute(query_paciente, (id_paciente,))
        data["paciente"] = cursor.fetchone()

        # 2. Tratamientos (Corregido: Join con Area Específica)
        query_trat = """
            SELECT t.*, a.nombre as nombre_area 
            FROM tratamiento t
            LEFT JOIN area_especifica a ON t.id_area_especifica = a.id_area_especifica
            WHERE t.id_paciente = %s
            ORDER BY t.fecha_inicio DESC
        """
        cursor.execute(query_trat, (id_paciente,))
        data["tratamientos"] = cursor.fetchall()

        # 3. Hospitalizaciones (Corregido: Join con Area Específica)
        query_hosp = """
            SELECT h.*, a.nombre as nombre_area 
            FROM hospitalizaciones h
            LEFT JOIN area_especifica a ON h.id_area_especifica = a.id_area_especifica
            WHERE h.id_paciente = %s
            ORDER BY h.fecha_ingreso DESC
        """
        cursor.execute(query_hosp, (id_paciente,))
        data["hospitalizaciones"] = cursor.fetchall()

        # 4. Citas Médicas (CORREGIDO AQUI)
        # Ahora apuntamos directo a la tabla 'empleado' para sacar nombre y especialidad
        query_citas = """
            SELECT 
                c.*, 
                e.nombre as nombre_medico,
                e.puesto_especialidad as especialidad 
            FROM citas c
            LEFT JOIN empleado e ON c.id_empleado = e.id_empleado
            WHERE c.id_paciente = %s
            ORDER BY c.fecha_hora_inicio DESC
        """
        cursor.execute(query_citas, (id_paciente,))
        data["citas"] = cursor.fetchall()

        return data

    except mysql.connector.Error as err:
        print(f"Error obteniendo historial: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()