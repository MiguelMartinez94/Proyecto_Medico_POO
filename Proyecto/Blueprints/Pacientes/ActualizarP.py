from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from Cuerito import mysql
from auth import login_necesario

ActualizarP_bp = Blueprint('ActualizarP', __name__)

@ActualizarP_bp.route('/actualizar_paciente/<int:id>')
@login_necesario
def consulta_actualizar(id):
    
    
    id_medico = session.get('medico_id')
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('select * from expediente_pacientes where id_paciente = %s', (id,))
        
        paciente = cursor.fetchone()
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM administracion_medicos WHERE estado = 1')
        medicos = cursor.fetchall()
        

        if paciente:
            cursor.execute('SELECT * FROM expediente_pacientes WHERE estado = 1 and id_medico = %s', (id_medico,))
            consultaTodo = cursor.fetchall()
            return render_template('consultar_pacientes.html', paciente=paciente, pacientes=consultaTodo, medicos = medicos, errores={})
        else:
            flash('Paciente no encontrado')
            return redirect(url_for('ConsultarP.pacientes'))

    except Exception as e:
        print('Error al consultar paciente: ' + str(e))
        flash('Error al consultar paciente')
        return redirect(url_for('ConsultarP.pacientes'))

    finally:
        cursor.close()


@ActualizarP_bp.route('/modificacion_paciente', methods=['POST'])
def guardarPacienteActualizado():
    errores = {}

    idUpdatePaciente = request.form.get('id_paciente', '').strip()
    nMedico = request.form.get('n_medico_atiende', '').strip()
    nPaciente = request.form.get('n_paciente', '').strip()
    nFecha = request.form.get('n_fecha_nacimiento', '').strip()
    nEnfermedades = request.form.get('n_enfermedades_cronicas', '').strip()
    nAlergias = request.form.get('n_alergias', '').strip()
    nAntecedentes = request.form.get('n_antecedentes', '').strip()

    if not idUpdatePaciente:
        errores['id_paciente'] = 'ID del paciente es requerido'
    if not nMedico:
        errores['n_medico_atiende'] = 'ID del médico obligatorio'
    if not nPaciente:
        errores['n_paciente'] = 'Nombre del paciente obligatorio'
    if not nFecha:
        errores['n_fecha_nacimiento'] = 'Fecha de nacimiento obligatoria'
    if not nEnfermedades:
        errores['n_enfermedades_cronicas'] = 'En caso de no tener enfermedades crónicas indicar "Ninguna"'
    if not nAlergias:
        errores['n_alergias'] = 'En caso de no tener alergias indicar "Ninguna"'
    if not nAntecedentes:
        errores['n_antecedentes'] = 'En caso de no tener antecedentes familiares indicar "Ninguno"'

    if not errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('''
                UPDATE expediente_pacientes 
                SET id_medico = %s, nombre = %s, fecha_nacimiento = %s, 
                    enfermedades_cronicas = %s, alergias = %s, antecedentes_familiares = %s 
                WHERE id_paciente = %s
            ''', (nMedico, nPaciente, nFecha, nEnfermedades, nAlergias, nAntecedentes, idUpdatePaciente))
            mysql.connection.commit()
            flash('Paciente actualizado exitosamente')
            return redirect(url_for('ConsultarP.pacientes'))

        except Exception as e:
            mysql.connection.rollback()
            flash(f'Algo falló al guardar los datos del paciente: {str(e)}')
            return redirect(url_for('ConsultarP.pacientes'))

        finally:
            cursor.close()

    
