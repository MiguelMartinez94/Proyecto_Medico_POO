from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from Cuerito import mysql
from auth import login_necesario

AgregarCita_bp = Blueprint('AgregarCita', __name__)

@AgregarCita_bp.route('/registrarCitas', methods=['POST'])
@login_necesario
def registrarCitas():
    cursor = None
    errores = {}
    
    paciente_id = request.form.get('paciente_id', '').strip()
    medico_id = request.form.get('medico_id', '').strip()
    fecha = request.form.get('fecha_cita', '').strip()
    hora = request.form.get('hora_cita', '').strip()
    
    
    if not paciente_id:
        errores['paciente_id'] = 'ID del paciente es requerido'
    
    if not medico_id:
        errores['medico_id'] = 'Debe seleccionar un médico'
    
    if not fecha:
        errores['fecha_cita'] = 'La fecha de la cita es requerida'
    else:
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            fecha_actual = datetime.now().date()
            if fecha_obj < fecha_actual:
                errores['fecha_cita'] = 'La fecha de la cita no puede ser en el pasado'
        except ValueError:
            errores['fecha_cita'] = 'Formato de fecha inválido'
    
    if not hora:
        errores['hora_cita'] = 'La hora de la cita es requerida'
    else:
        try:
            datetime.strptime(hora, '%H:%M')
        except ValueError:
            errores['hora_cita'] = 'Formato de hora inválido'
    
    
    if not errores:
        try:
            cursor = mysql.connection.cursor()
            
            
            cursor.execute('''
                SELECT COUNT(*) 
                FROM citas 
                WHERE id_medico = %s 
                AND fecha = %s 
                AND hora = %s
            ''', (medico_id, fecha, hora))
            
            conflicto = cursor.fetchone()[0]
            
            if conflicto > 0:
                flash('El médico no está disponible en esa fecha y hora. Por favor, selecciona otro horario.', 'warning')
                return redirect(url_for('MostrarPacienteCitas.mostrar_paciente_citas', id_paciente=paciente_id))
            
            
            cursor.execute('''
                INSERT INTO citas (id_paciente, id_medico, fecha, hora) 
                VALUES (%s, %s, %s, %s)
            ''', (paciente_id, medico_id, fecha, hora))
            
            mysql.connection.commit()
            flash('Cita registrada exitosamente', 'success')
            return redirect(url_for('MostrarPacienteCitas.mostrar_paciente_citas', id_paciente=paciente_id))
            
        except Exception as e:
            mysql.connection.rollback()
            flash('Error al registrar la cita: ' + str(e), 'error')
            return redirect(url_for('MostrarPacienteCitas.mostrar_paciente_citas', id_paciente=paciente_id))
        finally:
            if cursor is not None:
                cursor.close()
    
    return redirect(url_for('MostrarPacienteCitas.mostrar_paciente_citas', id_paciente=paciente_id))