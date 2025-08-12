from flask import Blueprint, render_template, request, flash, redirect, url_for
from Cuerito import mysql
from auth import login_necesario

MostrarPacienteCitas_bp = Blueprint('MostrarPacienteCitas', __name__)

@MostrarPacienteCitas_bp.route('/mostrar_paciente_citas')
@login_necesario
def mostrar_paciente_citas():
    
    cursor = None
    try:
        id_paciente = request.args.get('id_paciente')
        
        if not id_paciente:
            flash('No se especificó un paciente', 'warning')
            return redirect(url_for('ConsultarP.pacientes'))
        
        cursor = mysql.connection.cursor()
        
        
        cursor.execute('SELECT id_paciente, nombre FROM expediente_pacientes WHERE id_paciente = %s', (id_paciente,))
        paciente = cursor.fetchone()
        
        if not paciente:
            flash('Paciente no encontrado', 'error')
            return redirect(url_for('ConsultarP.pacientes'))
        
        
        
        
        cursor.execute('SELECT id_medico, nombre FROM administracion_medicos WHERE estado = 1')
        medicos = cursor.fetchall()
        
        
        cursor.execute('''
                            SELECT 
                                ep.nombre as nombre_paciente,
                                am.nombre as nombre_medico,
                                c.fecha,
                                c.hora
                            FROM citas c
                            INNER JOIN expediente_pacientes ep ON c.id_paciente = ep.id_paciente
                            INNER JOIN administracion_medicos am ON c.id_medico = am.id_medico
                            WHERE c.id_paciente = %s
                            ORDER BY c.fecha DESC, c.hora DESC
                        ''', (id_paciente,))
        
        citas = cursor.fetchall()
        
        return render_template('consultar_citas.html', 
                                paciente =paciente,
                                medicos=medicos,
                                citas=citas)
            
    except Exception as e:
        
        flash('Error al obtener información: ' + str(e))
        return redirect(url_for('ConsultarP.pacientes'))
    

    finally:
        if cursor is not None:
            cursor.close()