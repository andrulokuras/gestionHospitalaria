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
from gestion_hospitalizaciones_logic import ( create_hospitalizacion, read_hospitalizaciones, update_hospitalizacion, delete_hospitalizacion )
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
from gestion_asignaciones_logic import create_asignacion, read_asignaciones, update_asignacion, delete_asignacion
from gestion_reportes_logic import (
    obtener_resumen_clinico,
    obtener_resumen_ocupacion,
    obtener_productividad_medica,
    obtener_estadisticas_servicios,
    obtener_resumen_administrativo,
)
from gestion_usuarios_logic import (
    create_usuario, read_usuarios, update_usuario, delete_usuario
)




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

# LOGIN
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

    
    # GET: filtros
    filtro_nombre = request.args.get('buscar_nombre', '').strip()
    filtro_tipo = request.args.get('buscar_tipo', '').strip()

    empleados = read_empleados(
        filtro_nombre=filtro_nombre or None,
        filtro_tipo=filtro_tipo or None
    )

    return render_template(
        'gestion_empleados.html',
        empleados=empleados,
        filtro_nombre=filtro_nombre,
        filtro_tipo=filtro_tipo
    )


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

    # Obtener filtros desde la barra de búsqueda (query string)
    filtro_nombre = request.args.get('buscar_nombre', '').strip()
    filtro_seguro = request.args.get('buscar_seguro', '').strip()

    pacientes = read_pacientes(
        filtro_nombre=filtro_nombre or None,
        filtro_seguro=filtro_seguro or None
    )

    return render_template(
        'gestion_pacientes.html',
        pacientes=pacientes,
        filtro_nombre=filtro_nombre,
        filtro_seguro=filtro_seguro
    )



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

    # Lógica GET (Mostrar la tabla con filtro)
    filtro_tipo = request.args.get('buscar_tipo', '').strip()

    procedimientos = read_procedimientos(
        filtro_tipo=filtro_tipo or None
    )

    return render_template(
        'gestion_procedimientos.html',
        procedimientos=procedimientos,
        filtro_tipo=filtro_tipo
    )



# GESTIÓN DE ÁREAS
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
                
                raw_empleado = request.form.get('id_empleado', '')
                id_empleado  = extraer_id(raw_empleado) if raw_empleado else None

                recursos_clave = request.form.get('recursos_clave') or None
                
                resultado = create_area(tipo, nombre, ubicacion, id_empleado, recursos_clave)
                
                if resultado is True:
                    flash('Área específica registrada con éxito!', 'success')
                else:
                    flash(f'Error de BD al crear el área: {resultado}', 'danger')
                
            except Exception as e:
                 flash(f'Error de datos al crear área: {e}', 'danger')

        # 2. UPDATE (Actualizar Área)
        elif 'update_area' in request.form:
            try:
                id_area_especifica = request.form['id_area_actualizar']
                tipo = request.form['tipo_edit']
                nombre = request.form['nombre_edit'] 
                ubicacion = request.form['ubicacion_edit']

                raw_empleado = request.form.get('id_empleado_edit', '')
                id_empleado  = extraer_id(raw_empleado) if raw_empleado else None

                recursos_clave = request.form.get('recursos_clave_edit') or None

                resultado = update_area(id_area_especifica, tipo, nombre, ubicacion, id_empleado, recursos_clave)
                if resultado is True:
                    flash('Área actualizada con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar área: {resultado}', 'danger')
                
            except Exception as e:
                 flash(f'Error de actualización: {e}', 'danger')

        # 3. DELETE (Eliminar Área)
        elif 'delete_area' in request.form:
            try:
                id_area = request.form.get('id_area_especifica_eliminar')
            
                if not id_area:
                    raise ValueError("El ID del área a eliminar no fue proporcionado en la solicitud.")
            
                resultado = delete_area(id_area) 

                if resultado is True:
                    flash(f'Área específica ID {id_area} eliminada correctamente.', 'success')
                else:
                    flash(f'Error de BD al eliminar área: {resultado}', 'danger')
        
            except Exception as e:
                flash(f'Error al procesar la eliminación de área: {e}', 'danger')
        
        return redirect(url_for('gestion_areas'))


    # Lógica GET (Mostrar la tabla con filtros)
    filtro_tipo = request.args.get('buscar_tipo', '').strip()
    filtro_nombre = request.args.get('buscar_nombre', '').strip()

    areas = read_areas(
        filtro_tipo=filtro_tipo or None,
        filtro_nombre=filtro_nombre or None
    )

    if isinstance(areas, str):
        flash(f"Error al cargar las áreas: {areas}", "danger")
        areas = []

    # Lista de empleados para el datalist
    empleados_select = read_empleados()

    return render_template(
        'areas_especificas.html',
        areas=areas,
        filtro_tipo=filtro_tipo,
        filtro_nombre=filtro_nombre,
        empleados_select=empleados_select
    )


# GESTIÓN DE TRATAMIENTOS
@app.route('/tratamientos', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico', 'enfermera')
def gestion_tratamientos():
    if request.method == 'POST':
        # 1. CREATE
        if 'create_tratamiento' in request.form:
            try:
                # valores crudos: "2 - Regina", "3 - Ginecología", "5 - Biopsia"
                raw_paciente = request.form.get('id_paciente', '')
                raw_area     = request.form.get('id_area_especifica', '')
                raw_proc     = request.form.get('id_procedimiento', '')

                id_paciente        = extraer_id(raw_paciente)
                id_area_especifica = extraer_id(raw_area)
                id_procedimiento   = extraer_id(raw_proc) if raw_proc else None

                tipo          = request.form['tipo']
                fecha_inicio  = request.form['fecha_inicio']
                estado_actual = request.form['estado_actual']

                resultado = create_tratamiento(
                    id_paciente,
                    tipo,
                    fecha_inicio,
                    estado_actual,
                    id_area_especifica,
                    id_procedimiento
                )

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

                raw_paciente = request.form.get('id_paciente_edit', '')
                raw_area     = request.form.get('id_area_especifica_edit', '')
                raw_proc     = request.form.get('id_procedimiento_edit', '')

                id_paciente        = extraer_id(raw_paciente)
                id_area_especifica = extraer_id(raw_area)
                id_procedimiento   = extraer_id(raw_proc) if raw_proc else None

                tipo          = request.form['tipo_edit']
                fecha_inicio  = request.form['fecha_inicio_edit']
                estado_actual = request.form['estado_actual_edit']

                resultado = update_tratamiento(
                    id_tratamiento,
                    id_paciente,
                    tipo,
                    fecha_inicio,
                    estado_actual,
                    id_area_especifica,
                    id_procedimiento
                )

                if resultado is True:
                    flash(f'Tratamiento ID {id_tratamiento} actualizado con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar tratamiento: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de actualización: {e}', 'danger')

        return redirect(url_for('gestion_tratamientos'))

    # GET: mostrar tabla con filtro opcional por nombre de paciente
    filtro_nombre = request.args.get('buscar_paciente', '').strip()

    tratamientos = read_tratamientos(
        filtro_nombre_paciente=filtro_nombre or None
    )

    # listas para los datalist
    pacientes_select      = read_pacientes(filtro_nombre=None, filtro_seguro=None)
    areas_select          = read_areas()
    procedimientos_select = read_procedimientos()

    return render_template(
        'gestion_tratamientos.html',
        tratamientos=tratamientos,
        filtro_nombre=filtro_nombre,
        pacientes_select=pacientes_select,
        areas_select=areas_select,
        procedimientos_select=procedimientos_select
    )



# GESTIÓN DE ESTANCIAS
@app.route('/estancias', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico', 'enfermera')
def gestion_estancias():
    if request.method == 'POST':

        # 1. CREAR
        if 'create_estancia' in request.form:
            try:
                raw_medico = request.form['medico_responsable']      # "3 - Dr. Limón"
                hora = request.form['hora']
                raw_proc = request.form['id_procedimientos']         # "5 - Biopsia" por ej.

                id_medico_responsable = extraer_id(raw_medico)
                id_procedimientos = extraer_id(raw_proc)

                resultado = create_estancia(id_medico_responsable, hora, id_procedimientos)

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

                raw_medico = request.form['medico_responsable_edit']
                hora = request.form['hora_edit']
                raw_proc = request.form['id_procedimientos_edit']

                id_medico_responsable = extraer_id(raw_medico)
                id_procedimientos = extraer_id(raw_proc)

                resultado = update_estancia(id_estancia, id_medico_responsable, hora, id_procedimientos)

                if resultado is True:
                    flash(f'Estancia ID {id_estancia} actualizada con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar estancia: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de actualización: {e}', 'danger')

        return redirect(url_for('gestion_estancias'))

    # GET → mostrar tabla con filtro opcional por nombre de médico
    filtro_medico = request.args.get('buscar_medico', '').strip()

    estancias = read_estancias(
        filtro_medico=filtro_medico or None
    )

    # Listas para los datalist
    medicos_select = read_empleados()                 # luego filtramos si quieres solo médicos
    # si solo quieres tipo "medico":
    medicos_select = [
        m for m in medicos_select
        if getattr(m, 'tipo', None) == 'medico'
        or (isinstance(m, dict) and m.get('tipo') == 'medico')
    ]

    procedimientos_select = read_procedimientos()

    return render_template(
        'estancias.html',
        estancias=estancias,
        filtro_medico=filtro_medico,
        medicos_select=medicos_select,
        procedimientos_select=procedimientos_select
    )


# HOSPITALIZACIONES
@app.route('/hospitalizaciones', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico', 'enfermera', 'administrativo')
def gestion_hospitalizaciones():
    if request.method == 'POST':

        # CREAR
        if 'create' in request.form:
            # hacer opcionales fecha_egreso y motivo
            fecha_egreso = request.form.get('fecha_egreso') or None
            motivo = request.form.get('motivo') or None

            # valores crudos: "2 - Regina Valenzuela", "3 - Estancia corta", etc.
            raw_paciente  = request.form.get('id_paciente', '')
            raw_estancia  = request.form.get('id_estancia', '')
            raw_area      = request.form.get('id_area', '')

            id_paciente   = extraer_id(raw_paciente)
            id_estancia   = extraer_id(raw_estancia)
            id_area       = extraer_id(raw_area)

            result = create_hospitalizacion(
                request.form['fecha_ingreso'],
                fecha_egreso,
                motivo,
                request.form.get('habitacion'),
                id_paciente,
                id_estancia,
                id_area
            )
            if result is True:
                flash("Hospitalización registrada correctamente!", "success")
            else:
                flash(f"Error: {result}", "danger")

        # ACTUALIZAR
        if 'update' in request.form:
            # hacer opcionales fecha_egreso y motivo
            fecha_egreso = request.form.get('fecha_egreso') or None
            motivo = request.form.get('motivo') or None

            raw_paciente  = request.form.get('id_paciente', '')
            raw_estancia  = request.form.get('id_estancia', '')
            raw_area      = request.form.get('id_area', '')

            id_paciente   = extraer_id(raw_paciente)
            id_estancia   = extraer_id(raw_estancia)
            id_area       = extraer_id(raw_area)

            result = update_hospitalizacion(
                request.form['id_hosp'],
                request.form['fecha_ingreso'],
                fecha_egreso,
                motivo,
                request.form.get('habitacion'),
                id_paciente,
                id_estancia,
                id_area
            )
            flash("Hospitalización actualizada!", "success")

        # ELIMINAR
        if 'delete' in request.form:
            delete_hospitalizacion(request.form['id_hosp'])
            flash("Hospitalización eliminada!", "warning")

        return redirect(url_for('gestion_hospitalizaciones'))

    # GET: mostrar lista con filtro opcional por nombre de paciente
    filtro_nombre = request.args.get('buscar_nombre', '').strip()

    hospitalizaciones = read_hospitalizaciones(
        filtro_nombre=filtro_nombre or None
    )

    # listas para los datalist
    pacientes_select = read_pacientes(
        filtro_nombre=None,
        filtro_seguro=None
    )
    estancias_select = read_estancias()
    areas_select     = read_areas()

    return render_template(
        "hospitalizaciones.html",
        hospitalizaciones=hospitalizaciones,
        filtro_nombre=filtro_nombre,
        pacientes_select=pacientes_select,
        estancias_select=estancias_select,
        areas_select=areas_select
    )

    return render_template(
        "hospitalizaciones.html",
        hospitalizaciones=hospitalizaciones,
        filtro_nombre=filtro_nombre
    )


# GESTIÓN DE PARTICIPACIONES
@app.route('/participaciones', methods=['GET', 'POST'])
def gestion_participaciones():
    if request.method == 'POST':
        
        # 1. CREATE
        if 'create_participacion' in request.form:
            try:
                tipo_intervencion = request.form['tipo_intervencion']
                fecha = request.form['fecha']
                rol = request.form['rol']

                raw_trat  = request.form.get('id_tratamiento', '')
                raw_emp   = request.form.get('id_empleado', '')

                id_tratamiento = extraer_id(raw_trat)
                id_empleado    = extraer_id(raw_emp)

                resultado = create_participacion(
                    tipo_intervencion,
                    fecha,
                    rol,
                    id_tratamiento,
                    id_empleado
                )

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
                id_participacion   = request.form['id_participacion_actualizar']
                tipo_intervencion  = request.form['tipo_intervencion_edit']
                fecha              = request.form['fecha_edit']
                rol                = request.form['rol_edit']

                raw_trat_edit = request.form.get('id_tratamiento_edit', '')
                raw_emp_edit  = request.form.get('id_empleado_edit', '')

                id_tratamiento = extraer_id(raw_trat_edit)
                id_empleado    = extraer_id(raw_emp_edit)

                resultado = update_participacion(
                    id_participacion,
                    tipo_intervencion,
                    fecha,
                    rol,
                    id_tratamiento,
                    id_empleado
                )

                if resultado is True:
                    flash(f'Participación ID {id_participacion} actualizada con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar participación: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de actualización: {e}', 'danger')

        return redirect(url_for('gestion_participaciones'))

    # GET: mostrar tabla con filtros
    filtro_tipo_intervencion = request.args.get("buscar_tipo_intervencion", "").strip()
    filtro_nombre_empleado   = request.args.get("buscar_empleado", "").strip()

    participaciones = read_participaciones(
        filtro_tipo_intervencion=filtro_tipo_intervencion or None,
        filtro_nombre_empleado=filtro_nombre_empleado or None
    )

    # listas para los datalist
    tratamientos_select = read_tratamientos(
        filtro_nombre_paciente=None  # ajusta según firma de tu función
    )
    empleados_select = read_empleados()

    return render_template(
        'gestion_participaciones.html',
        participaciones=participaciones,
        filtro_tipo_intervencion=filtro_tipo_intervencion,
        filtro_nombre_empleado=filtro_nombre_empleado,
        tratamientos_select=tratamientos_select,
        empleados_select=empleados_select
    )

# FACTURAS
@app.route('/facturas', methods=['GET', 'POST'])
@requiere_roles('admin', 'administrativo')
def gestion_facturas():
    if request.method == "POST":

        # Crear factura
        if "create_factura" in request.form:
            try:
                # Puede venir como "2 - Regina Valenzuela"
                raw_paciente = request.form.get("id_paciente", "")
                id_paciente_str = extraer_id(raw_paciente)
                id_paciente = int(id_paciente_str)

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

        # Eliminar pago
        if "delete_pago" in request.form:
            id_pago = request.form.get("id_pago_eliminar")
            resultado = delete_pago(id_pago)
            if resultado is True:
                flash("Pago eliminado correctamente.", "success")
            else:
                flash(f"Error al eliminar pago: {resultado}", "danger")
            return redirect(url_for("gestion_facturas"))

        # Eliminar factura
        if "delete_factura" in request.form:
            id_factura = request.form.get("id_factura_eliminar")
            resultado = delete_factura(id_factura)
            if resultado is True:
                flash("Factura eliminada correctamente.", "success")
            else:
                flash(f"Error al eliminar factura: {resultado}", "danger")
            return redirect(url_for("gestion_facturas"))

    # ---------- GET: leer facturas con filtros ----------
    filtro_estado = request.args.get("buscar_estado", "").strip()
    filtro_paciente = request.args.get("buscar_paciente", "").strip()

    filtro_paciente_int = None
    if filtro_paciente:
        try:
            filtro_paciente_int = int(filtro_paciente)
        except ValueError:
            filtro_paciente_int = None  # si no es número, no filtra por paciente

    facturas = read_facturas(
        filtro_estado=filtro_estado or None,
        filtro_paciente=filtro_paciente_int
    )

    pagos_por_factura = {
        f["id_factura"]: read_pagos_por_factura(f["id_factura"])
        for f in facturas
    }

    # Lista de pacientes para el <datalist> en el formulario
    pacientes_select = read_pacientes(
        filtro_nombre=None,
        filtro_seguro=None
    )

    return render_template(
        "facturas.html",
        facturas=facturas,
        pagos_por_factura=pagos_por_factura,
        filtro_estado=filtro_estado,
        filtro_paciente=filtro_paciente,
        pacientes_select=pacientes_select
    )


# ---- Helper para limpiar IDs ----
def extraer_id(valor):
    """Recibe algo como '2 - Regina Valenzuela' y devuelve '2'."""
    if not valor:
        return None
    return valor.split('-', 1)[0].strip()


# CITAS
@app.route('/citas', methods=['GET', 'POST'])
@requiere_roles('admin', 'medico', 'administrativo')
def gestion_citas():
    if request.method == 'POST':
        # 1. CREAR
        if 'create_cita' in request.form:
            try:
                raw_paciente = request.form.get('id_paciente', '')
                raw_medico   = request.form.get('id_empleado', '')
                raw_area     = request.form.get('id_area_especifica', '')

                id_paciente = extraer_id(raw_paciente)
                id_medico   = extraer_id(raw_medico)
                area        = extraer_id(raw_area) if raw_area else None

                resultado = create_cita(
                    id_paciente,                    # solo el número
                    id_medico,                      # solo el número
                    area,
                    request.form['fecha_hora_inicio'],
                    request.form['duracion_minutos'],
                    request.form.get('motivo_consulta', ''),
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
                raw_paciente = request.form.get('id_paciente_edit', '')
                raw_medico   = request.form.get('id_empleado_edit', '')
                raw_area     = request.form.get('id_area_especifica_edit', '')

                id_paciente = extraer_id(raw_paciente)
                id_medico   = extraer_id(raw_medico)
                area        = extraer_id(raw_area) if raw_area else None

                resultado = update_cita(
                    request.form['id_cita_actualizar'],
                    id_paciente,                    # solo ID numérico
                    id_medico,                      # solo ID numérico
                    area,                           # puede ser None
                    request.form['fecha_hora_inicio_edit'],
                    request.form['duracion_minutos_edit'],
                    request.form.get('motivo_consulta_edit', ''),
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

    # GET: Cargar la tabla con filtros
    filtro_estado = request.args.get('filtro_estado', '').strip()

    citas = read_citas(
        filtro_estado=filtro_estado or None
    )

    pacientes_select = read_pacientes(
        filtro_nombre=None,
        filtro_seguro=None
    )

    empleados_select = read_empleados()          # luego filtramos solo médicos
    medicos_select = [
        e for e in empleados_select
        if getattr(e, 'tipo', None) == 'medico'
        or (isinstance(e, dict) and e.get('tipo') == 'medico')
    ]

    areas_select = read_areas()

    return render_template(
        'gestion_citas.html',
        citas=citas,
        filtro_estado=filtro_estado,
        pacientes_select=pacientes_select,
        medicos_select=medicos_select,
        areas_select=areas_select
    )



# VISTA MAESTRA: LISTA DE PACIENTES PARA HISTORIAL
@app.route('/historial')
@requiere_roles('admin', 'medico', 'enfermera')
def lista_historial():
    # Tomamos el filtro que venga en la barra de búsqueda (GET)
    filtro_nombre = request.args.get('buscar_nombre', '').strip()

    # Si ya implementaste read_pacientes con filtros, reusamos ese parámetro
    # Si no, puedes ajustar la función read_pacientes para aceptarlo
    pacientes = read_pacientes(
        filtro_nombre=filtro_nombre or None  # si viene vacío, no filtra
    )

    return render_template(
        'lista_historial.html',
        pacientes=pacientes,
        filtro_nombre=filtro_nombre
    )
# VISTA DETALLE: EL EXPEDIENTE DEL PACIENTE
@app.route('/historial/<int:id_paciente>')
@requiere_roles('admin', 'medico', 'enfermera')
def ver_expediente(id_paciente):
    datos = get_historial_completo(id_paciente)
    
    if not datos or not datos['paciente']:
        flash("Paciente no encontrado", "danger")
        return redirect(url_for('lista_historial'))
        
    return render_template('detalle_expediente.html', data=datos)


# INVENTARIO
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
    # Lógica GET: filtros
    filtro_nombre = request.args.get('buscar_nombre', '').strip()
    filtro_tipo = request.args.get('buscar_tipo', '').strip()

    articulos = read_inventario(
        filtro_nombre=filtro_nombre or None,
        filtro_tipo=filtro_tipo or None
    )

    return render_template(
        'gestion_inventario.html',
        articulos=articulos,
        filtro_nombre=filtro_nombre,
        filtro_tipo=filtro_tipo
    )


# ASIGNACIONES
@app.route('/asignaciones', methods=['GET', 'POST'])
@requiere_roles('admin', 'administrativo')  # Solo Admin o Administrativo pueden gestionar turnos
def gestion_asignaciones():
    asignaciones = []
    empleados = []
    areas = []
    
    # ------------------ LÓGICA POST ------------------
    if request.method == 'POST':
        # 1. CREATE
        if 'create_asignacion' in request.form:
            try:
                # Pueden venir como "3 - Dra. Pérez" y "5 - UCI Adultos"
                raw_empleado = request.form.get('id_empleado_fk', '')
                raw_area     = request.form.get('id_area_fk', '')
                
                id_empleado = extraer_id(raw_empleado)   # "3 - Dra. Pérez" → "3"
                id_area     = extraer_id(raw_area)       # "5 - UCI Adultos" → "5"
                
                asignacion     = request.form['asignacion']        # TEXT (puede ser vacío)
                turno_datetime = request.form['turno_datetime']    # DATETIME

                resultado = create_asignacion(id_empleado, id_area, asignacion, turno_datetime)
                
                if resultado is True:
                    flash('Asignación de turno registrada con éxito.', 'success')
                else:
                    flash(f'Error de BD al crear asignación: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de datos al crear asignación: {e}', 'danger')

        # 2. UPDATE
        elif 'update_asignacion' in request.form:
            try:
                id_asignacion = request.form['id_asignacion_actualizar']

                # En el modal usas <select>, pero por si acaso en algún momento
                # cambias a "ID - Nombre", también pasamos por extraer_id.
                raw_empleado_edit = request.form.get('id_empleado_edit', '')
                raw_area_edit     = request.form.get('id_area_especifica_edit', '')

                id_empleado       = extraer_id(raw_empleado_edit)
                id_area_especifica = extraer_id(raw_area_edit)

                asignacion     = request.form['asignacion_edit']
                turno_datetime = request.form['turno_datetime_edit']
                
                resultado = update_asignacion(
                    id_asignacion,
                    id_empleado,
                    id_area_especifica,
                    asignacion,
                    turno_datetime
                )

                if resultado is True:
                    flash(f'Asignación ID {id_asignacion} actualizada con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar asignación: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de actualización: {e}', 'danger')

        # 3. DELETE
        elif 'delete_asignacion' in request.form:
            try:
                id_asignacion = request.form['id_asignacion_eliminar']
                resultado = delete_asignacion(id_asignacion)

                if resultado is True:
                    flash(f'Asignación ID {id_asignacion} eliminada.', 'success')
                else:
                    flash(f'Error de BD al eliminar asignación: {resultado}', 'danger')
            except Exception as e:
                flash(f'Error de eliminación: {e}', 'danger')

        return redirect(url_for('gestion_asignaciones'))

    # ------------------ LÓGICA GET ------------------
    filtro_nombre_medico = request.args.get("buscar_medico", "").strip()

    try:
        asignaciones = read_asignaciones(
            filtro_nombre_medico=filtro_nombre_medico or None
        )
        empleados = read_empleados()
        areas = read_areas()
        
    except Exception as e:
        flash(f'Error crítico al cargar datos base (Empleados, Áreas o Asignaciones): {e}', 'danger')
        asignaciones = []
        empleados = []
        areas = []

    if isinstance(empleados, str) or isinstance(areas, str):
        flash("Error al cargar datos base (Empleados/Áreas).", "danger")
        empleados = []
        areas = []

    return render_template(
        'gestion_asignaciones.html', 
        asignaciones=asignaciones,
        empleados=empleados,
        areas=areas,
        filtro_nombre_medico=filtro_nombre_medico
    )

# REPORTES
@app.route('/reportes')
@requiere_roles('admin', 'medico', 'enfermera', 'administrativo')
def reportes():
    # Filtro opcional por nombre de médico (para el panel de productividad)
    filtro_medico = request.args.get('medico', '').strip()

    resumen_clinico = obtener_resumen_clinico()
    resumen_ocupacion = obtener_resumen_ocupacion()
    productividad = obtener_productividad_medica(filtro_medico)
    estadisticas_servicios = obtener_estadisticas_servicios()
    resumen_admin = obtener_resumen_administrativo()

    # Manejo sencillo de errores (si alguna función regresa string)
    if isinstance(resumen_clinico, str):
        flash(resumen_clinico, 'danger')
        resumen_clinico = {}

    if isinstance(resumen_ocupacion, str):
        flash(resumen_ocupacion, 'danger')
        resumen_ocupacion = []

    if isinstance(productividad, str):
        flash(productividad, 'danger')
        productividad = []

    if isinstance(estadisticas_servicios, str):
        flash(estadisticas_servicios, 'danger')
        estadisticas_servicios = {
            "tratamientos_por_tipo": [],
            "procedimientos_por_tipo": [],
            "hospitalizaciones_por_mes": [],
        }

    if isinstance(resumen_admin, str):
        flash(resumen_admin, 'danger')
        resumen_admin = {
            "resumen_montos": {
                "total_facturado": 0,
                "total_pagado": 0,
                "total_pendiente": 0,
            },
            "facturas_por_estado": [],
        }

    # Total de hospitalizados actuales (para el encabezado)
    total_hospitalizados = sum(
        a.get("pacientes_hospitalizados", 0) for a in resumen_ocupacion
    )

    return render_template(
        'reportes.html',
        resumen_clinico=resumen_clinico,
        resumen_ocupacion=resumen_ocupacion,
        productividad=productividad,
        estadisticas_servicios=estadisticas_servicios,
        resumen_admin=resumen_admin,
        total_hospitalizados=total_hospitalizados,
    )

# GESTIÓN DE USUARIOS (solo admin)
@app.route('/usuarios', methods=['GET', 'POST'])
@requiere_roles('admin')
def gestion_usuarios():
    if request.method == 'POST':
        # CREAR
        if 'create_usuario' in request.form:
            try:
                username = request.form['username']
                password = request.form['password']
                rol = request.form['rol']
                id_empleado = request.form.get('id_empleado') or None

                if id_empleado == "":
                    id_empleado = None

                resultado = create_usuario(username, password, rol, id_empleado)

                if resultado is True:
                    flash('Usuario creado con éxito.', 'success')
                else:
                    flash(f'Error de BD al crear usuario: {resultado}', 'danger')

            except Exception as e:
                flash(f'Error de datos al crear usuario: {e}', 'danger')

        # ACTUALIZAR
        elif 'update_usuario' in request.form:
            try:
                id_usuario = request.form['id_usuario_actualizar']
                username = request.form['username_edit']
                password = request.form['password_edit']
                rol = request.form['rol_edit']
                id_empleado = request.form.get('id_empleado_edit') or None

                if id_empleado == "":
                    id_empleado = None

                resultado = update_usuario(
                    id_usuario, username, password, rol, id_empleado
                )

                if resultado is True:
                    flash('Usuario actualizado con éxito.', 'success')
                else:
                    flash(f'Error de BD al actualizar usuario: {resultado}', 'danger')

            except Exception as e:
                flash(f'Error de datos al actualizar usuario: {e}', 'danger')

        # ELIMINAR
        elif 'delete_usuario' in request.form:
            try:
                id_usuario = request.form['id_usuario_eliminar']
                resultado = delete_usuario(id_usuario)

                if resultado is True:
                    flash(f'Usuario ID {id_usuario} eliminado.', 'success')
                else:
                    flash(f'Error de BD al eliminar usuario: {resultado}', 'danger')

            except Exception as e:
                flash(f'Error de eliminación de usuario: {e}', 'danger')

        return redirect(url_for('gestion_usuarios'))

    # GET: filtros
    filtro_username = request.args.get('buscar_username', '').strip()
    filtro_rol = request.args.get('buscar_rol', '').strip()

    usuarios = read_usuarios(
        filtro_username=filtro_username or None,
        filtro_rol=filtro_rol or None
    )

    # Para el select de empleados (opcional)
    empleados = read_empleados(
        filtro_nombre=None,
        filtro_tipo=None
    )

    return render_template(
        'gestion_usuarios.html',
        usuarios=usuarios,
        empleados=empleados,
        filtro_username=filtro_username,
        filtro_rol=filtro_rol
    )


if __name__ == '__main__':
    app.run(debug=True)
