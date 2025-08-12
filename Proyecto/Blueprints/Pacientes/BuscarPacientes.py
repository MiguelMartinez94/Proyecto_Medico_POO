from flask import Blueprint, render_template, flash, session, request
from Cuerito import mysql
from auth import login_necesario

BuscarPacientes_bp = Blueprint('BuscarPacientes', __name__)

@BuscarPacientes_bp.route('/buscar_pacientes', methods=['POST'])
@login_necesario
def buscar_pacientes():
    cursor = None
    
    id_medico = session.get('medico_id')
    nombre_paciente = request.form.get('nombre_paciente', '').strip()
    
    try:
        cursor = mysql.connection.cursor()
        
        
        
        cursor.execute('''
                SELECT * FROM expediente_pacientes 
                WHERE estado = 1 
                AND id_medico = %s 
                AND nombre LIKE %s
                ORDER BY nombre desc
            ''', (id_medico, f'%{nombre_paciente}%'))
    
        pacientes = cursor.fetchall()
        
        
        return render_template('consultar_pacientes.html', 
                                errores={}, 
                                pacientes=pacientes,
                                busqueda=nombre_paciente)

    except Exception as e:
        print('Error al buscar pacientes: ' + str(e))
        flash('Error al buscar pacientes: ' + str(e))
        return render_template('consultar_pacientes.html', 
                                errores={}, 
                                pacientes=[],)

    finally:
        if cursor is not None:
            cursor.close()