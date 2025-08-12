from flask import Blueprint, render_template, request, flash, redirect, url_for
from Cuerito import mysql
from auth import login_necesario

RegistrarP_bp = Blueprint('RegistrarP', __name__)

@RegistrarP_bp.route('/registrar_paciente')
@login_necesario
def vistaRegistroPaciente():
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM administracion_medicos WHERE estado = 1')
    medicos = cursor.fetchall()
    cursor.close() 

    return render_template('registrar_pacientes.html',  medicos = medicos)

@RegistrarP_bp.route('/registrar_pacientes', methods=['GET','POST'])
@login_necesario
def registrarPaciente():
    errores = {}
    
    
    medico = request.form.get('medico_atiende', '').strip()
    paciente = request.form.get('paciente', '').strip()
    fecha = request.form.get('fecha_nacimiento', '').strip()
    enfermedades = request.form.get('enfermedades_cronicas', '').strip()
    alergias = request.form.get('alergias', '').strip()
    antecedentes = request.form.get('antecedentes', '').strip()

    if not medico:
        errores['medico_atiende'] = 'ID del médico obligatorio'
    if not paciente:
        errores['paciente'] = 'Nombre del paciente obligatorio'
    if not fecha:
        errores['fecha_nacimiento'] = 'Fecha de nacimiento obligatoria'
    if not enfermedades:
        errores['enfermedades_cronicas'] = 'En caso de no tener enfermedades crónicas indicar "Ninguna"'
    if not alergias:
        errores['alergias'] = 'En caso de no tener alergias indicar "Ninguna"'
    if not antecedentes:
        errores['antecedentes'] = 'En caso de no tener antecedentes familiares indicar "Ninguno"'

    if not errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('''
                INSERT INTO expediente_pacientes (
                    id_medico, nombre, fecha_nacimiento, enfermedades_cronicas, alergias, antecedentes_familiares
                ) VALUES (%s, %s, %s, %s, %s, %s)
            ''', (medico, paciente, fecha, enfermedades, alergias, antecedentes))
            mysql.connection.commit()
            flash('Paciente registrado exitosamente')
            return redirect(url_for('ConsultarP.pacientes'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Algo falló al guardar los datos del paciente: {str(e)}', 'error')
            return redirect(url_for('RegistrarP.vistaRegistroPaciente'))
        finally:
            cursor.close()

    return render_template('registrar_pacientes.html', errores=errores,)
