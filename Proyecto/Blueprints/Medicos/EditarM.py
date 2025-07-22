from flask import Blueprint, request, render_template, flash, redirect, url_for
from Cuerito import mysql

EditarM_bp = Blueprint('EditarM', __name__)

@EditarM_bp.route('/editar_medico/<rfc>', methods=['POST'])
def editar_medico(rfc):
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()
    cedula = request.form.get('cedula', '').strip()
    rol = request.form.get('rol', '').strip()
    password = request.form.get('password', '').strip()
    confirmPassword = request.form.get('confirmPassword', '').strip()

    errores = {}

    if not nombre:
        errores['nombre'] = 'El nombre es obligatorio'
    if not correo or '@' not in correo:
        errores['correo'] = 'Correo electrónico inválido'
    if not cedula:
        errores['cedula'] = 'La cédula profesional es obligatoria'
    if not rol:
        errores['rol'] = 'El rol es obligatorio'
    if not password or len(password) < 8:
        errores['password'] = 'La contraseña debe tener al menos 8 caracteres'
    if password != confirmPassword:
        errores['confirmPassword'] = 'Las contraseñas no coinciden'

    if errores:
        return render_template(
            'actualizar_medico.html',
            errores=errores,
            rfc=rfc,
            nombre=nombre,
            correo=correo,
            cedula=cedula,
            rol=rol,
            password=password
        )

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE administracion_medicos 
            SET nombre=%s, correo=%s, cedula=%s, rol=%s, password=%s 
            WHERE rfc=%s
        ''', (nombre, correo, cedula, rol, password, rfc))
        mysql.connection.commit()
        flash('Médico actualizado correctamente')
        return redirect(url_for('AdministrarM.administrar_medicos'))
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al actualizar el médico: ' + str(e))
        return redirect(url_for('EditarM.editar_medico', rfc=rfc))
    finally:
        cursor.close()
