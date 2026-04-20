from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm

ACCENT = HexColor("#1a56db")
ACCENT_LIGHT = HexColor("#e8f0fe")
DARK = HexColor("#1a1a2e")
GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#f5f5f5")
BORDER = HexColor("#d0d0d0")

styles = getSampleStyleSheet()

def s(name, **kw):
    base = styles[name] if name in styles else styles["Normal"]
    return ParagraphStyle(name + str(id(kw)), parent=base, **kw)

name_style = s("Normal", fontSize=22, textColor=DARK, fontName="Helvetica-Bold",
               leading=26, spaceAfter=2)
title_style = s("Normal", fontSize=11, textColor=ACCENT, fontName="Helvetica-Bold",
                leading=14, spaceAfter=4)
contact_style = s("Normal", fontSize=8.5, textColor=GRAY, fontName="Helvetica",
                  leading=12)
section_header = s("Normal", fontSize=11, textColor=white, fontName="Helvetica-Bold",
                   leading=14, spaceAfter=0, spaceBefore=0,
                   leftIndent=6)
job_title = s("Normal", fontSize=9.5, textColor=DARK, fontName="Helvetica-Bold",
              leading=13, spaceAfter=1)
job_company = s("Normal", fontSize=9, textColor=ACCENT, fontName="Helvetica-Bold",
                leading=12, spaceAfter=1)
job_date = s("Normal", fontSize=8.5, textColor=GRAY, fontName="Helvetica-Oblique",
             leading=11, spaceAfter=2)
body_style = s("Normal", fontSize=8.5, textColor=DARK, fontName="Helvetica",
               leading=12, spaceAfter=1, leftIndent=8)
bullet_style = s("Normal", fontSize=8.5, textColor=DARK, fontName="Helvetica",
                 leading=12, leftIndent=14, firstLineIndent=-6, spaceAfter=1)
skill_label = s("Normal", fontSize=8.5, textColor=DARK, fontName="Helvetica-Bold",
                leading=12, spaceAfter=0)
skill_val = s("Normal", fontSize=8.5, textColor=GRAY, fontName="Helvetica",
              leading=12, spaceAfter=2)
profile_style = s("Normal", fontSize=9, textColor=DARK, fontName="Helvetica",
                  leading=13, spaceAfter=4, alignment=TA_JUSTIFY)


def section_block(title):
    tbl = Table([[Paragraph(title.upper(), section_header)]],
                colWidths=[PAGE_W - 2 * MARGIN])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl


def tag(text):
    return (f'<font color="#1a56db" backColor="#e8f0fe">&nbsp;{text}&nbsp;</font>')


def build_skills_table(skills):
    rows = []
    for label, items in skills:
        tags = "  ".join(tag(i) for i in items)
        rows.append([
            Paragraph(label, skill_label),
            Paragraph(tags, skill_val),
        ])
    t = Table(rows, colWidths=[3.8 * cm, PAGE_W - 2 * MARGIN - 3.8 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def job_block(company, role, period, bullets):
    elems = [
        Paragraph(company, job_company),
        Paragraph(role, job_title),
        Paragraph(period, job_date),
    ]
    for b in bullets:
        elems.append(Paragraph(f"• {b}", bullet_style))
    elems.append(Spacer(1, 4))
    return KeepTogether(elems)


def project_block(name, role_period, bullets):
    elems = [
        Paragraph(name, job_company),
        Paragraph(role_period, job_date),
    ]
    for b in bullets:
        elems.append(Paragraph(f"• {b}", bullet_style))
    elems.append(Spacer(1, 4))
    return KeepTogether(elems)


story = []

# ── Header ──────────────────────────────────────────────────────────────────
story.append(Paragraph("Francisco Jesús Castro Zuleta", name_style))
story.append(Paragraph("Desarrollador XR/AR/VR · Inteligencia Artificial · Full-Stack", title_style))

contact_line = (
    "francisco.castro.init@gmail.com  |  +56 9 3523 2158  |  Chile  |  "
    "<link href='https://linkedin.com/in/francisco-castro-zuleta/' color='#1a56db'>LinkedIn</link>  |  "
    "<link href='https://franciscocastro.cl' color='#1a56db'>franciscocastro.cl</link>  |  "
    "<link href='https://github.com/franciscocastro54' color='#1a56db'>GitHub</link>"
)
story.append(Paragraph(contact_line, contact_style))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8, spaceBefore=6))

# ── Perfil ───────────────────────────────────────────────────────────────────
story.append(section_block("Perfil Profesional"))
story.append(Spacer(1, 5))
story.append(Paragraph(
    "Desarrollador de Software con más de 4 años de experiencia entregando soluciones de alto impacto en "
    "Realidad Extendida (XR) e Inteligencia Artificial, en entornos militares, universitarios y corporativos. "
    "Especializado en Unity para Meta Quest 2/3 y HoloLens 2, con historial comprobado de llevar proyectos "
    "desde prototipo hasta producción.", profile_style))
story.append(Paragraph(
    "Combino desarrollo Full-Stack (C#, Python, React, Django) con integración de IA on-device y visión "
    "computacional, liderazgo técnico de equipos de desarrollo, y docencia universitaria. Capaz de trabajar "
    "de forma autónoma en proyectos complejos y de escalar soluciones para múltiples usuarios y dispositivos.",
    profile_style))

# ── Experiencia ──────────────────────────────────────────────────────────────
story.append(section_block("Experiencia Profesional"))
story.append(Spacer(1, 5))

story.append(job_block(
    "Academia Politécnica Militar",
    "Desarrollador XR / Líder Técnico",
    "03/2023 – 12/2025",
    [
        "Desarrollé y entregué más de 5 aplicaciones Unity en producción para Meta Quest 2, Meta Quest 3 y HoloLens 2, utilizadas en formación militar activa.",
        "Diseñé experiencias educativas inmersivas: ensamblaje virtual de artefactos, entornos multijugador, reconstrucción georreferenciada de terrenos e integración Meta Quest 3 + Arduino.",
        "Liderazgo técnico del equipo XR: coordinación de tareas, revisión de avances y mentoría a desarrolladores junior.",
        "Instructor en desarrollo de aplicaciones para Meta Quest 3.",
    ]
))

story.append(job_block(
    "Universidad del Desarrollo (UDD)",
    "Desarrollador XR / Instructor",
    "03/2024 – 12/2025",
    [
        "Desarrollé experiencias de realidad virtual en Unity para Meta Quest 2 orientadas a simulaciones educativas en medicina.",
        "Implementé entornos multijugador con Meta Quest XR SDK, Photon Voice y Meta Quest Avatars.",
        "Instructor de Unity para estudiantes de Ingeniería.",
    ]
))

story.append(job_block(
    "Plataforma Group Spa",
    "Desarrollador Full-Stack",
    "01/2022 – 12/2022",
    [
        "Diseño y desarrollo de librerías en C# para plataforma interna.",
        "Desarrollo de APIs REST y migración de sistema de .NET Core 5 a .NET Standard 2.0.",
    ]
))

story.append(job_block(
    "Inacap Renca",
    "Analista Programador",
    "03/2020 – 12/2022",
    [
        "Aplicación web para gestión de datos en procesos de flotación de minerales (minería).",
        "Sistema de gestión para sala de profesores con integración de escáner de códigos de barras.",
    ]
))

story.append(job_block(
    "Profesor Particular de Programación",
    "Freelance",
    "03/2020 – Presente",
    [
        "Tutorías en educación media y superior: fundamentos de programación e ingeniería.",
        "Clases de desarrollo de videojuegos con Unity.",
    ]
))

# ── Proyectos ─────────────────────────────────────────────────────────────────
story.append(section_block("Proyectos Independientes Destacados"))
story.append(Spacer(1, 5))

story.append(project_block(
    "Proyecto Educativo AR Potenciado con IA",
    "Desarrollo Independiente · 04/2025 – Presente",
    [
        "Detección de imágenes en tiempo real con IA on-device en Meta Quest 3.",
        "Análisis dinámico mediante modelos de IA preconfigurados ejecutados directamente en el visor.",
    ]
))

story.append(project_block(
    "franciscocastro.cl / propiedadesyparcelasenpirque.cl",
    "Desarrollador Front-End · 2025 – Presente",
    [
        "franciscocastro.cl: Vite + React + TypeScript, priorizado en performance y mantenibilidad.",
        "propiedadesyparcelasenpirque.cl: arquitectura escalable de componentes y optimización de carga.",
    ]
))

story.append(project_block(
    "Sistema de Análisis de PDFs y CSVs mediante IA",
    "Proyecto Independiente · 2026",
    [
        "Aplicación web con chatbot para análisis de grandes volúmenes de documentos con visualización dinámica.",
    ]
))

story.append(project_block(
    "Sistema de Tracking de Movimientos por Webcam + IA",
    "Proyecto Independiente · 2026",
    [
        "Aplicación web de visión computacional para control por gestos mediante la webcam.",
    ]
))

story.append(project_block(
    "Admivet — Aplicación Veterinaria de Escritorio",
    "Desarrollador Full-Stack · 2026",
    [
        "Gestión de clínicas veterinarias: pacientes, citas, historial médico y facturación.",
    ]
))

story.append(project_block(
    "Conergie Demo API",
    "Desarrollador Full-Stack (Django REST Framework) · 2026",
    [
        "API REST para flujo de licitación: Tender, Suppliers, Offers y ranking por costo estimado.",
        "Autenticación JWT con roles CLIENT/SUPPLIER y control de acceso granular.",
        "Documentación OpenAPI/Swagger y comando de seed para pruebas.",
    ]
))

# ── Habilidades ───────────────────────────────────────────────────────────────
story.append(section_block("Habilidades Técnicas"))
story.append(Spacer(1, 5))

skills_data = [
    ("Lenguajes", ["C#", "Python", "JavaScript", "TypeScript"]),
    ("XR / Spatial", ["Unity", "Meta Quest 2/3", "HoloLens 2", "Meta XR SDK", "Hand Tracking", "Passthrough", "Mixed Reality"]),
    ("IA & Visión", ["IA on-device (Quest 3)", "Computer Vision", "Gaussian Splatting", "Text-to-Speech"]),
    ("Multiplayer", ["Netcode for GameObjects", "Photon Voice", "Meta Quest Avatars"]),
    ("Backend", ["Django", "Django REST Framework", "JWT (SimpleJWT)", "OpenAPI/Swagger", ".NET", "REST APIs"]),
    ("Frontend", ["React", "Vite", "TypeScript", "HTML", "CSS"]),
    ("Bases de datos", ["PostgreSQL", "SQLite"]),
    ("Hardware / IoT", ["Arduino", "ESP32", "Bluetooth", "WiFi"]),
    ("DevOps / Tools", ["Git", "GitHub", "3D Terrain Reconstruction", "Optimización XR móvil"]),
    ("Docencia", ["Instrucción universitaria", "Liderazgo técnico", "Mentoría junior", "Gestión de proyectos"]),
]

story.append(build_skills_table(skills_data))
story.append(Spacer(1, 6))

# ── Educación ─────────────────────────────────────────────────────────────────
story.append(section_block("Educación y Certificaciones"))
story.append(Spacer(1, 5))

story.append(Paragraph("<b>Analista Programador</b> · Inacap Renca · 2022", body_style))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "<b>7 cursos de uso de IA Generativa para sector público</b> · Hazlo con IA (CENIA Chile / SOFOFA / SENCE) · "
    "14 horas · marzo 2026", body_style))
story.append(Spacer(1, 6))

# ── Idiomas ───────────────────────────────────────────────────────────────────
story.append(section_block("Idiomas"))
story.append(Spacer(1, 5))
story.append(Paragraph("<b>Español:</b> Nativo", body_style))
story.append(Paragraph("<b>Inglés:</b> Avanzado — lectura técnica, documentación, comunicación escrita", body_style))

# ── Build ─────────────────────────────────────────────────────────────────────
out = "D:/PortfolioWeb/cvFranciscoCastroZuleta/CV_Francisco_Castro.pdf"
doc = SimpleDocTemplate(
    out, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
    title="CV – Francisco Jesús Castro Zuleta",
    author="Francisco Castro",
)
doc.build(story)
print(f"PDF generado: {out}")
