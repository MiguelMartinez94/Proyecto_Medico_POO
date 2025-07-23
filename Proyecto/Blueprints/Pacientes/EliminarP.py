from flask import Blueprint, redirect, url_for, flash, request
from Cuerito import mysql

EliminarP_bp = Blueprint('EliminarP', __name__)

@EliminarP_bp.route('/eliminar_paciente/<int:id>', methods=['POST'])
def eliminar_paciente(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE expediente_pacientes SET estado = 0 WHERE id_paciente = %s', (id,))
        mysql.connection.commit()
        flash('Paciente eliminado correctamente')
        return redirect(url_for('ConsultarP.pacientes'))
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al eliminar el paciente: ' + str(e))
        return redirect(url_for('ConsultarP.pacientes'))
    finally:
        cursor.close()
