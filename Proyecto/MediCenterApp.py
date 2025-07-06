#Proyecto de POO MediCenter
#Aqui se añaden imports

from flask import Flask, jsonify, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL
import MySQLdb

#Aqui se añaden los app

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = ""
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
    return render_template('login.html')


@app.route('/medicos') #Ruta medicos
def medicos():
    return render_template('medicos.html')

@app.route('/exploracion_diagnostico')
def expDiag():
    return render_template('cita_exploracion_diagnostico.html')


#CRUD DE PACIENTES

'''
#Ruta de consulta de pacientes

@app.route('/consultar_pacientes') 
def pacientes():
    
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('select * from expediente_pacientes where state = 1')
        consultaTodo = cursor.fetchall()
        return render_template('consultar_pacientes.html', errores={}, pacientes = consultaTodo)
        
    except Exception as e:
        print('Error al consultar todo: ' + e)
        return render_template('consultar_pacientes.html', errores={}, pacientes = {})
        
    finally:
        cursor.close()
        

#Ruta para regitsrar pacientes    
@app.route('/registrar_pacientes', methods=['POST'])
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
            return redirect(url_for('registrarPacientes'))
            
        except Exception as e:
            mysql.connection.rollback()
            flash( f'Algo falló al guardar los datos del paciente: {str(e)}')
            return redirect(url_for('resgistrarPacientes'))
            
        finally:
            
            cursor.close()
    
    return render_template('registrar_pacientes.html', errores = errores)

#Ruta de actualizar pacientes
@app.route('/actualizar_paciente/<int:id>')
def consulta_actualizar(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('select * from expediente_pacientes where id_paciente = %s', (id,))
        paciente = cursor.fetchone()
        return render_template('consultar_pacientes.html', paciente=paciente)
        
    except Exception as e:
        print('Error al consultar todo: ' + e)
        return render_template('update.html', errores={}, pacientes = {})
        
    finally:
        cursor.close()
        
    
@app.route('/modificacion_paciente', methods=['POST'])
def guardarPacienteActualizado():
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
    #Intentamos ejecutar el UPDATE
    
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('update expediente_pacientes set id_medico = %s, nombre = %s, fecha_nacimiento = %s, enfermedades_cronicas = %s, alergias = %s, antecedentes_familiares = %s', (medico, paciente, fecha, enfermedades, alergias, antecedentes))
            mysql.connection.commit()
            flash('Paciente actualizado exitosamente')
            return redirect(url_for('pacientes'))
            
        except Exception as e:
            mysql.connection.rollback()
            flash( f'Algo falló al guardar los datos del paciente: {str(e)}')
            return redirect(url_for('pacientes'))
            
        finally:
            
            cursor.close()
    
    return render_template('consultar_pacientes.html', paciente = (medico, paciente, fecha, enfermedades, alergias, antecedentes), errores = errores )

    '''

@app.route('/consultar_citas')
def citas():
    return render_template('consultar_citas.html')



@app.route('/agregar_medico', methods=['GET', 'POST'])
def agregar_medico():
    return render_template('agregar_medico.html')

@app.route('/administrar_medicos')
def administrar_medicos():
    return render_template('administrar_medicos.html')
@app.route('/editar_medico/<rfc>', methods=['GET', 'POST'])
def editar_medico(rfc):
    # Por ahora solo mostramos un mensaje
    return f"Editar médico con RFC: {rfc}" 

@app.route('/eliminar_medico/<rfc>')
def eliminar_medico(rfc):
    # Por ahora solo mostramos un mensaje
    return f"Eliminar médico con RFC: {rfc}"

#Fin del apartado para añadir rutas

if __name__ == '__main__':
    app.run(port = 3000, debug = True)