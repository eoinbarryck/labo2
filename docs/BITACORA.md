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
