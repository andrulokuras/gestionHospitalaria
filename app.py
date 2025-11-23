from flask import Flask, render_template, request, redirect, url_for, flash, session


# 1. IMPORTACIONES DE LÓGICA (TODAS AL PRINCIPIO)
from gestion_empleados_logic import create_empleado, read_empleados, update_empleado, delete_empleado
from gestion_pacientes_logic import create_paciente, read_pacientes, update_paciente, delete_paciente 
from gestion_procedimientos_logic import create_procedimiento, read_procedimientos, update_procedimiento, delete_procedimiento 
from gestion_areas_logic import create_area, read_areas, update_area, delete_area 
from gestion_tratamientos_logic import create_tratamiento, read_tratamientos, update_tratamiento, delete_tratamiento
from gestion_estancias_logic import create_estancia, read_estancias, update_estancia, delete_estancia
from gestion_participaciones_logic import create_participacion, read_participaciones, update_participacion, delete_participacion
from gestion_inventario_logic import create_articulo, read_inventario,update_articulo, delete_articulo
from auth_logic import validar_login
from functools import wraps
from gestion_facturas_logic import (
    create_factura,
    read_facturas,
    delete_factura,
    create_pago,
    read_pagos_por_factura,
    delete_pago,
)
from gestion_citas_logic import create_cita, read_citas, update_cita, delete_cita
from gestion_historial_logic import get_historial_completo



#  CONFIGURACIÓN DE FLASK 
app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash' 

def requiere_roles(*roles_permitidos):
    """
    Uso:
    @requiere_roles('admin', 'medico')
    def gestion_pacientes():
        ...
    """
    def decorador(vista):
        @wraps(vista)
        def vista_envuelta(*args, **kwargs):
            rol_usuario = session.get('rol')

            # Si por alguna razón no hay rol, lo mandamos a login
            if not rol_usuario:
                return redirect(url_for('login'))

            # Si su rol no está en la lista permitida:
            if rol_usuario not in roles_permitidos:
                flash("No tienes permiso para acceder a esta sección.", "danger")

                # Redirección amigable según rol
                if rol_usuario == 'medico':
                    return redirect(url_for('gestion_pacientes'))
                elif rol_usuario in ('enfermera', 'administrativo'):
                    return redirect(url_for('gestion_hospitalizaciones'))
                else:
                    return redirect(url_for('login'))

            # Si sí tiene permiso, se ejecuta la vista normal
            return vista(*args, **kwargs)
        return vista_envuelta
    return decorador

@app.before_request
def requerir_login():
    # Permitir acceso sin login a la página de login y a archivos estáticos
    if request.endpoint in ('login', 'static'):
        return

    # Si no hay usuario en sesión, redirigir a login
    if 'user_id' not in session:
        return redirect(url_for('login'))

from flask import session, redirect, url_for, flash

@app.route('/')
def index():
    rol = session.get('rol')

    # Si no hay sesión → login
    if not rol:
        return redirect(url_for('login'))

    # Redirección según rol
    if rol == 'admin':
        return redirect(url_for('gestion_empleados'))

    elif rol == 'medico':
        # El médico entra directo a Pacientes
        return redirect(url_for('gestion_pacientes'))

    elif rol == 'enfermera':
        # La enfermera también entra a Pacientes
        return redirect(url_for('gestion_pacientes'))

    elif rol == 'administrativo':
        # Administrativo directamente a Hospitalizaciones
        return redirect(url_for('gestion_hospitalizaciones'))

    # Rol raro / error
    flash("Rol no reconocido, inicia sesión de nuevo.", "danger")
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = validar_login(username, password)

        if user:
            # Guardar datos básicos en sesión
            session['user_id'] = user['id_usuario']
            session['username'] = user['username']
            session['rol'] = user['rol']

            flash(f"Bienvenido, {user['username']} ({user['rol']})", "success")
            return redirect(url_for('index'))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
            return redirect(url_for('login'))

    # Si ya está logueado, mandarlo directo a empleados
    if 'user_id' in session:
        return redirect(url_for('gestion_empleados'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('login'))

# GESTION EMPLEADOS
@app.route('/empleados', methods=['GET', 'POST'])
@requiere_roles('admin')
def gestion_empleados():
    if request.method == 'POST':
        
        # CRUD
        if 'create' in request.form:
            try:
                nombre = request.form['nombre']
                puesto = request.form['puesto']
                fecha = request.form['fecha_contratacion']
                tipo = request.form['tipo']
                resultado = create_empleado(nombre, puesto, fecha, tipo)
                
                if resultado is True:
                    flash('Empleado creado con éxito!', 'success')
                else:
                    flash(f'Error de BD al crear: {resultado}', 'danger')
            except Exception as e:
                 flash(f'Error de datos al crear: {e}', 'danger')

        elif 'delete' in request.form:
            try:
                id_empleado = request.form['id_empleado_eliminar']
                resultado = delete_empleado(id_empleado)
                
                if resultado is True:
                    flash(f'Empleado ID {id_empleado} eliminado.', 'success')
                else:
                    flash(f'Error de BD al eliminar: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de eliminación: {e}', 'danger')

        elif 'update' in request.form:
            try:
                id_empleado = request.form['id_empleado_actualizar']
                nombre = request.form['nombre_edit']
                puesto = request.form['puesto_edit']
                fecha = request.form['fecha_contratacion_edit']
                tipo = request.form['tipo_edit']

                resultado = update_empleado(id_empleado, nombre, puesto, fecha, tipo)
                
                if resultado is True:
                    flash(f'Empleado ID {id_empleado} actualizado con éxito!', 'success')
                else:
                    flash(f'Error de BD al actualizar: {resultado}', 'danger')
            except Exception as e:
                 flash(f'Error de actualización: {e}', 'danger')

        
        return redirect(url_for('gestion_empleados'))

    
    empleados = read_empleados() 
    return render_template('gestion_empleados.html', empleados=empleados)

# GESTIÓN DE PACIENTES
@app.route('/pacientes', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico', 'enfermera', 'administrativo')
def gestion_pacientes():
    if request.method == 'POST':
        
        if 'create_paciente' in request.form:
            try:
                
                nombre_completo = request.form['nombre'] 
                fecha_nacimiento = request.form['fecha_nacimiento']
                genero = request.form['genero']
                domicilio = request.form['direccion'] 
                telefono = request.form['telefono']
                seguro_medico = request.form['seguro_medico']
                resultado = create_paciente(nombre_completo, fecha_nacimiento, genero, domicilio, telefono, seguro_medico)
                
                if resultado is True:
                    flash('Paciente registrado con éxito.', 'success')
                else:
                    flash(f'Error de BD al registrar paciente: {resultado}', 'danger')
            except Exception as e:
                 flash(f'Error de datos al crear paciente: {e}', 'danger')

        elif 'delete_paciente' in request.form:
             try:
                id_paciente = request.form['id_paciente_eliminar']
                resultado = delete_paciente(id_paciente)
                
                if resultado is True:
                    flash(f'Paciente ID {id_paciente} eliminado.', 'success')
                else:
                    flash(f'Error de BD al eliminar paciente: {resultado}', 'danger')
             except Exception as e:
                flash(f'Error de eliminación: {e}', 'danger')
            
        elif 'update_paciente' in request.form:
            try:
                id_paciente = request.form['id_paciente_actualizar']
                nombre_completo = request.form['nombre_edit']
                fecha_nacimiento = request.form['fecha_nacimiento_edit']
                genero = request.form['genero_edit']
                domicilio = request.form['direccion_edit']
                telefono = request.form['telefono_edit']
                seguro_medico = request.form['seguro_medico_edit']
                resultado = update_paciente(id_paciente, nombre_completo, fecha_nacimiento, genero, domicilio, telefono, seguro_medico)
                
                if resultado is True:
                    flash(f'Paciente ID {id_paciente} actualizado con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar paciente: {resultado}', 'danger')
            except Exception as e:
                 flash(f'Error de actualización: {e}', 'danger')

        return redirect(url_for('gestion_pacientes'))

    pacientes = read_pacientes()
    return render_template('gestion_pacientes.html', pacientes=pacientes)


# GESTIÓN DE PROCEDIMIENTOS
@app.route('/procedimientos', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico')
def gestion_procedimientos():
    if request.method == 'POST':
        
        # 1. CREATE (Registrar Nuevo Procedimiento)
        if 'create_procedimiento' in request.form:
            try:
                fecha = request.form['fecha']
                tipo = request.form['tipo']
                resultados = request.form['resultados']
                
                resultado = create_procedimiento(fecha, tipo, resultados)
                
                if resultado is True:
                    flash('Procedimiento registrado con éxito.', 'success')
                else:
                    flash(f'Error de BD al registrar procedimiento: {resultado}', 'danger')
            except Exception as e:
                 flash(f'Error de datos al crear procedimiento: {e}', 'danger')

        # 2. DELETE (Eliminar Procedimiento)
        elif 'delete_procedimiento' in request.form:
             try:
                id_procedimiento = request.form['id_procedimiento_eliminar']
                resultado = delete_procedimiento(id_procedimiento)
                
                if resultado is True:
                    flash(f'Procedimiento ID {id_procedimiento} eliminado.', 'success')
                else:
                    flash(f'Error de BD al eliminar procedimiento: {resultado}', 'danger')
             except Exception as e:
                flash(f'Error de eliminación: {e}', 'danger')
            
        # 3. UPDATE (Actualizar Procedimiento)
        elif 'update_procedimiento' in request.form:
            try:
                id_procedimiento = request.form['id_procedimiento_actualizar']
                fecha = request.form['fecha_edit']
                tipo = request.form['tipo_edit']
                resultados = request.form['resultados_edit']

                resultado = update_procedimiento(id_procedimiento, fecha, tipo, resultados)
                
                if resultado is True:
                    flash(f'Procedimiento ID {id_procedimiento} actualizado con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar procedimiento: {resultado}', 'danger')
            except Exception as e:
                 flash(f'Error de actualización: {e}', 'danger')

        return redirect(url_for('gestion_procedimientos'))

    # Lógica GET (Mostrar la tabla)
    procedimientos = read_procedimientos()
    return render_template('gestion_procedimientos.html', procedimientos=procedimientos)


# GESTIÓN DE ÁREAS (RUTA UNIFICADA)

@app.route('/areas', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico', 'administrativo')
def gestion_areas():
    """
    Ruta unificada que maneja GET (mostrar lista) y POST (Crear, Actualizar, Eliminar)
    para la Gestión de Áreas.
    """
    if request.method == 'POST':
        
        # 1. CREATE (Registrar Nueva Área)
        if 'create_area' in request.form:
            try:
                tipo = request.form['tipo']
                nombre = request.form['nombre'] 
                ubicacion = request.form['ubicacion']
                
                resultado = create_area(tipo, nombre, ubicacion)
                
                if resultado is True:
                    flash(f'Área Específica registrada con éxito: {nombre}', 'success')
                else:
                    flash(f'Error de BD al registrar el área: {resultado}', 'danger')
            except Exception as e:
                 flash(f'Error de datos al crear área: {e}', 'danger')

        # 2. UPDATE (Actualizar Área)
        elif 'update_area' in request.form:
            try:
                id_area_especifica = request.form['id_area_actualizar']
                tipo = request.form['tipo_edit']
                nombre = request.form['nombre_edit'] 
                ubicacion = request.form['ubicacion_edit']

                resultado = update_area(id_area_especifica, tipo, nombre, ubicacion)
                
                if resultado is True:
                    flash(f'Área ID {id_area_especifica} actualizada con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar área: {resultado}', 'danger')
            except Exception as e:
                 flash(f'Error de actualización: {e}', 'danger')

        # 3. DELETE (Eliminar Área)
        elif 'delete_area' in request.form:
            try:
                id_area_especifica = request.form['id_area_especifica_eliminar']
                area_name_to_flash = request.form.get('nombre_area_eliminar', id_area_especifica) 
                
                resultado = delete_area(id_area_especifica)
                
                if resultado is True:
                    flash(f'Área {area_name_to_flash} eliminada.', 'success')
                else:
                    flash(f'Error de BD al eliminar área: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de eliminación: {e}', 'danger')

        return redirect(url_for('gestion_areas'))


    # Lógica GET (Mostrar la tabla)
    areas = read_areas()
    
    if isinstance(areas, str):
        flash(f"Error al cargar las áreas: {areas}", "danger")
        areas = []
        
    return render_template('areas_especificas.html', areas=areas)

# GESTIÓN DE TRATAMIENTOS
@app.route('/tratamientos', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico', 'enfermera')
def gestion_tratamientos():
    if request.method == 'POST':
        # 1. CREATE
        if 'create_tratamiento' in request.form:
            try:
                id_paciente = request.form['id_paciente']
                tipo = request.form['tipo']
                fecha_inicio = request.form['fecha_inicio']
                estado_actual = request.form['estado_actual']
                id_area_especifica = request.form['id_area_especifica']
                id_de_tratamiento = request.form.get('id_de_tratamiento') or None

                resultado = create_tratamiento(id_paciente, tipo, fecha_inicio, estado_actual, id_area_especifica, id_de_tratamiento)

                if resultado is True:
                    flash('Tratamiento registrado con éxito.', 'success')
                else:
                    flash(f'Error de BD al crear tratamiento: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de datos al crear tratamiento: {e}', 'danger')

        # 2. DELETE
        elif 'delete_tratamiento' in request.form:
            try:
                id_tratamiento = request.form['id_tratamiento_eliminar']
                resultado = delete_tratamiento(id_tratamiento)

                if resultado is True:
                    flash(f'Tratamiento ID {id_tratamiento} eliminado.', 'success')
                else:
                    flash(f'Error de BD al eliminar tratamiento: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de eliminación: {e}', 'danger')

        # 3. UPDATE
        elif 'update_tratamiento' in request.form:
            try:
                id_tratamiento = request.form['id_tratamiento_actualizar']
                id_paciente = request.form['id_paciente_edit']
                tipo = request.form['tipo_edit']
                fecha_inicio = request.form['fecha_inicio_edit']
                estado_actual = request.form['estado_actual_edit']
                id_area_especifica = request.form['id_area_especifica_edit']
                id_de_tratamiento = request.form.get('id_de_tratamiento_edit') or None

                resultado = update_tratamiento(id_tratamiento, id_paciente, tipo, fecha_inicio, estado_actual, id_area_especifica, id_de_tratamiento)

                if resultado is True:
                    flash(f'Tratamiento ID {id_tratamiento} actualizado con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar tratamiento: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de actualización: {e}', 'danger')

        return redirect(url_for('gestion_tratamientos'))

    # GET: mostrar tabla
    tratamientos = read_tratamientos()
    return render_template('gestion_tratamientos.html', tratamientos=tratamientos)

# GESTIÓN DE ESTANCIAS
@app.route('/estancias', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico', 'enfermera')
def gestion_estancias():
    if request.method == 'POST':

        # 1. CREAR
        if 'create_estancia' in request.form:
            try:
                medico_responsable = request.form['medico_responsable']      # name del input en el form
                hora = request.form['hora']
                id_procedimientos = request.form['id_procedimientos']

                resultado = create_estancia(medico_responsable, hora, id_procedimientos)

                if resultado is True:
                    flash('Estancia registrada con éxito.', 'success')
                else:
                    flash(f'Error de BD al registrar estancia: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de datos al crear estancia: {e}', 'danger')

        # 2. ELIMINAR
        elif 'delete_estancia' in request.form:
            try:
                id_estancia = request.form['id_estancia_eliminar']
                resultado = delete_estancia(id_estancia)

                if resultado is True:
                    flash(f'Estancia ID {id_estancia} eliminada.', 'success')
                else:
                    flash(f'Error de BD al eliminar estancia: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de eliminación: {e}', 'danger')

        # 3. ACTUALIZAR
        elif 'update_estancia' in request.form:
            try:
                id_estancia = request.form['id_estancia_actualizar']
                medico_responsable = request.form['medico_responsable_edit']
                hora = request.form['hora_edit']
                id_procedimientos = request.form['id_procedimientos_edit']

                resultado = update_estancia(id_estancia, medico_responsable, hora, id_procedimientos)

                if resultado is True:
                    flash(f'Estancia ID {id_estancia} actualizada con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar estancia: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de actualización: {e}', 'danger')

        return redirect(url_for('gestion_estancias'))

    # GET → mostrar tabla
    estancias = read_estancias()
    return render_template('estancias.html', estancias=estancias)

# HOSPITALIZACIONES
from gestion_hospitalizaciones_logic import (
    create_hospitalizacion, read_hospitalizaciones,
    update_hospitalizacion, delete_hospitalizacion
)

@app.route('/hospitalizaciones', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico', 'enfermera', 'administrativo')
def gestion_hospitalizaciones():
    if request.method == 'POST':

        # CREAR
        if 'create' in request.form:
            result = create_hospitalizacion(
                request.form['fecha_ingreso'],
                request.form.get('fecha_egreso'),
                request.form.get('motivo'),
                request.form.get('habitacion'),
                request.form['id_paciente'],
                request.form.get('id_estancia'),
                request.form['id_area']
            )
            if result is True:
                flash("Hospitalización registrada correctamente!", "success")
            else:
                flash(f"Error: {result}", "danger")

        # ACTUALIZAR
        if 'update' in request.form:
            result = update_hospitalizacion(
                request.form['id_hosp'],
                request.form['fecha_ingreso'],
                request.form.get('fecha_egreso'),
                request.form.get('motivo'),
                request.form.get('habitacion'),
                request.form['id_paciente'],
                request.form.get('id_estancia'),
                request.form['id_area']
            )
            flash("Hospitalización actualizada!", "success")

        # ELIMINAR
        if 'delete' in request.form:
            delete_hospitalizacion(request.form['id_hosp'])
            flash("Hospitalización eliminada!", "warning")

        return redirect(url_for('gestion_hospitalizaciones'))

    hospitalizaciones = read_hospitalizaciones()
    return render_template("hospitalizaciones.html", hospitalizaciones=hospitalizaciones)

@app.route('/participaciones', methods=['GET', 'POST'])
def gestion_participaciones():
    if request.method == 'POST':
        
        # 1. CREATE
        if 'create_participacion' in request.form:
            try:
                tipo_intervencion = request.form['tipo_intervencion']
                fecha = request.form['fecha']
                rol = request.form['rol']
                id_tratamiento = request.form['id_tratamiento']
                id_empleado = request.form['id_empleado']

                resultado = create_participacion(tipo_intervencion, fecha, rol, id_tratamiento, id_empleado)

                if resultado is True:
                    flash('Participación registrada con éxito.', 'success')
                else:
                    flash(f'Error de BD al crear participación: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de datos al crear participación: {e}', 'danger')

        # 2. DELETE
        elif 'delete_participacion' in request.form:
            try:
                id_participacion = request.form['id_participacion_eliminar']
                resultado = delete_participacion(id_participacion)

                if resultado is True:
                    flash(f'Participación ID {id_participacion} eliminada.', 'success')
                else:
                    flash(f'Error de BD al eliminar participación: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de eliminación: {e}', 'danger')

        # 3. UPDATE
        elif 'update_participacion' in request.form:
            try:
                id_participacion = request.form['id_participacion_actualizar']
                tipo_intervencion = request.form['tipo_intervencion_edit']
                fecha = request.form['fecha_edit']
                rol = request.form['rol_edit']
                id_tratamiento = request.form['id_tratamiento_edit']
                id_empleado = request.form['id_empleado_edit']

                resultado = update_participacion(id_participacion, tipo_intervencion, fecha, rol, id_tratamiento, id_empleado)

                if resultado is True:
                    flash(f'Participación ID {id_participacion} actualizada con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar participación: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de actualización: {e}', 'danger')

        return redirect(url_for('gestion_participaciones'))

    # GET: mostrar tabla
    participaciones = read_participaciones()
    return render_template('gestion_participaciones.html', participaciones=participaciones)

# FACTURAS
@app.route('/facturas', methods=['GET', 'POST'])
@requiere_roles('admin', 'administrativo')
def gestion_facturas():
    if request.method == "POST":

        # Crear factura
        if "create_factura" in request.form:
            try:
                id_paciente = int(request.form.get("id_paciente"))
                fecha_emision = request.form.get("fecha_emision")
                fecha_vencimiento = request.form.get("fecha_vencimiento") or None
                estado = request.form.get("estado") or "Pendiente"
                metodo_pago_preferido = request.form.get("metodo_pago_preferido") or None
                observaciones = request.form.get("observaciones") or None
                total_neto = float(request.form.get("total_neto") or 0)

                resultado = create_factura(
                    id_paciente,
                    fecha_emision,
                    fecha_vencimiento,
                    estado,
                    metodo_pago_preferido,
                    observaciones,
                    total_neto,
                )

                if resultado is True:
                    flash("Factura creada correctamente.", "success")
                else:
                    flash(f"Error BD al crear factura: {resultado}", "danger")

            except Exception as e:
                flash(f"Error al procesar la factura: {e}", "danger")

            return redirect(url_for("gestion_facturas"))

        # Registrar pago
        if "create_pago" in request.form:
            try:
                id_factura = int(request.form.get("id_factura_pago"))
                fecha_pago = request.form.get("fecha_pago")
                monto = float(request.form.get("monto_pago") or 0)
                metodo_pago = request.form.get("metodo_pago")
                referencia = request.form.get("referencia_pago") or None

                resultado = create_pago(
                    id_factura,
                    fecha_pago,
                    monto,
                    metodo_pago,
                    referencia,
                )

                if resultado is True:
                    flash("Pago registrado correctamente.", "success")
                else:
                    flash(f"Error BD al registrar pago: {resultado}", "danger")

            except Exception as e:
                flash(f"Error al procesar el pago: {e}", "danger")

            return redirect(url_for("gestion_facturas"))

        # Eliminar pago (botón opcional en la tabla)
        if "delete_pago" in request.form:
            id_pago = request.form.get("id_pago_eliminar")
            resultado = delete_pago(id_pago)
            if resultado is True:
                flash("Pago eliminado correctamente.", "success")
            else:
                flash(f"Error al eliminar pago: {resultado}", "danger")
            return redirect(url_for("gestion_facturas"))

        # Eliminar factura (opcional)
        if "delete_factura" in request.form:
            id_factura = request.form.get("id_factura_eliminar")
            resultado = delete_factura(id_factura)
            if resultado is True:
                flash("Factura eliminada correctamente.", "success")
            else:
                flash(f"Error al eliminar factura: {resultado}", "danger")
            return redirect(url_for("gestion_facturas"))

    # GET: leer facturas y sus pagos
    facturas = read_facturas()
    pagos_por_factura = {
        f["id_factura"]: read_pagos_por_factura(f["id_factura"]) for f in facturas
    }

    return render_template(
        "facturas.html",
        facturas=facturas,
        pagos_por_factura=pagos_por_factura,
    )

# CITAS
@app.route('/citas', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico', 'administrativo')
def gestion_citas():
    if request.method == 'POST':
        # 1. CREAR
        if 'create_cita' in request.form:
            try:
                # Convertir vacíos a None para campos opcionales
                area = request.form['id_area_especifica']
                if not area: area = None

                resultado = create_cita(
                    request.form['id_paciente'],
                    request.form['id_empleado'], # Médico
                    area,
                    request.form['fecha_hora_inicio'],
                    request.form['duracion_minutos'],
                    request.form['motivo_consulta'],
                    request.form['estado']
                )
                
                if resultado is True:
                    flash('Cita agendada con éxito.', 'success')
                else:
                    flash(f'Error de BD al agendar: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de datos al agendar: {e}', 'danger')

        # 2. ACTUALIZAR
        elif 'update_cita' in request.form:
            try:
                area = request.form['id_area_especifica_edit']
                if not area: area = None

                resultado = update_cita(
                    request.form['id_cita_actualizar'],
                    request.form['id_paciente_edit'],
                    request.form['id_empleado_edit'],
                    area,
                    request.form['fecha_hora_inicio_edit'],
                    request.form['duracion_minutos_edit'],
                    request.form['motivo_consulta_edit'],
                    request.form['estado_edit']
                )

                if resultado is True:
                    flash('Cita actualizada con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de actualización: {e}', 'danger')

        # 3. ELIMINAR
        elif 'delete_cita' in request.form:
            try:
                id_cita = request.form['id_cita_eliminar']
                resultado = delete_cita(id_cita)
                
                if resultado is True:
                    flash(f'Cita ID {id_cita} eliminada.', 'success')
                else:
                    flash(f'Error de BD al eliminar: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de eliminación: {e}', 'danger')
            
        return redirect(url_for('gestion_citas'))

    # GET: Cargar la tabla
    citas = read_citas()
    return render_template('gestion_citas.html', citas=citas)

# VISTA MAESTRA: LISTA DE PACIENTES PARA HISTORIAL
@app.route('/historial')
@requiere_roles('admin', 'medico', 'enfermera')
def lista_historial():
    # Reutilizamos la lógica de leer pacientes
    pacientes = read_pacientes()
    return render_template('lista_historial.html', pacientes=pacientes)

# VISTA DETALLE: EL EXPEDIENTE DEL PACIENTE
@app.route('/historial/<int:id_paciente>')
@requiere_roles('admin', 'medico', 'enfermera')
def ver_expediente(id_paciente):
    datos = get_historial_completo(id_paciente)
    
    if not datos or not datos['paciente']:
        flash("Paciente no encontrado", "danger")
        return redirect(url_for('lista_historial'))
        
    return render_template('detalle_expediente.html', data=datos)

@app.route('/inventario', methods=['GET', 'POST'])
@requiere_roles('admin', 'enfermera') # Restringido a 'admin' y 'enfermera'
def gestion_inventario():
    if request.method == 'POST':
        
        # 1. CREAR ARTÍCULO
        if 'create_articulo' in request.form:
            try:
                nombre = request.form['nombre']
                tipo = request.form['tipo']
                # Convertir a int y asegurar que no haya error si el campo está vacío (aunque es requerido en HTML)
                stock_actual = int(request.form['stock_actual']) 
                stock_minimo = int(request.form['stock_minimo'])
                
                ubicacion = request.form['ubicacion']
                numero_lote_serie = request.form.get('numero_lote_serie')
                
                # Campos de fecha opcionales (serán None si están vacíos)
                fecha_vencimiento = request.form.get('fecha_vencimiento')
                fecha_mantenimiento = request.form.get('fecha_mantenimiento')
                
                descripcion = request.form.get('descripcion')

                resultado = create_articulo(
                    nombre, tipo, stock_actual, stock_minimo, ubicacion, 
                    numero_lote_serie, fecha_vencimiento, fecha_mantenimiento, descripcion
                )
                
                if resultado is True:
                    flash(f'Artículo "{nombre}" registrado con éxito.', 'success')
                else:
                    flash(f'Error de BD al registrar: {resultado}', 'danger')
            except Exception as e:
                 flash(f'Error de datos al crear artículo: {e}', 'danger')

        # 2. ACTUALIZAR ARTÍCULO
        elif 'update_articulo' in request.form:
            try:
                # El campo oculto id_articulo_actualizar identifica el registro
                id_articulo = request.form['id_articulo_actualizar']
                
                # Los campos de edición tienen el mismo nombre en el modal, se recogen aquí:
                nombre = request.form['nombre']
                tipo = request.form['tipo']
                stock_actual = int(request.form['stock_actual']) 
                stock_minimo = int(request.form['stock_minimo'])
                ubicacion = request.form['ubicacion']
                numero_lote_serie = request.form.get('numero_lote_serie')
                fecha_vencimiento = request.form.get('fecha_vencimiento')
                fecha_mantenimiento = request.form.get('fecha_mantenimiento')
                descripcion = request.form.get('descripcion')

                resultado = update_articulo(
                    id_articulo, nombre, tipo, stock_actual, stock_minimo, ubicacion, 
                    numero_lote_serie, fecha_vencimiento, fecha_mantenimiento, descripcion
                )
                
                if resultado is True:
                    flash(f'Artículo ID {id_articulo} actualizado con éxito!', 'success')
                else:
                    flash(f'Error de BD al actualizar: {resultado}', 'danger')
            except Exception as e:
                 flash(f'Error de actualización: {e}', 'danger')

        # 3. ELIMINAR ARTÍCULO
        elif 'delete_articulo' in request.form:
            try:
                id_articulo = request.form['id_articulo_eliminar']
                resultado = delete_articulo(id_articulo)
                
                if resultado is True:
                    flash(f'Artículo ID {id_articulo} eliminado.', 'success')
                else:
                    flash(f'Error de BD al eliminar: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de eliminación: {e}', 'danger')
        
        return redirect(url_for('gestion_inventario'))

    # Lógica GET: Leer el inventario y mostrar la plantilla
    articulos = read_inventario()
    return render_template('gestion_inventario.html', articulos=articulos)

if __name__ == '__main__':
    app.run(debug=True)
