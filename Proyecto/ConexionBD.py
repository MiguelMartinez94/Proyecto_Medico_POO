from flask_mysqldb import MySQL

mysql = MySQL()

def init_mysql(app):
    app.config['MYSQL_HOST'] = "localhost"
    app.config['MYSQL_USER'] = "root"
    app.config['MYSQL_PASSWORD'] = "Emiliano04"
    app.config['MYSQL_DB'] = "proyecto_medico"
    app.secret_key = 'mysecretkey'

    mysql.init_app(app)
    return mysql
