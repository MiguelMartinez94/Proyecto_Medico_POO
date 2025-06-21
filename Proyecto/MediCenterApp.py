from flask import Flask, jsonify, render_template, request, url_for, flash, redirect

#Aqui se añaden los app

app = Flask(__name__)
app.secret_key ='mysecretkey'

#Apartir de aqui se añaden rutas

@app.route('/')
def home():
    return render_template('login.html')

#fin del apartado para añadir rutas
if __name__ == '__main__':
    app.run(port = 3000, debug = True)