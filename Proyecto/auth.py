from functools import wraps
from flask import session, redirect, url_for, flash

def login_necesario(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'medico_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('Login.mostrar_login'))
        return f(*args, **kwargs)
    return decorated_function
