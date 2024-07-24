import os
from django.http import HttpResponse
from django.db import connection, connections
from .utils import api_firma, fecha_a_texto, numero_a_texto
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from reportlab.lib.units import inch
from FirmaSeduzac import settings
import textwrap
from reportlab.platypus import Table, TableStyle, Paragraph, Frame, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import qrcode
from reportlab.lib.units import mm

def pdf_totales(curp):
    with connections['mariadb'].cursor() as cursor:
        query = ("SELECT id_hist_estudio, curp, prim_apellido, seg_apellido, nombre, nombre_ct, clavecct, "
                 "bachillerato, fecha_cert_texto, folio_sep, sello_seduzac, autoridad_educativa, certificado_autoridad_educativa, fecha_firma FROM alumno_certificado WHERE curp = %s;")

        cursor.execute(query, [curp])
        registro = cursor.fetchall()

        if(not registro):
            return HttpResponse("No se encontraron registros para esta CURP.")

        registro = registro[0]

        id_hist_estudio = registro[0]
        curp = registro[1]
        prim_apellido = registro[2]
        seg_apellido = registro[3]
        nombre = registro[4]
        nombre_ct = registro[5]
        clave_ct = registro[6]
        bachillerato = registro[7]
        fecha_texto = registro[8]
        folio = registro[9]
        sello = registro[10]
        autoridad = registro[11]
        certificdo_autoridad = registro[12]
        fecha_firma = registro[13]

        query2 = ("SELECT a.id_hist_estudio, a.curp, b.cve_materia, m.nombre_materia, b.promedio "
                  "FROM alumno_certificado a JOIN boleta b ON a.id_hist_estudio = b.cve_alumno JOIN "
                  "materias m ON b.cve_materia = m.cve_materia WHERE a.curp = %s;")
        
        cursor.execute(query2, [curp])
        califs = cursor.fetchall()

        query_semestres = {
            1: "SELECT m.nombre_materia, b.calificacion FROM boleta b JOIN materias m ON b.cve_materia = m.cve_materia WHERE b.curp = %s AND b.semestre = 1;",
            2: "SELECT m.nombre_materia, b.calificacion FROM boleta b JOIN materias m ON b.cve_materia = m.cve_materia WHERE b.curp = %s AND b.semestre = 2;",
            3: "SELECT m.nombre_materia, b.calificacion FROM boleta b JOIN materias m ON b.cve_materia = m.cve_materia WHERE b.curp = %s AND b.semestre = 3;",
            4: "SELECT m.nombre_materia, b.calificacion FROM boleta b JOIN materias m ON b.cve_materia = m.cve_materia WHERE b.curp = %s AND b.semestre = 4;",
            5: "SELECT m.nombre_materia, b.calificacion FROM boleta b JOIN materias m ON b.cve_materia = m.cve_materia WHERE b.curp = %s AND b.semestre = 5;",
            6: "SELECT m.nombre_materia, b.calificacion FROM boleta b JOIN materias m ON b.cve_materia = m.cve_materia WHERE b.curp = %s AND b.semestre = 6;"
        }

        # Diccionario para almacenar los resultados por semestre
        materias_por_semestre = {}

        # Ejecutar las consultas para cada ssmestre
        for semestre, query in query_semestres.items():
            cursor.execute(query, [curp])
            materias_por_semestre[semestre] = cursor.fetchall()
            print(f"Semestre {semestre}: {materias_por_semestre[semestre]}")

        total_materias = sum(len(materias_por_semestre[semestre]) for semestre in materias_por_semestre)
        print(f"Numero total de materias: {total_materias}")
        num_text = numero_a_texto(total_materias)
        print(f'Numero de materias en texto: {num_text}')

        # Query para periodos
        query_periodo_s1 = "SELECT periodo_s1 FROM boleta WHERE curp = %s;"
        query_periodo_s2 = "SELECT periodo_s2 FROM boleta WHERE curp = %s;"
        query_periodo_s3 = "SELECT periodo_s3 FROM boleta WHERE curp = %s;"
        query_periodo_s4 = "SELECT periodo_s4 FROM boleta WHERE curp = %s;"
        query_periodo_s5 = "SELECT periodo_s5 FROM boleta WHERE curp = %s;"
        query_periodo_s6 = "SELECT periodo_s6 FROM boleta WHERE curp = %s;"

        cursor.execute(query_periodo_s1,[curp])
        periodo_s1 = cursor.fetchall()

        cursor.execute(query_periodo_s2,[curp])
        periodo_s2 = cursor.fetchall()

        cursor.execute(query_periodo_s3,[curp])
        periodo_s3 = cursor.fetchall()

        cursor.execute(query_periodo_s4,[curp])
        periodo_s4 = cursor.fetchall()

        cursor.execute(query_periodo_s5,[curp])
        periodo_s5 = cursor.fetchall()

        cursor.execute(query_periodo_s6,[curp])
        periodo_s6 = cursor.fetchall()
        print(f'Periodos:{periodo_s1},{periodo_s2},{periodo_s3},{periodo_s4},{periodo_s5},{periodo_s6}')
    
        if((not periodo_s1) and (not periodo_s2) and (not periodo_s3) and (not periodo_s4) and (not periodo_s5) and (not periodo_s6)):
            print(f'Periodos:{periodo_s1},{periodo_s2},{periodo_s3},{periodo_s4},{periodo_s5},{periodo_s6}')
            return HttpResponse("No se encontraron periodos")
        
        periodo_s1 = periodo_s1[0]
        periodo_s2 = periodo_s2[0]
        periodo_s3 = periodo_s3[0]
        periodo_s4 = periodo_s4[0]
        periodo_s5 = periodo_s5[0]
        periodo_s6 = periodo_s6[0]

        ps1 = periodo_s1[0]
        ps2 = periodo_s2[0]
        ps3 = periodo_s3[0]
        ps4 = periodo_s4[0]
        ps5 = periodo_s5[0]
        ps6 = periodo_s6[0]

        nombres_materias = []
        promedios = []

        for registro in califs:
            nombres_materias.append(registro[3])
            promedios.append(registro[4])

        try:
            promedio_total = sum(promedios) / len(promedios)
        except:
            return HttpResponse("El alumno no cuenta con materias registradas")

    # Código para generar el PDF
    custom_page_size = (9 * inch, letter[1])
    filename = f"{curp}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=custom_page_size)

    # Ruta de la imagen de fondo
    bg_relative_path = os.path.join('sello.jpg')
    background_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', bg_relative_path)
    
    try:
        p.drawImage(background_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1])
    except IOError:
        print(f"Error: No se pudo cargar la imagen de fondo en {background_image_path}")

    titulo = f"Certificado Total - {curp}"
    p.setTitle(titulo)
    p.setFont("Helvetica", 14)

    # Cargarlas imágenes de los logos
    logo1_relative_path = os.path.join('img', 'logo1.jpeg')
    logo1_path = os.path.join(settings.STATICFILES_DIRS[0], logo1_relative_path)
    logo2_relative_path = os.path.join('img', 'logo2.jpeg')
    logo2_path = os.path.join(settings.STATICFILES_DIRS[0], logo2_relative_path)
    logo3_relative_path = os.path.join('img', 'logo3.jpeg')
    logo3_path = os.path.join(settings.STATICFILES_DIRS[0], logo3_relative_path)

    x_logo1 = inch / 2
    y_logo1 = letter[1] - inch / 2 - 30
    x_logo3 = inch / 2 + 160
    y_logo3 = letter[1] - inch / 2 - 35
    x_logo2 = inch / 2 + 390
    y_logo2 = letter[1] - inch / 2 - 30

    if os.path.exists(logo1_path):
        p.drawImage(logo1_path, x_logo1 - 10, y_logo1, width=160, height=40)
    else:
        print(f"Error: La imagen en {logo1_path} no existe.")

    if os.path.exists(logo3_path):
        p.drawImage(logo3_path, x_logo3 + 35, y_logo3, width=220, height=50)
    else:
        print(f"Error: La imagen en {logo3_path} no existe.")

    if os.path.exists(logo2_path):
        p.drawImage(logo2_path, x_logo2 + 90, y_logo2 + 2, width=125, height=40)
    else:
        print(f"Error: La imagen en {logo2_path} no existe.")

    # Coordenadas iniciales para el texto debajo de los logos
    x_texto = inch / 2 - 10
    y_texto = letter[1] - inch / 2 - 30

    style_paragraphT1 = ParagraphStyle(
        name='Justified',
        fontSize=9,
        leading=12,
        alignment=4
    )

    text_width =610  # Ancho del cuadro de texto
    text_height = 600  # Altura del cuadro de texto

    # Contenido debajo del encabezado
    texto = (
        f'La Secretaría de Educación del Estado de Zacatecas, a través de la Escuela Preparatoria {nombre_ct}, con Clave de Centro de Trabajo {clave_ct}, '
        f'<b>CERTIFICA</b> que <b>{nombre} {prim_apellido} {seg_apellido}</b> con CURP {curp}, cursó los estudios completos de {bachillerato}, en la modalidad Escolarizada, '
        f'según constancias que obran en el Área de Control Escolar'
    )
    
    paragraph_texto = Paragraph(texto, style_paragraphT1)
    # Dividir el texto en líneas automáticas
    text_lines = textwrap.wrap(texto, width=100)
    line_height = 14
    p.setFont("Helvetica", 10)

    frame = Frame(x_texto, y_texto - 610, text_width, text_height, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
    frame.addFromList([paragraph_texto], p)

    y_texto -= line_height * 2.5
    max_line_width = 550
    bold_words = ["CERTIFICA"]

    p.setFont("Helvetica", 9)
    texto_p2 = (f"La presente certificación ampara {num_text} asignaturas que integran el Plan de Estudios respectivo.")
    p.drawString(x_texto, y_texto - 30, texto_p2)

    p.setFont("Helvetica", 9)
    texto_p3 = (f"El presente se expide en GUADALUPE, ZACATECAS, a los {fecha_texto}.")
    p.drawString(x_texto, y_texto-42, texto_p3)

    #------------------------------------------ la tabla
    style_semester_title = ParagraphStyle(
    name='SemesterTitle',
    fontSize=8,
    leading=12,
    )

    data = [
    ['ASIGNATURAS', 'CALIF.FINAL ', 'ASIGNATURAS', 'CALIF.FINAL'],
    ['', '', '', ''],
    [Paragraph(f"PRIMER SEMESTRE({ps1})", style_semester_title), '', Paragraph(f"SEGUNDO SEMESTRE({ps2})", style_semester_title), '']
    ]

    # Agregar materias y promedios para el primer y segundo semestre
    max_length = max(len(materias_por_semestre[1]), len(materias_por_semestre[2]))

    if(max_length == 0):
        for _ in range(11):
            data.append(['', '', '', ''])
    else:
        for i in range(max_length):
            materia1 = materias_por_semestre[1][i] if i < len(materias_por_semestre[1]) else ('', '')
            materia2 = materias_por_semestre[2][i] if i < len(materias_por_semestre[2]) else ('', '')
            data.append([materia1[0], materia1[1], materia2[0], materia2[1]])

        for _ in range(11 - max_length):
            data.append(['', '', '', ''])

    # Otros semestres y agregar el contenido
    entra_for = False
    semesters = [
        [Paragraph(f"TERCER SEMESTRE({ps4})", style_semester_title), 3, Paragraph(f"CUARTO SEMESTRE({ps3})", style_semester_title), 4],
        [Paragraph(f"QUINTO SEMESTRE({ps5})", style_semester_title), 5, Paragraph(f"SEXTO SEMESTRE({ps6})", style_semester_title), 6],
    ]

    for title1, sem1, title2, sem2 in semesters:
        data.append([title1, '', title2, ''])  # Agregar el encabezado del semestre
        max_length = max(len(materias_por_semestre.get(sem1, [])), len(materias_por_semestre.get(sem2, [])))

        if(max_length == 0):
            for _ in range(11):
                data.append(['', '', '', ''])
        else:
            for i in range(max_length):
                materia1 = materias_por_semestre[sem1][i] if i < len(materias_por_semestre.get(sem1, [])) else ('', '')
                materia2 = materias_por_semestre[sem2][i] if i < len(materias_por_semestre.get(sem2, [])) else ('', '')
                data.append([materia1[0], materia1[1], materia2[0], materia2[1]])

            for _ in range(11 - max_length):
                entra_for = True
                data.append(['', '', '', ''])

    # print(f"ENTRA AL FOR: {entra_for}")

    # Relleno hasta llegar a 35 filas
    while len(data) < 35:
        data.append([" ", " "])
            
    # Crear un estilopara los títulos
    style_wrap = ParagraphStyle(
        name='Wrapped',
        fontSize=9,
        leading=12,
        alignment=1,
        wordWrap='CJK',  #Habilitar el ajuste de texto
    )

    #Convertir los títulos de la tabla a prrafos con ajuste de texto
    data[0] = [Paragraph(cell, style_wrap) for cell in data[0]]

    # Definir anchos fijos para las columnas
    col_widths = [267, 45, 267, 45]

    row_heights = [20] + [10] * (len(data) - 1)

    # Crear una tabla con dimensiones predefinidas
    table = Table(data, colWidths=col_widths, rowHeights=row_heights)

    # Estilo de la tabla
    style = TableStyle([
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'), 
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 2), 
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),  
        ('LINEAFTER', (0, 0), (0, -1), 0.5, colors.black),   
        ('LINEAFTER', (1, 0), (1, -1), 0.5, colors.black),   
        ('LINEAFTER', (2, 0), (2, -1), 0.5, colors.black),   
        ('LINEAFTER', (3, 0), (3, -1), 0.5, colors.black),   
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    table.setStyle(style)

    table.wrapOn(p, 0, 0)  # Ajustar el espacio disponible
    table.drawOn(p, 15, y_texto - 445)  # Ajustar el valor X para mover la tabla a la izquierda 365

    # PROMEDIO
    p.setFont("Helvetica-Bold", 9.5)
    texto_prom = (f'PROMEDIO GENERAL')
    p.drawString(x_texto + 5, y_texto - 460, texto_prom)
    texto_prom = (f'DE APROVECHAMIENTO')
    p.drawString(x_texto, y_texto - 472, texto_prom)
    # Dibuo el rectangulo para la celda
    p.setLineWidth(0.1)
    ancho_rect = 79  # Ancho del rectangulo
    alto_rect = 21  # Alto del rectsngulo
    p.setFont("Helvetica", 9)
    p.rect(x_texto + 18, y_texto - 498, ancho_rect, alto_rect)
    p.drawString(x_texto + 52, y_texto - 490,f'{promedio_total}')

    # Codigo QR
    qr_text = f"{nombre} {prim_apellido} {seg_apellido} Secretaría de Educación del Estado de Zacatecas Certificado de Terminación de Estudios https://www.seduzac.gob.mx/consultaCalificacion.html"  # Texto para generar el QR (puedes cambiarlo por tu propio contenido)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(qr_text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_path = os.path.join(settings.MEDIA_ROOT, 'qr_code.png')
    qr_img.save(qr_img_path)

    p.drawImage(qr_img_path, inch / 2 - 15, y_texto - 625, width=120, height=120)

    os.remove(qr_img_path)  # Eliminar el archivo de imagen temporal del QR

    # FOLIO
    texto_prom = (f'FOLIO {folio}')
    p.drawString(x_texto + 20, y_texto - 650, texto_prom)

    # TEXTO DESPUES DEL FOLIO
    x_qr = inch / 2
    y_qr = 200
    qr_size = 100  # Tamaño del QR

    text_x = x_qr + qr_size + 10
    text_y = y_qr + qr_size - 10
    text_width = 482
    text_height = qr_size*2.5

    texto_autoridad = f"Autoridad educativa: {autoridad}"
    texto_certificado = f"No. certificado autoridad educativa: {certificdo_autoridad}"
    texto_sello_texto = "Sello Digital autoridad educativa:"
    texto_sello = f"{sello}"
    texto_fecha = f"Fecha y hora de timbrado: {fecha_texto} {fecha_firma}"
    texto_fijo1 = f"Con fundamento en lo dispuesto por el artículo 141 de la Ley General de Educación, los certificados de estudios expedidos por instituciones del Sistema Educativo Nacional, tienen validez en la República Mexicana sin necesidad de trámites adicionales de autenticación o legalización, favoreciendo el tránsito del educando por el Sistema Educativo Nacional."
    texto_fijo2 = f"La presente certificación es expedida previa consulta y validación de antecedentes escolares con el Departamento de Control Escolar de la Secretaría de Educación del Estado de Zacatecas y, ha sido firmado mediante el uso de la firma electrónica avanzada, amparada por un certificado vigente a la fecha de su elaboración; y, es válido de conformidad con lo dispuesto en el Artículo 5 Fracción I, 7, 9 Fracción I, 12, 13 y 22 de la Ley de Firma Electrónica del Estado de Zacatecas y demás aplicables."
    texto_fijo3 = f"La versión electrónica del presente documento, su integridad y autoría se podrá comprobar a través de la página electrónica de la Secretaría de Educación del Estado de Zacatecas por medio de la siguiente liga: https://www.seduzac.gob.mx/consultaCalificacion.html De igual manera, podrá verificar el documento electrónico por medio del código QR."

    style_paragraph = ParagraphStyle(
        name='Justified',
        fontSize=7,
        leading=10,
        alignment=4
    )

    paragraph = Paragraph(texto_autoridad, style_paragraph)
    paragraph2 = Paragraph(texto_certificado, style_paragraph)
    paragraph3 = Paragraph(texto_sello_texto, style_paragraph)
    paragraph4 = Paragraph(texto_sello, style_paragraph)
    paragraph5 = Paragraph(texto_fecha, style_paragraph)
    paragraph6 = Paragraph(texto_fijo1, style_paragraph)
    paragraph7 = Paragraph(texto_fijo2, style_paragraph)
    paragraph8 = Paragraph(texto_fijo3, style_paragraph)

    espacio_p = Spacer(1, 3)
    espacio_pd = Spacer(1, 6)

    frame = Frame(text_x + 10, y_texto - 699, text_width, text_height, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
    frame.addFromList([paragraph,paragraph2,paragraph3,paragraph4,paragraph5,paragraph6,espacio_p,paragraph7,espacio_pd,paragraph8], p)

    # Finalizar la página y guardar el PDF
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)

    return response