from flask import Blueprint, render_template, request, flash, redirect, url_for, session
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
        # Usamos cursor tradicional para obtener resultados
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id_medico, nombre, password FROM administracion_medicos WHERE rfc = %s", 
            (rfc,)
        )
        medico = cursor.fetchone()
        cursor.close()

        if medico:
            # Convertir a diccionario para manejo más fácil
            medico_dict = {
                'id_medico': medico[0],
                'nombre': medico[1],
                'password': medico[2]
            }
            
            if medico_dict['password'] == password:
                flash(f'Bienvenido, {medico_dict["nombre"]}', 'success')
                
                # Almacenar información en sesión
                session['medico_id'] = medico_dict['id_medico']
                session['medico_nombre'] = medico_dict['nombre']
                
                return redirect(url_for('AdministrarM.administrar_medicos'))  # Redirigir a dashboard
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Médico no encontrado', 'error')

    except Exception as e:
        flash(f'Error en la autenticación: {str(e)}', 'error')

    return redirect(url_for('Login.mostrar_login'))