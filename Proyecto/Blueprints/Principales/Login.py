from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from functools import wraps
from Cuerito import mysql

Login_bp = Blueprint('Login', __name__)




@Login_bp.route('/', methods=['GET'])
def mostrar_login():
    return render_template('login.html')

@Login_bp.route('/login', methods=['POST'])
def procesar_login():
    
    rfc = request.form.get('txtRFC', '').strip()
    password = request.form.get('txtContrasena', '').strip()

    if not rfc or not password:
        flash('Por favor ingrese RFC y Contraseña', 'error')
        return redirect(url_for('Login.mostrar_login'))

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id_medico, nombre, password FROM administracion_medicos WHERE rfc = %s", 
            (rfc,)
        )
        medico = cursor.fetchone()
        cursor.close()

        if medico:
            
            medico_dict = {
                'id_medico': medico[0],
                'nombre': medico[1],
                'password': medico[2]
            }
            
            
            password_valida = False
            
            
            if medico_dict['password'].startswith(('pbkdf2:', 'scrypt:')):
                password_valida = check_password_hash(medico_dict['password'], password)
                
            else:
                
                password_valida = medico_dict['password'] == password
            
            if password_valida:
                flash(f'Bienvenido, {medico_dict["nombre"]}', 'success')
                
                session['medico_id'] = medico_dict['id_medico']
                session['medico_nombre'] = medico_dict['nombre']
                
                return redirect(url_for('AdministrarM.administrar_medicos', id_medico = medico[0]))
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Médico no encontrado', 'error')

    except Exception as e:
        flash(f'Error en la autenticación: {str(e)}', 'error')

    return redirect(url_for('Login.mostrar_login'))


@Login_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('Login.mostrar_login'))