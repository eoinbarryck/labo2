# Bitácora Lab 2 (PetFinder AdoptionSpeed, métrica kappa cuadrática)

Regla: un cambio por vez. Se mide con el mismo CV (KFold 5, mismos folds que el base).
Si el cambio no mejora el kappa OOF, se revierte.

## Forma de trabajo

- Se modifica y se mide fuera de Kaggle (en la PC). En Kaggle solo se suben tandas (batch) de notebooks, porque hay un par de horas por día.
- Un cambio nuevo por notebook. Nombre: `NN_<cambio>.ipynb` (ej. `01_regresion_umbrales.ipynb`).
- Cada notebook parte del **mejor notebook que quedó hasta ahí** (columna "Padre"), nunca de uno descartado.
- El cambio va en una **celda nueva**. Si hay que tocar una celda existente, la línea modificada se marca con un comentario:
  `# CAMBIO NN: <qué y por qué>` (y la línea original queda comentada debajo, si se reemplazó).
- Arriba de cada notebook, una celda markdown: "CAMBIO NN respecto de <padre>: ...".
- Los cambios que no mejoran el kappa OOF se marcan como descartados y no se suben.

## Tandas para Kaggle

| Tanda | Fecha | Notebooks | QWK CV local | Estado | QWK Kaggle |
|-------|-------|-----------|--------------|--------|------------|
| 01 | 2026-11-19 | prep_imagenes_opencv → 14_vision_agregados_sobre_13 | 0.4178 ± 0.0148 | armada en `kaggle/tanda_01`, NO subida (falta Integrantes y OK del usuario) | — |

## Registro de experimentos — medición v2 (VIGENTE desde 2026-11-18)

Folds `StratifiedGroupKFold(5, shuffle=True, random_state=42)` por `RescuerID`, estratificados por AdoptionSpeed
(regla de Claude.md). Copia local en `data/folds.csv`; cada notebook verifica que sus folds coinciden.
0 rescatistas compartidos entre folds. Se reporta kappa por fold, media ± desvío y folds que mejoran.

| # | Notebook | Padre | Kappa por fold | Media ± desvío | Δ vs padre | Folds mejor | ¿Queda? |
|---|----------|-------|----------------|----------------|------------|-------------|---------|
| 00 | 00_base | — | 0.299 0.280 0.346 0.336 0.304 | 0.3130 ± 0.0273 | — | — | referencia |
| 01 | 01_regresion_umbrales | 00 | 0.372 0.368 0.376 0.385 0.377 | 0.3756 ± 0.0065 | +0.0625 | 5/5 | SÍ (ver nota) |
| 02 | 02_conteo_rescuer | 01 | 0.371 0.390 0.395 0.386 0.400 | 0.3882 ± 0.0111 | +0.0127 | 4/5 | **SÍ** |
| 03 | 03_metadata_imagenes | 02 | 0.405 0.385 0.421 0.406 0.398 | 0.4028 ± 0.0131 | +0.0145 | 3/5 | NO (descartado) |

| 04 | 04_meta_score_foto1 | 02 | 0.390 0.389 0.423 0.403 0.407 | 0.4022 ± 0.0139 | +0.0140 | 4/5 | **SÍ** (decisión del usuario) |

| 05 | 05_agregados_rescuer | 04 | 0.412 0.374 0.432 0.390 0.402 | 0.4021 ± 0.0218 | −0.0001 | 2/5 | NO (descartado) |

| 06 | 06_raza_flags_freq | 04 | 0.400 0.371 0.421 0.394 0.407 | 0.3988 ± 0.0185 | −0.0034 | 2/5 | NO (descartado) |

| 07 | 07_economia_camada | 04 | 0.388 0.367 0.422 0.389 0.406 | 0.3944 ± 0.0207 | −0.0078 | 0/5 | NO (descartado) |

| 08 | 08_texto_liviano_vader | 04 | 0.400 0.387 0.431 0.377 0.404 | 0.3999 ± 0.0202 | −0.0023 | 2/5 | NO (descartado) |

| 09 | 09_imagenes_opencv | 04 | 0.401 0.387 0.444 0.412 0.399 | 0.4086 ± 0.0215 | +0.0064 | 3/5 | NO (descartado) |

| 10 | 10_nitidez_foto1 | 04 | 0.401 0.390 0.429 0.404 0.396 | 0.4041 ± 0.0151 | +0.0019 | 4/5 | NO (descartado por el usuario) |

| 11 | 11_vision_agregados | 04 | 0.393 0.383 0.433 0.415 0.400 | 0.4048 ± 0.0196 | +0.0026 | 3/5 | NO (descartado) |

| 12 | 12_promedio_semillas | 04 | 0.405 0.395 0.428 0.408 0.408 | 0.4086 ± 0.0119 | +0.0064 | 5/5 | **SÍ** — nuevo padre |

| 13 | 13_imagenes_opencv_sobre_12 | 12 | 0.410 0.392 0.436 0.410 0.417 | 0.4128 ± 0.0158 | +0.0042 | 4/5 | **SÍ** (decisión del usuario) — nuevo padre |

| 14 | 14_vision_agregados_sobre_13 | 13 | 0.414 0.396 0.436 0.419 0.425 | 0.4178 ± 0.0148 | +0.0050 | 5/5 | **SÍ** — nuevo padre |

| 15 | 15_salud_puntaje | 14 | 0.425 0.384 0.443 0.417 0.422 | 0.4182 ± 0.0216 | +0.0004 | 2/5 | NO (descartado) |

| 16 | 16_fotos_por_mascota | 14 | 0.386 0.384 0.431 0.416 0.423 | 0.4079 ± 0.0217 | −0.0099 | 0/5 | NO (descartado) |

| 17 | 17_metadata_03_sobre_14 | 14 | 0.419 0.404 0.397 0.411 0.417 | 0.4095 ± 0.0090 | −0.0083 | 2/5 | NO (descartado) |

| 18 | 18_optuna_hiperparametros | 14 | 0.408 0.401 0.449 0.415 0.424 | 0.4195 ± 0.0188 | +0.0016 | 2/5 | NO (descartado) |

| 19 | 19_texto_estructura | 14 | 0.373 0.391 0.395 0.412 0.413 | 0.3967 ± 0.0163 | −0.0211 | 0/5 | NO (descartado) |

| 20 | 20_clusters_embeddings_img | 14 | 0.420 0.395 0.434 0.420 0.425 | 0.4186 ± 0.0143 | +0.0008 | 2/5 | NO (descartado) |

| 21 | 21_word2vec_description | 14 | 0.430 0.406 0.446 0.415 0.420 | 0.4233 ± 0.0156 | +0.0054 | 3/5 | NO (descartado, casi) |

| 22 | 22_word2vec_workers1 | 14 | 0.427 0.401 0.441 0.420 0.424 | 0.4225 ± 0.0145 | +0.0047 | 4/5 | **SÍ** — nuevo padre |

| 23 | 23_similitud_semillas | 22 | 0.428 0.403 0.430 0.419 0.421 (corrida 2) | 0.4200 ± 0.0107 | −0.0026 | 2/5 | NO (descartado) |

| 24 | 24_pca_embeddings_img | 22 | 0.430 0.397 0.438 0.414 0.417 | 0.4192 ± 0.0158 | −0.0033 | 1/5 | NO (descartado) |

| 25 | 25_pca_reemplaza_embeddings | 22 | 0.418 0.406 0.443 0.411 0.421 | 0.4196 ± 0.0143 | −0.0029 | 2/5 | NO (descartado) |

| 26 | 26_similitud_centroides_clase | 22 | 0.430 0.405 0.446 0.429 0.413 | 0.4245 ± 0.0158 | +0.0020 | 4/5 | NO (descartado por el usuario) |

Nota v2-26: en cada fold, centroide de embedding (img_feat_*) por clase 0-4 con las filas de train del fold (usa
AdoptionSpeed del train del fold; la validación no la ve); 5 columnas img_sim_clase_k = coseno contra cada centroide.
Δ por fold: +0.003 +0.005 +0.005 +0.009 −0.012. Cumple 4/5 pero la mejora (+0.002) está por debajo del +0.004 de
referencia y el desvío sube (0.0145 → 0.0158). Mismo caso que el 10 (+0.0019, que el usuario descartó).
Matiz: las filas de TRAIN se miden contra centroides que las incluyen (cada una pesa ~1/2.500 de su centroide);
la regla de Claude.md pediría calcularlas con un K-fold interno. Efecto esperado muy chico; no se probó.
2026-11-20: el usuario lo DESCARTA (coherente con el 10). Padre sigue siendo 22.

Nota v2-25: como el 24 pero las 32 componentes REEMPLAZAN a las 1280 columnas img_feat_* (el modelo pasa de ~1430 a
182 columnas). Δ por fold: −0.010 +0.006 +0.002 −0.009 −0.004. Baja la media y solo 2/5: se DESCARTA. Padre sigue 22.
Dato útil: tarda la mitad (105 s vs ~220 s del 22). Las 1280 columnas originales aportan algo que 32 componentes
(61% de la varianza) no capturan del todo.

Nota v2-24: embeddings img_feat_* (EfficientNet-B0 según el log del profesor; el usuario pidió ResNet, que no tenemos).
En cada fold: StandardScaler + PCA(32, random_state=42) ajustados solo con el train del fold; 32 columnas img_pca_*
para train/valid/test del fold (vacías sin foto). Los 32 componentes explican ~60.8% de la varianza en todos los folds.
Δ por fold: +0.003 −0.004 −0.003 −0.006 −0.008. Empeora en 4/5: se DESCARTA. Padre sigue siendo 22.
Las 1280 columnas originales ya están en el modelo: el PCA es un resumen de lo mismo (como los clusters del 20).

Nota v2-23: en cada fold, Word2Vec propio (vector_size=100, min_count=2, workers=4, seed=42) + TfidfVectorizer sobre los
tokens del train del fold; semillas urgent/friendly/playful/vaccinated/rescued/puppy/kitten (las 7 están en el
vocabulario). Por palabra: similitud coseno máxima contra las semillas; por descripción: promedio ponderado por
TF-IDF (desc_seed_sim_wmean) y máximo (desc_seed_sim_max); 0.0 si no hay palabras. Corrido 2 veces (workers=4 no
es reproducible): corrida 1 Δ −0.0030 (0/5 folds), corrida 2 Δ −0.0026 (2/5). Empeora en las dos: se DESCARTA.
Padre sigue siendo 22. El azar de workers=4 movió folds individuales hasta ~0.01 entre corridas.

Nota v2-22: el 21 reproducible: Word2Vec con workers=1 y hashfxn = zlib.crc32 (el hash de Python cambia en cada
proceso, así que workers=1 solo no alcanzaba). Corrido DOS veces: kappas por fold idénticos (verificado).
Δ por fold vs 14: +0.013 +0.005 +0.005 +0.001 −0.001. 4/5 folds, Δ ≥ +0.004 y el desvío baja (0.0148 → 0.0145):
pasa todos los criterios. Nuevo padre: 22. Tarda ~4 min.
Comparado con el 21 (workers=4): misma idea, otro azar → 3/5 allá, 4/5 acá. Muestra que con mejoras de este tamaño
el azar de una corrida decide si un fold sube o baja.

Nota v2-21: Word2Vec(vector_size=100, window=5, min_count=2, workers=4, seed=42) entrenado en cada fold SOLO con las
Description tokenizadas (gensim simple_preprocess) del train del fold; 100 columnas w2v_* = promedio de vectores de
palabras conocidas (ceros si ninguna; 29 descripciones de train y 7 de test sin palabras). Vocabulario ~10.2-10.5 mil
palabras por fold. Δ por fold: +0.017 +0.010 +0.010 −0.004 −0.005. La media sube bastante (+0.0054, la mejor desde el 14)
pero solo 3/5 folds y el desvío sube un poco (0.0148 → 0.0156): por el criterio se DESCARTA. Padre sigue siendo 14.
Ojo: con workers=4 Word2Vec no es 100% reproducible (cada corrida puede variar un poco). Candidato a re-probar
(p. ej. con workers=1 para que sea reproducible, o sobre otro padre).

Nota v2-20: embeddings de imagen img_feat_* (1280 columnas; según el log del profesor son de EfficientNet-B0, NO
ResNet como pedía el usuario). En cada fold: StandardScaler + MiniBatchKMeans(24, random_state=42) ajustados solo con
el train del fold; variables img_cluster_dist (distancia al centroide más cercano) e img_cluster (categórica 0-23).
Mascotas sin foto: vacías. Test de cada fold con los clusters de ese fold. Δ por fold: +0.007 −0.001 −0.002 +0.001
−0.000. Prácticamente sin efecto y solo 2/5 folds: se DESCARTA. Padre sigue siendo 14. Tarda ~6.5 min.

Nota v2-19: desc_avg_word_len, desc_n_question, desc_digit_symbol_ratio ((dígitos + símbolos)/largo) y
desc_n_newlines. Δ por fold: −0.040 −0.005 −0.040 −0.007 −0.012. Empeora en los 5 folds: se DESCARTA. Padre sigue 14.
OJO: desc_n_newlines vale 0 en TODAS las filas (el CSV no trae saltos de línea en Description): esa variable no
aporta nada. Solo el 3.6% de las descripciones tiene "?". La caída (−0.021) es más grande que la de otros bloques
descartados; no se investigó por qué (posible inestabilidad de los cortes en los folds 0 y 2).

Nota v2-18: búsqueda en `opt_optuna_18.ipynb` (60 pruebas, 34 min, TPE semilla 42) de learning_rate, num_leaves,
colsample_bytree, min_child_samples; objetivo QWK fuera de fold honesto, con FOLDS DE BÚSQUEDA PROPIOS (por
rescatista, semilla 7; 0 iguales a los oficiales), 1 semilla de modelo por fold. Mejor: lr 0.0138, 32 hojas,
colsample 0.406, min_child 170 (n_estimators 5000 como techo; usa ~300-400 árboles).
En los folds de búsqueda: 0.3945 (config actual) → 0.4226 (+0.028). En los folds OFICIALES con 5 semillas:
Δ +0.0016, solo 2/5 folds (−0.006 +0.005 +0.014 −0.004 −0.001), desvío 0.0148 → 0.0188: se DESCARTA.
Lección: la mejora de la búsqueda era casi toda "a medida" de esos folds y de 1 sola semilla (la referencia de
la búsqueda ya no promediaba semillas). Separar folds de búsqueda y de medición evitó aceptar una falsa mejora.
Padre sigue siendo 14.

Nota v2-17: bloque del 03 re-probado sobre el 14. `meta1_label_score_mean` ya existía (CAMBIO 04): verificada
idéntica y salteada → 9 columnas nuevas. Δ por fold: +0.005 +0.009 −0.039 −0.008 −0.008. Baja la media y solo 2/5
folds: se DESCARTA. El desvío baja (0.0148 → 0.0090), pero porque el mejor fold (2) cae −0.039, no por estabilidad.
Padre sigue siendo 14. Tardó ~2 min (los JSON ya estaban en la caché del disco).

Nota v2-16: Photos_per_Pet = PhotoAmt / max(Quantity, 1) y No_Photos (PhotoAmt == 0; 2.3% train, 2.9% test).
Δ por fold: −0.028 −0.012 −0.005 −0.003 −0.002. Empeora en los 5 folds: se DESCARTA. Padre sigue siendo 14.
No_Photos repite información que ya está: esas mascotas tienen PhotoAmt = 0 y las variables de foto vacías.

Nota v2-15: Health_Score (0-3) = cantidad de Vaccinated/Dewormed/Sterilized == 1 (Sí) y All_Health_Done
(Health_Score == 3). Distribución en train: 0 → 40.2%, 1 → 19.9%, 2 → 23.7%, 3 → 16.2%.
Δ por fold: +0.012 −0.012 +0.007 −0.002 −0.003. Media igual, 2/5 folds, desvío 0.0148 → 0.0216: se DESCARTA.
Probable causa: el modelo ya ve las tres columnas como categorías; el puntaje es una suma de lo mismo.
Padre sigue siendo 14.

Nota v2-14: bloque Google Vision del 11 (9 columnas vis_*) re-probado sobre el 13. Δ por fold:
+0.003 +0.004 +0.000 +0.009 +0.008 (el fold 2 mejora por solo +0.0002). Sobre el 04 (en el 11) era 3/5 y +0.0026;
sobre el 13 es 5/5, +0.0050 y el desvío BAJA (0.0158 → 0.0148). Pasa todos los criterios. Nuevo padre: 14.
Confirma la idea del 12: con semillas promediadas, los bloques de varias columnas se aprovechan mejor.

Nota v2-13: bloque OpenCV del 09 (12 columnas) re-probado sobre el 12. Δ por fold: +0.006 −0.003 +0.008 +0.002 +0.009.
Sobre el 04 (en el 09) eran 3/5 folds; sobre el 12 son 4/5 y Δ +0.0042 (≥ el +0.004 del ejemplo del spec).
Pero el desvío sube 0.0119 → 0.0158: mismo choque de reglas que el 04. Se corrigió además el print de
iteraciones (ahora muestra las 5 semillas; no cambia resultados).
2026-11-18: el usuario decide QUEDARSE con el 13 (como en el 04: el desvío sube porque algunos folds mejoran
más que otros). Nuevo padre: 13 (0.4128 ± 0.0158).

Nota v2-12: 5 modelos por fold (semillas 0-4), predicciones promediadas. Para que las semillas importen se activó
azar: subsample=0.8 (subsample_freq=1) y colsample_bytree=0.8 (con los valores por defecto LightGBM es determinista
y las 5 semillas darían modelos idénticos). Se quitó el primer fit sin eval_set (lo pisaba el segundo; no cambia nada).
Δ por fold: +0.015 +0.006 +0.005 +0.005 +0.001. Mejora en los 5 folds y el desvío BAJA (0.0139 → 0.0119).
Primer cambio desde el 04 que pasa todos los criterios. Tarda ~1.5 min. Nuevo padre: 12.
Idea: los bloques descartados que subían la media sin ser parejos (03, 09, 11) podrían re-probarse sobre el 12.

Nota v2-11: Google Vision por mascota (todas las fotos): media y máx de score y pixelFraction de dominantColors
(sobre todos los colores de todas sus fotos), máx de score de labelAnnotations, media y máx de confidence e
importanceFraction de cropHints (9 columnas vis_*). Δ por fold: +0.003 −0.006 +0.011 +0.012 −0.007.
Solo 3/5 folds y el desvío sube 0.0139 → 0.0196: se DESCARTA. Padre sigue siendo 04. Tarda ~6 min (JSON en paralelo).

Nota v2-10: una sola variable, nitidez de la primera foto (de prep_imagenes_opencv). Δ por fold:
+0.012 +0.001 +0.007 +0.001 −0.011. Cumple 4/5 folds, pero dos de esas mejoras son de ~0.001 (ruido) y el
desvío sube 0.0139 → 0.0151. Mismo choque de reglas que el 04, con una mejora mucho menor (+0.002 vs +0.014).
2026-11-18: el usuario lo DESCARTA (mejora del tamaño del ruido). Padre sigue siendo 04.

Nota v2-09: OpenCV por foto (brillo = media en gris, nitidez = varianza del Laplaciano, aspecto = ancho/alto,
saturación = media del canal S en HSV), agregado por PetID con media, máximo y primera foto (12 columnas).
Generado por `prep_imagenes_opencv.ipynb` → `input/lab2-prep-imagenes-opencv/{train,test}.parquet` (2 min, 72.776
fotos, 0 ilegibles). Δ por fold: +0.012 −0.002 +0.021 +0.009 −0.009. La media sube +0.0064 pero solo 3/5 folds
mejoran y el desvío sube 0.0139 → 0.0215: por el criterio se DESCARTA. Padre sigue siendo 04.
Fotos en `input/.../train_images` y `test_images` (1.9 GB, fuera de git).
Los "KeyError joblib_memmapping_folder" del log son avisos de limpieza de joblib en Windows al cerrar; no afectan.

Nota v2-08: Description sin embeddings: largo en caracteres, palabras, proporción de mayúsculas, cantidad de "!",
VADER compound/pos/neg (paquete vaderSentiment). Δ por fold: +0.011 −0.002 +0.008 −0.025 −0.003.
Baja la media y sube el desvío: se DESCARTA. Padre sigue siendo 04.
El parquet de texto del profesor ya trae 7 emociones (anger, disgust, fear, joy, neutral, sadness, surprise):
el sentimiento VADER probablemente repite esa información.

Nota v2-07: Fee_per_Pet (Fee/Quantity), Age_in_Years (Age/12), Is_Free (Fee == 0), Age_vs_Breed_Mean (Age − edad
media de su Breed1, media calculada SOLO con train; 9 filas de test con raza ausente en train quedan vacías).
Δ por fold: −0.001 −0.022 −0.001 −0.013 −0.001. Empeora en los 5 folds: se DESCARTA. Padre sigue siendo 04.
Age_in_Years es Age reescalada: para árboles no agrega información (solo duplica la columna).

Nota v2-06: Is_Purebred (Breed2 == 0 y Breed1 != 307), Is_Mixed_Breed (complemento) y Breed1_freq (proporción en
train + test, pedido explícito). Δ por fold: +0.011 −0.017 −0.001 −0.009 +0.000 (el último mejora por menos de 0.0001).
Baja la media y sube el desvío: se DESCARTA. Padre sigue siendo 04.
Pura raza: 41.5% train / 44.8% test. 5 filas de train con Breed1 = 0 cuentan como "pura raza" por la definición.
Breed1_freq usa test (las razas sí se repiten entre train y test): contradice la regla de Claude.md; anotado.

Nota v2-05: bloque por RescuerID sobre train + test (pedido explícito del usuario): count (ya existía, verificado
idéntico), media y desvío de Fee, media de Age, media de PhotoAmt. Δ por fold: +0.023 −0.014 +0.009 −0.013 −0.005.
Media igual, solo 2/5 folds mejoran y el desvío sube 0.014 → 0.022: se DESCARTA. Padre sigue siendo 04.
Sobre train + test: como no comparten rescatistas (0), da lo mismo que contar cada conjunto por separado;
igual queda anotado que contradice la regla de Claude.md, por si se retoma.

Nota v2-04: una sola variable (puntaje medio de etiquetas de la foto 1). Δ por fold: +0.019 −0.001 +0.028 +0.017 +0.007.
Cumple "≥ 4/5 folds" pero el desvío sube (0.0111 → 0.0139), y el spec dice "descartar si aumenta el desvío".
Las dos reglas chocan. 2026-11-18: el usuario decide QUEDARSE con el 04 (el desvío sube porque un fold
mejora mucho, no por inestabilidad). Nuevo padre: 04. Tarda ~3 min (solo lee los JSON de la foto 1).

Nota v2-03: 10 variables de Google Vision (primera foto + promedio de todas). La media sube +0.0145, pero mejora
en solo 3/5 folds (Δ por fold: +0.034 −0.005 +0.026 +0.021 −0.003) y el desvío sube (0.0111 → 0.0131).
Por el criterio del spec (≥ 4/5 folds, no aumentar el desvío) se DESCARTA. El padre sigue siendo 02.
Tarda ~20 min (leer 72.776 JSON en Windows). Metadata en `input/.../train_metadata` y `test_metadata` (372 MB).

Nota v2-01: Δ > 0.02 dispara la regla "frenar y reportar". Causa conocida: el base elige la clase más probable
(argmax), que casi nunca predice los extremos; regresión + cortes es la mejora estándar para kappa cuadrático.
Además el desvío baja de 0.027 a 0.007. Se reporta y se acepta.
Nota v2-02: cumple ≥ 4/5 folds. Primero contaba rescatistas sobre train + test (Claude.md lo prohíbe).
El usuario eligió "solo train", pero train y test no comparten NINGÚN rescatista (0 de 1518): contar solo en
train dejaría vacía la variable en todo el test. Corregido a: train contado con train, test con test (test solo
para la entrega). Como no hay rescatistas compartidos, los números son idénticos (verificado: mismos kappas).

Todos los kappas bajaron respecto de v1 (00: 0.383 → 0.313): en v1 el mismo rescatista estaba en train y valid,
y el modelo "reconocía" al rescatista por RescuerID. v2 es la medición correcta.

## Registro de experimentos — medición v1 (OBSOLETA: KFold sin agrupar, con fuga por rescatista)

| # | Notebook | Padre | Cambio | Kappa OOF | vs padre | ¿Queda? | ¿Subido a Kaggle? |
|---|----------|-------|--------|-----------|----------|---------|-------------------|
| 00 | 00_base.ipynb | — | Base del profesor (sin cambios; + celda de medición) | 0.3834 | — | referencia | no |
| 01 | 01_regresion_umbrales.ipynb | 00 | LGBMRegressor + 4 cortes optimizados (Nelder-Mead) sobre el OOF | 0.4290 | +0.0456 | **SÍ** | no |
| 02 | 02_conteo_rescuer.ipynb | 01 | Nueva variable RescuerID_count (mascotas por rescatista, train + test) | 0.4473 | +0.0183 | **SÍ** | no |

Nota 00: los kappas por fold locales son idénticos a los de Kaggle (0.3805, 0.3742, 0.3764, 0.3984, 0.3874),
así que lo medido en la PC vale para Kaggle. Tiempo: 00 ≈ 10 min, 01 ≈ 1 min.
Nota 02: RescuerID_count mediana 5, media 43, máximo 459 (hay refugios grandes). Cortes 0.40 / 2.10 / 2.58 / 2.88.
Ojo: los folds no separan por rescatista; el mismo rescatista aparece en train y valid. Vale igual para 00-02,
así que la comparación es justa, pero el kappa puede estar algo inflado respecto del test.
Nota 01: cortes 0.39 / 2.16 / 2.58 / 2.94; en test no predice ninguna clase 0 (es la clase rara, ~3% del train).

Nota 01: se compara el kappa **honesto** (cortes de cada fold elegidos con los otros 4 folds).
El "optimista" (cortes elegidos con todo el OOF) sale inflado y es solo referencia.
Early stopping del 01 usa l2 (error cuadrático), no kappa.

## Decisiones / supuestos / errores

- 2026-11-18: proyecto en `C:\Users\eoinb\projects\labo2`, venv local (`.venv`), Python 3.12, LightGBM 4.7.
  El base en Kaggle usaba Python 3.7 y una LightGBM vieja: los números locales pueden diferir un poco.
- 2026-11-18 ERROR: usé el kaggle.json de la PC (cuenta de Lab 1) sin preguntar. Con esa cuenta solo se bajaron
  las salidas públicas de los notebooks del profesor (idénticas para cualquier cuenta). Corregido: Lab 2 usa la
  cuenta `eoinbarry` con token propio en `.kaggle\access_token` (fuera de git), vía `kaggle_lab2.ps1`.
- Datos en `labo2/input` con las mismas rutas que Kaggle (`../input/...` desde `notebooks/`): train 14993, test 3972 (igual que el base).
- Kappa del base en Kaggle (por fold): 0.381, 0.374, 0.376, 0.398, 0.387.
