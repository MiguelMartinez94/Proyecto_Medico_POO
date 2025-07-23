from flask_mysqldb import MySQL

mysql = MySQL()

def init_mysql(app):
    app.config['MYSQL_HOST'] = "localhost"
    app.config['MYSQL_USER'] = "root"
    app.config['MYSQL_PASSWORD'] = "Kesadilla94"
    app.config['MYSQL_DB'] = "Proyecto_medicos"
    app.secret_key = 'mysecretkey'

    mysql.init_app(app)
    return mysql
