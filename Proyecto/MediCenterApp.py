#Proyecto de POO MediCenter
#Aqui se añaden imports

from flask import Flask, jsonify, render_template, request, url_for, flash, redirect

#Aqui se añaden los app

app = Flask(__name__)
app.secret_key ='mysecretkey'

#Apartir de aqui se añaden rutas

@app.route('/') #Ruta principal
def home():
    return render_template('login.html')

@app.route('/cdp') #Ruta medicos
def cdp():
    return render_template('cdp.html')

@app.route('/medicos') #Ruta medicos
def medicos():
    return render_template('medicos.html')

@app.route('/exploracion_diagnostico')
def expDiag():
    return render_template('cita_exploracion_diagnostico.html')

@app.errorhandler(404) #Ruta try-catch 404
def PagNoE(e):
    return 'EY! Aprenda a escribir :)'

@app.errorhandler(405) #Ruta try-catch 405
def PagNoE(e):
    return 'EY! Revisa el metodo de envio :)'

#Fin del apartado para añadir rutas

if __name__ == '__main__':
    app.run(port = 3000, debug = True)