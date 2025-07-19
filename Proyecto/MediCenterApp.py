#Proyecto de POO MediCenter
#Aqui se añaden imports

from flask import Flask, jsonify, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL
import MySQLdb



app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Kesadilla94"
app.config['MYSQL_DB'] = "proyecto_medico"
#app.config['MYSQL_PORT'] = 3306
app.secret_key ='mysecretkey'

mysql = MySQL(app)


@app.errorhandler(404) #Ruta try-catch 404
def PagNoE(e):
    return 'EY! Aprenda a escribir :)'

@app.errorhandler(405) #Ruta try-catch 405
def PagNoE(e):
    return 'EY! Revisa el metodo de envio :)'


#Comprobación de la conexión a la base de datos
@app.route('/DBCheck')
def DB_check():
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute('Select 1')
        return jsonify({'status':'ok', 'message':'Conectado con exito'}), 200        
        
        
    except MySQLdb.MySQLError as e:
        return jsonify({'status':'error', 'message':str(e)}), 500  


#Apartir de aqui se añaden rutas

@app.route('/') #Ruta principal
def home():
    return render_template('consultar_citas.html')

#CRUD DE MEDICOS
# Ruta para guardar médico
@app.route('/guardarMedico', methods=['POST'])
def guardar_medico():
    errores = {}

    # Obtener los datos del formulario (solo los requeridos)
    rfc = request.form.get('rfc', '').strip()
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()
    cedula = request.form.get('cedula', '').strip()
    rol = request.form.get('rol', '').strip()
    password = request.form.get('password', '').strip()
    confirmPassword = request.form.get('confirmPassword', '').strip()

    # Validación de los datos
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
            cursor = mysql.connection.cursor()
            cursor.execute(
                'INSERT INTO administracion_medicos (rfc, nombre, correo, cedula, rol, password) VALUES (%s, %s, %s, %s, %s, %s)',
                (rfc, nombre, correo, cedula, rol, password)
            )
            mysql.connection.commit()
            flash('Médico registrado correctamente en la base de datos')
            return redirect(url_for('administrar_medicos'))
        except Exception as e:
            mysql.connection.rollback()
            flash('Error al guardar el médico: ' + str(e))
            return redirect(url_for('agregar_medico'))
        finally:
            cursor.close()

    return render_template('agregar_medico.html', errores=errores)

@app.route('/agregar_medico', methods=['GET', 'POST'])
def agregar_medico():
    if request.method == 'POST':
        return guardar_medico()
    return render_template('agregar_medico.html')

@app.route('/administrar_medicos')
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

# Ruta para editar médico
@app.route('/editar_medico/<rfc>', methods=['POST'])
def editar_medico(rfc):
    # Obtener los datos del formulario para la actualización
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()
    cedula = request.form.get('cedula', '').strip()
    rol = request.form.get('rol', '').strip()
    password = request.form.get('password', '').strip()
    confirmPassword = request.form.get('confirmPassword', '').strip()

    errores = {}

    # Validaciones de los campos
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
        # Si hay errores, volvemos a mostrar el formulario con los errores y los datos previos
        return render_template('actualizar_medico.html', errores=errores, rfc=rfc,nombre=nombre, correo=correo, cedula=cedula, rol=rol, password=password)

    # Si no hay errores, actualizamos el registro
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE administracion_medicos SET nombre=%s, correo=%s, cedula=%s, rol=%s, password=%s WHERE rfc=%s''',(nombre, correo, cedula, rol, password, rfc))
        mysql.connection.commit()
        flash('Médico actualizado correctamente')
        return redirect(url_for('administrar_medicos'))  # Redirigir a la página de administración
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al actualizar el médico: ' + str(e))
        return redirect(url_for('editar_medico', rfc=rfc))
    finally:
        cursor.close()

# Ruta para eliminar médico
@app.route('/eliminar_medico/<rfc>', methods=['POST'])
def eliminar_medico(rfc):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE administracion_medicos SET estado = 0 WHERE rfc = %s', (rfc,))
        mysql.connection.commit()
        flash('Médico eliminado correctamente')
        return redirect(url_for('administrar_medicos'))
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al eliminar el médico: ' + str(e))
        return redirect(url_for('administrar_medicos'))
    finally:
        cursor.close()





#CRUD DE PACIENTES

#Ruta de consulta de pacientes

@app.route('/consultar_pacientes') 
def pacientes():
    
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('select * from expediente_pacientes where estado = 1')
        pacientes = cursor.fetchall()
        return render_template('consultar_pacientes.html', errores={}, pacientes= pacientes)
        
    except Exception as e:
        print('Error al consultar todo: ' + e)
        return render_template('consultar_pacientes.html', errores={}, pacientes = {})
        
    finally:
        cursor.close()
        

#Ruta para regitsrar pacientes  

@app.route('/registrar_paciente')
def vistaRegistroPaciente():
    return render_template('registrar_pacientes.html')


@app.route('/registrar_pacientes', methods = ['POST'])
def registrarPaciente():
    
    #lista de errores
    
    errores = {}
    
    #Obtener los datos a insertar
    
    medico = request.form.get('medico_atiende', '').strip()
    paciente = request.form.get('paciente', '')
    fecha = request.form.get('fecha_nacimiento', '')
    enfermedades = request.form.get('enfermedades_cronicas', '')
    alergias = request.form.get('alergias', '')
    antecedentes = request.form.get('antecedentes', '')
    
    if not medico:
        errores['medico_atiende'] = 'ID del médico obligatorio'
        
    if not paciente:
        errores['paciente'] = 'Nombre del paciente obligatorio'
        
    if not fecha:
        errores['fecha_nacimiento'] = 'fecha de nacimiento obligatoria'
        
    if not enfermedades:
        errores['enfermedades_cronicas'] = 'En caso de no tener enfermedades crónicas indicar "Ninguna"'
        
    if not alergias:
        errores['alergias'] = 'En caso de no tener alergias indicar "Ninguna"'
        
    elif not antecedentes:
        errores['antecedentes'] = 'En caso de no tener antecedentes familiares indicar "Ninguno"'
        
        
    if not errores:
        
    #Intentamos ejecutar el INSERT
    
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('insert into expediente_pacientes(id_medico, nombre, fecha_nacimiento, enfermedades_cronicas, alergias, antecedentes_familiares) values(%s, %s, %s, %s, %s, %s)', (medico, paciente, fecha, enfermedades, alergias, antecedentes))
            mysql.connection.commit()
            flash('Paciente registrado exitosamente')
            return redirect(url_for('pacientes'))
            
        except Exception as e:
            mysql.connection.rollback()
            flash( f'Algo falló al guardar los datos del paciente: {str(e)}')
            return redirect(url_for('vistaRegistroPaciente'))
            
        finally:
            
            cursor.close()
    
    return render_template('registrar_pacientes.html', errores = errores)





@app.route('/actualizar_paciente/<int:id>')
def consulta_actualizar(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('select * from expediente_pacientes where id_paciente = %s', (id,))
        paciente = cursor.fetchone()
        
        
        if paciente:
            cursor.execute('select * from expediente_pacientes where estado = 1')
            consultaTodo = cursor.fetchall()
            return render_template('consultar_pacientes.html', paciente=paciente, pacientes=consultaTodo, errores={})
        else:
            flash('Paciente no encontrado')
            return redirect(url_for('pacientes'))
            
    except Exception as e:
        print('Error al consultar paciente: ' + str(e))
        flash('Error al consultar paciente')
        return redirect(url_for('pacientes'))
        
    finally:
        cursor.close()


@app.route('/modificacion_paciente', methods=['POST'])
def guardarPacienteActualizado():
    # Lista de errores
    errores = {}
    
    # Obtener los datos a modificar
    idUpdatePaciente = request.form.get('id_paciente', '').strip() 
    nMedico = request.form.get('n_medico_atiende', '').strip()
    nPaciente = request.form.get('n_paciente', '')
    nFecha = request.form.get('n_fecha_nacimiento', '').strip()
    nEnfermedades = request.form.get('n_enfermedades_cronicas', '')
    nAlergias = request.form.get('n_alergias', '')
    nAntecedentes = request.form.get('n_antecedentes', '')
    
    # Validaciones
    if not idUpdatePaciente:
        errores['id_paciente'] = 'ID del paciente es requerido'
        
    if not nMedico:
        errores['n_medico_atiende'] = 'ID del médico obligatorio'
        
    if not nPaciente:
        errores['n_paciente'] = 'Nombre del paciente obligatorio'
        
    if not nFecha:
        errores['n_fecha_nacimiento'] = 'Fecha de nacimiento obligatoria'
        
    if not nEnfermedades:
        errores['n_enfermedades_cronicas'] = 'En caso de no tener enfermedades crónicas indicar "Ninguna"'
        
    if not nAlergias:
        errores['n_alergias'] = 'En caso de no tener alergias indicar "Ninguna"'
        
    if not nAntecedentes:  
        errores['n_antecedentes'] = 'En caso de no tener antecedentes familiares indicar "Ninguno"'
        
    if not errores:
        
        # Intentamos ejecutar el UPDATE
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('''UPDATE expediente_pacientes 
                            SET id_medico = %s, nombre = %s, fecha_nacimiento = %s, 
                            enfermedades_cronicas = %s, alergias = %s, antecedentes_familiares = %s 
                            WHERE id_paciente = %s''', 
                            (nMedico, nPaciente, nFecha, nEnfermedades, nAlergias, nAntecedentes, idUpdatePaciente))
            mysql.connection.commit()
            flash('Paciente actualizado exitosamente')
            return redirect(url_for('pacientes'))
            
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Algo falló al guardar los datos del paciente: {str(e)}')
            return redirect(url_for('pacientes'))
            
        finally:
            cursor.close()

    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('select * from expediente_pacientes where estado = 1')
        consultaTodo = cursor.fetchall()
        paciente = (idUpdatePaciente, nMedico, nPaciente, nFecha, nEnfermedades, nAlergias, nAntecedentes)
        return render_template('consultar_pacientes.html', paciente=paciente, pacientes=consultaTodo, errores=errores)
    except Exception as e:
        print('Error al consultar pacientes: ' + str(e))
        return redirect(url_for('pacientes'))
    finally:
        cursor.close()    
        
        
        
# Ruta para eliminar paciente
@app.route('/eliminar_paciente/<int:id>', methods=['POST'])
def eliminar_paciente(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE expediente_pacientes SET estado = 0 WHERE id_paciente = %s', (id,))
        mysql.connection.commit()
        flash('Paciente eliminado correctamente')
        return redirect(url_for('pacientes'))
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al eliminar el paciente: ' + str(e))
        return redirect(url_for('pacientes'))
    finally:
        cursor.close()


@app.route('/consultar_citas')
def citas():
    return render_template('consultar_citas.html')

@app.route('/exploracion_diagnostico')
def expDiag():
    return render_template('cita_exploracion_diagnostico.html')

@app.route('/login')
def login():
    return render_template('login.html')

#Fin del apartado para añadir rutas

if __name__ == '__main__':
    app.run(port = 3000, debug = True)