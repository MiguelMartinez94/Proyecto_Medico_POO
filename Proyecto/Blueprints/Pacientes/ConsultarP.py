from flask import Blueprint, render_template, flash, session
from Cuerito import mysql
from auth import login_necesario



ConsultarP_bp = Blueprint('ConsultarP', __name__)

@ConsultarP_bp.route('/consultar_pacientes')
@login_necesario
def pacientes():
    
    id_medico = session.get('medico_id')
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM expediente_pacientes WHERE estado = 1 and id_medico = %s', (id_medico,))
        pacientes = cursor.fetchall()
        
        return render_template('consultar_pacientes.html', errores={}, pacientes=pacientes)

    except Exception as e:
        print('Error al consultar todo: ' + str(e))
        flash('Error al consultar pacientes.' + str(e))
        return render_template('consultar_pacientes.html', errores={}, pacientes={}, medicos = {})

    finally:
        cursor.close()

    