#Proyecto de POO MediCenter

from flask import Flask, jsonify, render_template, request, url_for, flash, redirect

from ConexionBD import init_mysql

from Blueprints.Principales.DBCheck import DBCheck_bp
from Blueprints.Principales.Login import Login_bp

from Blueprints.Medicos.AgregarM import AgregarM_bp
from Blueprints.Medicos.AdministrarM import AdministrarM_bp
from Blueprints.Medicos.EliminarM import EliminarM_bp
from Blueprints.Medicos.EditarM import EditarM_bp

from Blueprints.Pacientes.RegistrarP import RegistrarP_bp
from Blueprints.Pacientes.ConsultarP import ConsultarP_bp
from Blueprints.Pacientes.EliminarP import EliminarP_bp
from Blueprints.Pacientes.ActualizarP import ActualizarP_bp


app = Flask(__name__)
mysql = init_mysql(app)

#Blueprints Generales

app.register_blueprint(DBCheck_bp)

app.register_blueprint(Login_bp)

#Blueprints de MEDICOS

app.register_blueprint(AgregarM_bp)

app.register_blueprint(AdministrarM_bp)

app.register_blueprint(EliminarM_bp)

app.register_blueprint(EditarM_bp)

#Blueprints de PACIENTES

app.register_blueprint(RegistrarP_bp)

app.register_blueprint(ConsultarP_bp)

app.register_blueprint(EliminarP_bp)

app.register_blueprint(ActualizarP_bp)

#Apartir de aqui se añaden rutas

@app.route('/consultar_citas')
def citas():
    return render_template('consultar_citas.html')

@app.route('/exploracion_diagnostico')
def expDiag():
    return render_template('cita_exploracion_diagnostico.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.errorhandler(404) #Ruta try-catch 404
def PagNoE(e):
    return 'EY! Aprenda a escribir :)'

@app.errorhandler(405) #Ruta try-catch 405
def PagNoE(e):
    return 'EY! Revisa el metodo de envio :)'

#Fin del apartado para añadir rutas

if __name__ == '__main__':
    app.run(port = 3000, debug = True)