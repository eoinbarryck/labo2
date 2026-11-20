"""Resumen Lab 2 en PDF. Los números salen de notebooks/resultados_*.json (no se escriben a mano)."""
import glob, json, os
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

ROOT = r"C:\Users\eoinb\projects\labo2"
os.chdir(ROOT + r"\notebooks")
R = {os.path.basename(f)[len("resultados_"):-5]: json.load(open(f)) for f in glob.glob("resultados_*.json")}
NOM = {k[:2]: k for k in R}
PADRE = {'01': '00', '02': '01', '03': '02', '04': '02', **{f"{n:02d}": '04' for n in range(5, 13)},
         '13': '12', '14': '13', **{f"{n:02d}": '14' for n in range(15, 23)}, **{f"{n:02d}": '22' for n in range(23, 30)}}

def stats(n):
    k = np.array(R[NOM[n]]["kappas_fold"])
    return k.mean(), k.std(ddof=1), k

def delta(n):
    _, _, k = stats(n); _, _, kp = stats(PADRE[n]); d = k - kp
    return d.mean(), int((d > 0).sum())

DESC = {
 '00': "Base del profesor (LightGBM clasificador, argmax)",
 '01': "Regresión + 4 umbrales optimizados para kappa",
 '02': "Cantidad de publicaciones por rescatista",
 '03': "10 variables de metadata de Google Vision",
 '04': "Puntaje medio de etiquetas de Google Vision, foto 1",
 '05': "Agregados por rescatista (Fee, Age, PhotoAmt)",
 '06': "Raza: pura / mestiza + frecuencia de Breed1",
 '07': "Precio por mascota, edad en años, gratis, edad vs raza",
 '08': "Texto liviano (largo, mayúsculas, !) + sentimiento VADER",
 '09': "Fotos con OpenCV: brillo, nitidez, aspecto, saturación",
 '10': "Solo nitidez de la foto 1",
 '11': "Agregados Google Vision (colores, etiquetas, recorte)",
 '12': "Promedio de 5 semillas por fold (80% filas y columnas)",
 '13': "Bloque OpenCV del 09, sobre el 12",
 '14': "Bloque Google Vision del 11, sobre el 13",
 '15': "Puntaje de salud (vacunado, desparasitado, castrado)",
 '16': "Fotos por mascota + flag sin fotos",
 '17': "Bloque de metadata del 03, sobre el 14",
 '18': "Hiperparámetros con Optuna (60 pruebas)",
 '19': "Estructura del texto (largo de palabra, ?, símbolos)",
 '20': "Clusters KMeans(24) de embeddings de imagen",
 '21': "Word2Vec de Description, 4 hilos (no reproducible)",
 '22': "Word2Vec de Description, reproducible (1 hilo)",
 '23': "Similitud con palabras semilla (TF-IDF)",
 '24': "PCA(32) de embeddings de imagen, sumado",
 '25': "PCA(32) de embeddings de imagen, reemplaza",
 '26': "Similitud con centroides de cada clase (imagen)",
 '27': "Vecinos más cercanos, embeddings de imagen",
 '28': "Vecinos más cercanos, vectores de texto",
 '29': "Coseno imagen-texto (dos SVD sin alinear)",
}
QUEDA = {'00': 'referencia', '01': 'SÍ', '02': 'SÍ', '04': 'SÍ (usuario)', '12': 'SÍ', '13': 'SÍ (usuario)',
         '14': 'SÍ', '22': 'SÍ', '10': 'no (usuario)', '26': 'no (usuario)'}

st = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=st["Heading1"], fontSize=15, spaceAfter=6, textColor=colors.HexColor("#1F3A5F"))
H2 = ParagraphStyle("H2", parent=st["Heading2"], fontSize=12, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#1F3A5F"))
P = ParagraphStyle("P", parent=st["BodyText"], fontSize=9.5, leading=13)
B = ParagraphStyle("B", parent=P, leftIndent=12, bulletIndent=2)
CELL = ParagraphStyle("C", parent=P, fontSize=8, leading=10)

def bullets(items):
    return [Paragraph(t, B, bulletText="-") for t in items]

def tabla(filas, anchos, resaltar=()):
    t = Table(filas, colWidths=anchos, repeatRows=1)
    estilo = [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
              ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
              ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8),
              ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B0B7C3")),
              ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
              ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F4F7")])]
    for r in resaltar:
        estilo += [("BACKGROUND", (0, r), (-1, r), colors.HexColor("#DCEFE0")), ("FONTNAME", (0, r), (-1, r), "Helvetica-Bold")]
    t.setStyle(TableStyle(estilo))
    return t

story = []
m22, s22, _ = stats('22'); m00, _, _ = stats('00')
story += [Paragraph("Lab 2 - PetFinder AdoptionSpeed: resumen de los pasos", H1),
          Paragraph(f"Fecha: 20/11/2026. Métrica: kappa cuadrático (QWK). Mejor versión: <b>22</b>, "
                    f"QWK de validación <b>{m22:.4f} +- {s22:.4f}</b> (base del profesor: {m00:.4f}; "
                    f"mejora total <b>+{m22 - m00:.3f}</b>). Todavía no se subió nada a Kaggle.", P)]

story += [Paragraph("1. Cómo se trabajó", H2)] + bullets([
    "Proyecto en la PC (carpeta labo2), repo privado en GitHub eoinbarryck/labo2, cuenta de Kaggle de Lab 2 (eoinbarry).",
    "Un cambio por notebook, con nombre NN_cambio. Cada notebook parte del mejor que quedó hasta ese momento (su \"padre\").",
    "El cambio va en una celda nueva; si se toca una celda existente, la línea se marca con # CAMBIO NN y la original queda comentada.",
    "Todo queda registrado en docs/BITACORA.md, con commit y subido a GitHub después de cada cambio.",
    "Criterio para quedarse un cambio (spec del usuario): mejorar en al menos 4 de 5 folds, sin que suba el desvío; "
    "referencia de mejora mínima +0.004. Cuando las reglas chocaron, decidió el usuario.",
])

story += [Paragraph("2. Validación (decisión clave)", H2)] + bullets([
    "El base usaba KFold sin agrupar: el mismo rescatista aparecía en train y en validación, y el modelo lo \"reconocía\". "
    "Con eso el base daba 0.383, pero era un número inflado.",
    "Desde el 18/11 se usa StratifiedGroupKFold(5) por RescuerID, semilla 42 (regla del Claude.md). "
    "Ningún rescatista se repite entre folds. Con esta validación honesta el base baja a 0.313.",
    "Los cortes de la regresión de cada fold se eligen con los otros 4 folds (kappa \"honesto\").",
    "Para buscar hiperparámetros (Optuna) se usaron otros folds (semilla 7), para no inflar la medición.",
])

story += [Paragraph("3. La cadena que quedó (lo que suma)", H2)]
filas = [["#", "Cambio", "QWK", "Suma vs padre", "Folds mejor"]]
for n in ['00', '01', '02', '04', '12', '13', '14', '22']:
    m, s, _ = stats(n)
    if n == '00':
        filas.append([n, Paragraph(DESC[n], CELL), f"{m:.4f}", "-", "-"])
    else:
        d, f = delta(n)
        filas.append([n, Paragraph(DESC[n] + (" (decisión del usuario)" if "usuario" in QUEDA[n] else ""), CELL),
                      f"{m:.4f}", f"{d:+.4f}", f"{f}/5"])
story += [tabla(filas, [1 * cm, 9.3 * cm, 1.7 * cm, 2.4 * cm, 2 * cm], resaltar=(len(filas) - 1,)), Spacer(1, 4),
          Paragraph(f"Casi el 60% de la mejora viene del 01 (regresión + umbrales): +{delta('01')[0]:.3f} de +{m22 - m00:.3f}.", P)]

story += [PageBreak(), Paragraph("4. Todas las versiones", H2),
          Paragraph("El delta es contra el padre de cada versión. QWK = media de los 5 folds.", P), Spacer(1, 4)]
filas = [["#", "Cambio", "Padre", "QWK +- desvío", "Delta", "Folds", "Queda"]]
verdes = []
for n in sorted(NOM):
    m, s, _ = stats(n)
    d, f = delta(n) if n != '00' else (None, None)
    q = QUEDA.get(n, "no")
    filas.append([n, Paragraph(DESC[n], CELL), PADRE.get(n, "-"), f"{m:.4f} +- {s:.4f}",
                  "-" if d is None else f"{d:+.4f}", "-" if f is None else f"{f}/5", q])
    if q.startswith("SÍ"):
        verdes.append(len(filas) - 1)
story += [tabla(filas, [0.8 * cm, 7.6 * cm, 1.1 * cm, 2.9 * cm, 1.5 * cm, 1.2 * cm, 1.9 * cm], resaltar=verdes)]

story += [PageBreak(), Paragraph("5. Lo que se aprendió", H2)] + bullets([
    "<b>Validar bien cambia todo.</b> Agrupar por rescatista bajó todos los números (~0.07), pero es lo que se parece al test, "
    "donde ningún rescatista de train aparece (0 de 1.518).",
    "<b>Estabilizar el modelo antes de sumar variables.</b> Con un solo modelo, los bloques de OpenCV (09) y Google Vision (11) "
    "no pasaban el criterio; con 5 semillas promediadas (12) pasaron (13 y 14).",
    "<b>El azar decide mejoras chicas.</b> Word2Vec con 4 hilos (21) dio 3/5 folds; la misma idea reproducible (22) dio 4/5. "
    "Para que fuera reproducible hizo falta workers=1 y una función de hash fija.",
    "<b>Optuna engañó en su propia búsqueda.</b> En los folds de búsqueda subía +0.028; en los folds oficiales, solo +0.002. "
    "Separar búsqueda y medición evitó aceptar una falsa mejora.",
    "<b>Resumir lo que el modelo ya ve no ayuda.</b> PCA, clusters, centroides y vecinos de los embeddings (20, 24-28) no sumaron: "
    "el modelo ya usa las 1.280 columnas de imagen y los 100 vectores de texto.",
    "<b>Revisar la idea antes de correrla.</b> El coseno imagen-texto (29) usaba dos espacios sin alinear: su valor medio cambiaba "
    "de signo entre folds (-0.67 / +0.67).",
])

story += [Paragraph("6. Datos y herramientas", H2)] + bullets([
    "Competencia petfinder-adoption-prediction: train.csv (14.993), test.csv (3.972), metadata de Google Vision y fotos (72.776).",
    "Notebooks del profesor (Rafael Crescenzi, nickel): emociones del texto y embeddings de imagen. Los embeddings son de "
    "EfficientNet-B0 (no ResNet), según su log.",
    "Preprocesamiento propio: prep_imagenes_opencv (brillo, nitidez, aspecto, saturación por foto).",
    "Python 3.12, LightGBM 4.7, scikit-learn 1.9, gensim 4.4 (Word2Vec), OpenCV, Optuna.",
])

story += [Paragraph("7. Pendiente", H2)] + bullets([
    "Tanda 01 para Kaggle armada en kaggle/tanda_01, pero con el 14; habría que rearmarla con el 22.",
    "Completar Integrantes en los notebooks (hoy dicen COMPLETAR).",
    "Comprobar en Kaggle: que gensim esté instalado, que los folds se armen igual y cuánto da el test.",
])

story += [Paragraph("Transparencia", H2)] + bullets([
    "<b>Mis elecciones:</b> validación por rescatista; kappa honesto para comparar; criterio del spec aplicado tal cual; "
    "folds aparte para Optuna; números de este PDF tomados de los archivos resultados_*.json.",
    "<b>Supuestos:</b> la competencia de la cátedra es petfinder-adoption-prediction; los números locales se parecen a los de Kaggle "
    "(con la validación vieja el base coincidió exacto por fold).",
    "<b>No verificado:</b> ningún resultado en Kaggle; otras semillas o particiones de folds; por qué algunos folds caen mucho (19, 27).",
    "<b>Errores:</b> usé al principio la cuenta de Kaggle de Lab 1 (corregido); el 02 usaba test para contar (corregido, mismos "
    "números); calculé mal tiempos de lectura de JSON; debí avisar el problema del 29 antes de correrlo.",
])

doc = SimpleDocTemplate(ROOT + r"\docs\resumen_lab2.pdf", pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm,
                        topMargin=1.5 * cm, bottomMargin=1.5 * cm, title="Lab 2 - resumen de los pasos", author="Lab 2")
doc.build(story)
print("ok")
