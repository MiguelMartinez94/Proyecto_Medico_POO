from flask import Blueprint, render_template, flash
from Cuerito import mysql

AdministrarM_bp = Blueprint('AdministrarM', __name__)

@AdministrarM_bp.route('/administrar_medicos')
def administrar_medicos():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM administracion_medicos WHERE estado = 1')
        medicos = cursor.fetchall()
        return render_template('administrar_medicos.html', medicos=medicos)
    except Exception as e:
        flash('Error al obtener los médicos: ' + str(e))
        return render_template('administrar_medicos.html', medicos=[])
    finally:
        cursor.close()
