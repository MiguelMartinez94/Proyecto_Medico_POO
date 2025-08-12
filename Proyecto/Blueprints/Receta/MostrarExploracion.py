from flask import Blueprint, render_template, request, flash, redirect, url_for
from Cuerito import execute_query
from auth import login_necesario

MostrarExploracion_bp = Blueprint('MostrarExploracion', __name__)

def obtener_nombre_paciente(id_paciente):
    
    try:
        query = "SELECT nombre FROM expediente_pacientes WHERE id_paciente = %s"
        result = execute_query(query, (id_paciente,), fetch="one")
        
        if result:
            return {
                        'id': id_paciente,
                        'nombre': result[0]
                    }
        return None
    
    except Exception as e:
        print(f"Error al obtener nombre del paciente: {e}")
        return None

@MostrarExploracion_bp.route('/mostrar_exploracion')
@login_necesario
def mostrar_exploracion():
    id_paciente = request.args.get('id_paciente')
    
    
    paciente_info = None
    
    if id_paciente:
        paciente_info = obtener_nombre_paciente(id_paciente)
        
        
        if not paciente_info:
            flash('Paciente no encontrado', 'error')
            return redirect(url_for('ConsultarP.pacientes'))
    else:
        flash('No se especificó un paciente', 'warning')
        return redirect(url_for('ConsultarP.pacientes'))
    
    return render_template('cita_exploracion_diagnostico.html', paciente_info=paciente_info)