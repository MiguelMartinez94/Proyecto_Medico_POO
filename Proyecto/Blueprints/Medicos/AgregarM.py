from flask import Blueprint, render_template, request, flash, redirect, url_for
from Cuerito import mysql

AgregarM_bp = Blueprint('AgregarM', __name__)

@AgregarM_bp.route('/guardarMedico', methods=['POST'])
def guardar_medico():
    errores = {}

    rfc = request.form.get('rfc', '').strip()
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()
    cedula = request.form.get('cedula', '').strip()
    rol = request.form.get('rol', '').strip()
    password = request.form.get('password', '').strip()
    confirmPassword = request.form.get('confirmPassword', '').strip()

    if not nombre:
        errores['nombre'] = 'Nombre completo es obligatorio'
    if not rfc:
        errores['rfc'] = 'RFC es obligatorio'
    if not correo or '@' not in correo:
        errores['correo'] = 'Correo electrónico inválido'
    if not cedula:
        errores['cedula'] = 'Cédula profesional es obligatoria'
    if not rol:
        errores['rol'] = 'Rol es obligatorio'
    if not password or len(password) < 8:
        errores['password'] = 'La contraseña debe tener al menos 8 caracteres'
    if password != confirmPassword:
        errores['confirmPassword'] = 'Las contraseñas no coinciden'

    if not errores:
        try:
            query = '''
                INSERT INTO administracion_medicos (rfc, nombre, correo, cedula, rol, password, estado)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
            '''
            params = (rfc, nombre, correo, cedula, rol, password)
            mysql(query, params, commit=True)

            flash('Médico registrado correctamente en la base de datos')
            return redirect(url_for('AgregarM.agregar_medico'))

        except Exception as e:
            flash('Error al guardar el médico: ' + str(e))
            return redirect(url_for('AgregarM.agregar_medico'))

    return render_template('agregar_medico.html', errores=errores)

@AgregarM_bp.route('/agregar_medico', methods=['GET', 'POST'])
def agregar_medico():
    if request.method == 'POST':
        return guardar_medico()
    return render_template('agregar_medico.html')