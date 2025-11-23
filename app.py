from flask import Flask, render_template, request, redirect, url_for, flash


# 1. IMPORTACIONES DE LÓGICA (TODAS AL PRINCIPIO)
from gestion_empleados_logic import create_empleado, read_empleados, update_empleado, delete_empleado
from gestion_pacientes_logic import create_paciente, read_pacientes, update_paciente, delete_paciente 
from gestion_procedimientos_logic import create_procedimiento, read_procedimientos, update_procedimiento, delete_procedimiento 
from gestion_areas_logic import create_area, read_areas, update_area, delete_area 

#  CONFIGURACIÓN DE FLASK 
app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash' 

@app.route('/')
def index():
    return redirect(url_for('gestion_empleados'))

# GESTION EMPLEADOS
@app.route('/empleados', methods=['GET', 'POST'])
def gestion_empleados():
    if request.method == 'POST':
        
        # CRUD
        if 'create' in request.form:
            try:
                nombre = request.form['nombre']
                puesto = request.form['puesto']
                fecha = request.form['fecha_contratacion']
                resultado = create_empleado(nombre, puesto, fecha)
                
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

                resultado = update_empleado(id_empleado, nombre, puesto, fecha)
                
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


if __name__ == '__main__':
    app.run(debug=True)