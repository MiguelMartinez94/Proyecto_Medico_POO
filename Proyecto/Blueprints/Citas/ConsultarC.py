from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from datetime import datetime, timedelta
from Cuerito import mysql
from auth import login_necesario

ConsultarCitas_bp = Blueprint('ConsultarCitas', __name__)

@ConsultarCitas_bp.route('/consultar_citas')
@login_necesario
def consultar_citas():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
                            SELECT 
                                c.id_cita,
                                ep.nombre as nombre_paciente,
                                am.nombre as nombre_medico,
                                c.fecha,
                                c.hora
                            FROM citas c
                            INNER JOIN expediente_pacientes ep ON c.id_paciente = ep.id_paciente
                            INNER JOIN administracion_medicos am ON c.id_medico = am.id_medico
                            ORDER BY c.fecha DESC, c.hora DESC
                        ''')
        
        citas = cursor.fetchall()
        return render_template('consultar_citas.html', citas=citas)
    
    
    except Exception as e:
        
        
        flash('Error al obtener las citas: ' + str(e))
        return render_template('consultar_citas.html', citas=[])
    
    
    finally:
        if cursor is not None:
            cursor.close()





