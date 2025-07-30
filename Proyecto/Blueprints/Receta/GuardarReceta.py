from flask import Blueprint, render_template, request, flash, redirect, url_for
from Cuerito import execute_query

GuardarR_bp = Blueprint('GuardarR', __name__)

# Ruta para guardar los datos de la exploración y la receta
@GuardarR_bp.route('/guardarReceta', methods=['POST'])
def guardarReceta():
    errores = {}
    
    # Obtener el ID del paciente del formulario (input hidden)
    id_paciente = request.form.get('id_paciente', '').strip()
    
    
    # Datos de exploración
    fecha = request.form.get('fechaExploracion', '').strip()
    altura = request.form.get('altura', '').strip()
    latidos = request.form.get('lpm', '').strip()
    glucosa = request.form.get('glucosa', '').strip()
    peso = request.form.get('peso', '').strip()
    temperatura = request.form.get('temperatura', '').strip()
    oxigeno = request.form.get('saturacionOxigeno', '').strip()
    
    # Datos de diagnóstico
    sintomas = request.form.get('sintomas', '').strip()
    diagnostico = request.form.get('diagnostico', '').strip()
    receta = request.form.get('receta', '').strip()
    indicaciones = request.form.get('indicaciones', '').strip()
    
    # Validaciones
    if not id_paciente:
        errores['general'] = 'ID de paciente requerido'
    
    # Validaciones de exploración
    if not fecha:
        errores['fechaExploracion'] = 'Ingresa la fecha en que se genera la exploración'
    if not altura:
        errores['altura'] = 'La altura del paciente es obligatoria'
    if not latidos:
        errores['lpm'] = 'Los latidos por minuto del paciente son necesarios'
    if not glucosa:
        errores['glucosa'] = 'La glucosa del paciente es obligatoria'
    if not peso:
        errores['peso'] = 'El peso del paciente es obligatorio'
    if not temperatura:
        errores['temperatura'] = 'La temperatura del paciente es obligatoria'
    if not oxigeno:
        errores['saturacionOxigeno'] = 'El nivel de saturación de oxígeno es obligatorio'
    
    # Validaciones de diagnóstico
    if not sintomas:
        errores['sintomas'] = 'Si no hay síntomas indicar "Ninguno"'
    if not diagnostico:
        errores['diagnostico'] = 'Si no hay diagnóstico indicar "No hay diagnóstico"'
    if not receta:
        errores['receta'] = 'Si no hay receta indicar "Sin receta"'
    if not indicaciones:
        errores['indicaciones'] = 'Si no hay indicaciones indicar "No hay indicaciones"'
    
    # Si hay errores, regresar al formulario pero conservando el id_paciente
    if errores:
        # Obtener el nombre del paciente para mostrar en caso de error
        paciente_info = None
        if id_paciente:
            try:
                query = "SELECT nombre FROM expediente_pacientes WHERE id_paciente = %s"
                result = execute_query(query, (id_paciente,), fetch="one")
                if result:
                    paciente_info = {'id': id_paciente, 'nombre': result[0]}
            except:
                pass
                
        return render_template('cita_exploracion_diagnostico.html', 
                             errores=errores, 
                             paciente_info=paciente_info)
    
    try:
        # Primera inserción: exploraciones (CON ID DEL PACIENTE)
        query1 = '''
            INSERT INTO exploraciones (id_paciente, fecha, altura, lpm, glucosa, peso, temperatura, saturacion_oxigeno)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params1 = (id_paciente, fecha, altura, latidos, glucosa, peso, temperatura, oxigeno)
        execute_query(query1, params1, commit=False)
        
        # Segunda inserción: diagnosticos (CON ID DEL PACIENTE)
        query2 = '''
            INSERT INTO diagnosticos (id_paciente, sintomas, diagnostico, receta, indicaciones)
            VALUES (%s, %s, %s, %s, %s)
        '''
        params2 = (id_paciente, sintomas, diagnostico, receta, indicaciones)
        result = execute_query(query2, params2, commit=True)
        
        if result is not None:
            # Obtener nombre del paciente para el mensaje
            try:
                query = "SELECT nombre FROM expediente_pacientes WHERE id_paciente = %s"
                paciente_result = execute_query(query, (id_paciente,), fetch="one")
                nombre_paciente = paciente_result[0] if paciente_result else "el paciente"
            except:
                nombre_paciente = "el paciente"
                
            flash(f'Exploración y Receta guardada con éxito para {nombre_paciente}', 'success')
            return redirect(url_for('ConsultarP.pacientes'))
        else:
            flash('Error al guardar los datos', 'error')
            return redirect(url_for('MostrarExploracion.mostrar_exploracion', id_paciente=id_paciente))
        
    except Exception as e:
        flash(f'Error al guardar: {str(e)}', 'error')
        return redirect(url_for('MostrarExploracion.mostrar_exploracion', id_paciente=id_paciente))