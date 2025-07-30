from flask import Blueprint, make_response, flash, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
from Cuerito import execute_query

ImprimirReceta_bp = Blueprint('ImprimirReceta', __name__)

@ImprimirReceta_bp.route('/descargar_receta/<id_paciente>/<nombre_paciente>')
def descargar_receta(id_paciente, nombre_paciente):
    try:
        # Obtener datos del paciente y su última receta
        query_paciente = "SELECT nombre FROM expediente_pacientes WHERE id_paciente = %s"
        paciente = execute_query(query_paciente, (id_paciente,), fetch="one")
        
        query_diagnostico = """
            SELECT sintomas, diagnostico, receta, indicaciones 
            FROM diagnosticos 
            WHERE id_paciente = %s 
            ORDER BY id_diagnostico DESC 
            LIMIT 1
        """
        diagnostico = execute_query(query_diagnostico, (id_paciente,), fetch="one")
        
        if not paciente:
            flash('No se encontró información del paciente', 'error')
            return redirect(url_for('ConsultarP.pacientes'))
            
        if not diagnostico:
            flash('No se ha generado una receta para este paciente', 'error')
            return redirect(url_for('ConsultarP.pacientes'))
        
        # Crear PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []
        
        # Contenido simple
        content.append(Paragraph("RECETA MÉDICA", styles['Title']))
        content.append(Spacer(1, 20))
        
        content.append(Paragraph(f"<b>Paciente:</b> {paciente[0]}", styles['Normal']))
        
        content.append(Paragraph(f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
        content.append(Spacer(1, 20))
        
        content.append(Paragraph(f"<b>Síntomas:</b> {diagnostico[0]}", styles['Normal']))
        content.append(Spacer(1, 10))
        
        content.append(Paragraph(f"<b>Diagnóstico:</b> {diagnostico[1]}", styles['Normal']))
        content.append(Spacer(1, 10))
        
        content.append(Paragraph(f"<b>Receta:</b> {diagnostico[2]}", styles['Normal']))
        content.append(Spacer(1, 10))
        
        content.append(Paragraph(f"<b>Indicaciones:</b> {diagnostico[3]}", styles['Normal']))
        content.append(Spacer(1, 30))
        
        content.append(Paragraph("_________________________", styles['Normal']))
        content.append(Paragraph("Firma del Médico", styles['Normal']))
        
        # Generar PDF
        doc.build(content)
        buffer.seek(0)
        
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=receta_{nombre_paciente}.pdf'
        
        return response
        
    except Exception as e:
        return f"Error: {str(e)}", 500