from flask import Blueprint, flash, redirect, url_for
from Cuerito import mysql

EliminarM_bp = Blueprint('EliminarM', __name__)

@EliminarM_bp.route('/eliminar_medico/<rfc>', methods=['POST'])
def eliminar_medico(rfc):
    try:
        cursor = mysql.connection.cursor()
        # Verificar si el médico existe
        cursor.execute('SELECT * FROM administracion_medicos WHERE rfc = %s', (rfc,))
        if not cursor.fetchone():
            flash('Médico no encontrado', 'error')
            return redirect(url_for('AdministrarM.administrar_medicos'))
        
        cursor.execute('UPDATE administracion_medicos SET estado = 0 WHERE rfc = %s', (rfc,))
        mysql.connection.commit()
        flash('Médico eliminado correctamente')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al eliminar médico: {str(e)}', 'error')
    finally:
        cursor.close()
    
    return redirect(url_for('AdministrarM.administrar_medicos'))