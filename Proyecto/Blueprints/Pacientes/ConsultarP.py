from flask import Blueprint, render_template, flash
from Cuerito import mysql

ConsultarP_bp = Blueprint('ConsultarP', __name__)

@ConsultarP_bp.route('/consultar_pacientes')
def pacientes():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM expediente_pacientes WHERE state = 1')
        pacientes = cursor.fetchall()
        return render_template('consultar_pacientes.html', errores={}, pacientes=pacientes)

    except Exception as e:
        print('Error al consultar todo: ' + str(e))
        flash('Error al consultar pacientes.', 'error')
        return render_template('consultar_pacientes.html', errores={}, pacientes={})

    finally:
        cursor.close()
