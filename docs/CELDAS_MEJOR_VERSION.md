# Celdas de la mejor versión (22) para pegar en el baseline

Versión 22_word2vec_workers1: **QWK 0.4225 ± 0.0145** en validación por rescatista.
El base del profesor da 0.3130 con la misma validación.

Las celdas van **en este orden**. El baseline tiene que tener las celdas del profesor:
- imports;
- lectura de train/test;
- categorías;
- los dos `.join` de los preprocesados;
- entrenamiento;
- submission.

Cada celda dice si es **NUEVA** o si **REEMPLAZA** una del baseline. Los cambios están marcados `# CAMBIO NN`, con el
mismo número que en la bitácora.

Las celdas que agregan columnas usan `unir`, definida en la celda 5. Así se pueden correr dos veces sin error.

**No hace falta ningún input extra.** Alcanzan la competencia y los dos preprocesados que el baseline ya usa. El bloque
de OpenCV (celda 6) calcula las estadísticas de las fotos ahí mismo; tarda unos minutos.

---

## Celda 1: REEMPLAZA la celda de imports

```python
# Importación de Librerías
import pandas as pd
import numpy as np                                          # CAMBIO 01

from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedGroupKFold   # CAMBIO VALIDACIÓN: folds por rescatista
from sklearn.metrics import cohen_kappa_score
from lightgbm import LGBMClassifier, LGBMRegressor, early_stopping   # CAMBIO 01: LGBMRegressor
from scipy.optimize import minimize                         # CAMBIO 01: para optimizar los umbrales

def metric(y_true, y_pred):
    res = cohen_kappa_score(y_true, y_pred.reshape((y_true.shape[0], 5), order="F").argmax(axis=1), weights= 'quadratic')
    return "kappa", res, True
```

## Celda 2: REEMPLAZA la celda que lee train/test y arma los folds

```python
train = pd.read_csv('../input/petfinder-adoption-prediction/train/train.csv').set_index("PetID")
test = pd.read_csv('../input/petfinder-adoption-prediction/test/test.csv').set_index("PetID")
# CAMBIO VALIDACIÓN: folds agrupados por rescatista (el mismo RescuerID nunca está en train y valid)
# y estratificados por AdoptionSpeed, semilla 42.
folds = [train.index[test_idx] for train_idx, test_idx in
         StratifiedGroupKFold(5, shuffle=True, random_state=42).split(train, train["AdoptionSpeed"], groups=train["RescuerID"])]
# folds = [train.index[test_idx] for train_idx, test_idx in KFold(5).split(train)]   # original
```

## Celda 3: sin cambios (la de `astype("category")`)

## Celda 4: NUEVA, después de la de categorías

```python
# CAMBIO 02: cantidad de mascotas publicadas por cada rescatista.
# Cada conjunto se cuenta por separado (ningún rescatista está en train y test a la vez).
train["RescuerID_count"] = train.groupby("RescuerID", observed=True)["RescuerID"].transform("size")
test["RescuerID_count"] = test.groupby("RescuerID", observed=True)["RescuerID"].transform("size")
```

## Celda 5: NUEVA

```python
# CAMBIO 04: puntaje medio de las etiquetas de Google Vision en la PRIMERA foto
import glob, json, os

def unir(df, nuevas):
    # CAMBIO ARREGLO: quita antes las columnas que ya estén, así la celda se puede correr dos veces sin error
    nuevas = nuevas.to_frame() if isinstance(nuevas, pd.Series) else nuevas
    return df.drop(columns=nuevas.columns, errors="ignore").join(nuevas)

def score_primera_foto(carpeta):
    valores = {}
    for ruta in glob.glob(os.path.join(carpeta, "*-1.json")):      # solo "<PetID>-1.json"
        pet_id = os.path.basename(ruta)[:-len("-1.json")]
        with open(ruta, encoding="utf-8") as f:
            etiquetas = [e.get("score", 0) for e in json.load(f).get("labelAnnotations", [])]
        valores[pet_id] = np.mean(etiquetas) if etiquetas else np.nan
    return pd.Series(valores, name="meta1_label_score_mean")

train = unir(train, score_primera_foto("../input/petfinder-adoption-prediction/train_metadata"))
test = unir(test, score_primera_foto("../input/petfinder-adoption-prediction/test_metadata"))
```

## Celda 6: NUEVA (tarda unos minutos: lee las ~72 000 fotos)

```python
# CAMBIO 13: brillo, nitidez, aspecto y saturación de las fotos con OpenCV, agregados por mascota (mean, max, primera foto)
import cv2
from joblib import Parallel, delayed

def stats_foto(ruta):
    pet_id, n = os.path.basename(ruta)[:-len(".jpg")].rsplit("-", 1)     # archivo "<PetID>-<n>.jpg"
    img = cv2.imread(ruta)
    if img is None:
        return {"PetID": pet_id, "foto": int(n)}
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    alto, ancho = gris.shape
    return {"PetID": pet_id, "foto": int(n),
            "brillo": float(gris.mean()),
            "nitidez": float(cv2.Laplacian(gris, cv2.CV_64F).var()),
            "aspecto": ancho / alto,
            "saturacion": float(hsv[:, :, 1].mean())}

VARIABLES_CV = ["brillo", "nitidez", "aspecto", "saturacion"]

def opencv_por_mascota(carpeta):
    rutas = glob.glob(os.path.join(carpeta, "*.jpg"))
    fotos = pd.DataFrame(Parallel(n_jobs=-1, batch_size=256)(delayed(stats_foto)(r) for r in rutas))
    g = fotos.groupby("PetID")[VARIABLES_CV]
    media = g.mean().add_prefix("img_cv_mean_")
    maximo = g.max().add_prefix("img_cv_max_")
    primera = fotos[fotos["foto"] == 1].set_index("PetID")[VARIABLES_CV].add_prefix("img_cv_first_")
    return media.join(maximo).join(primera)

train = unir(train, opencv_por_mascota("../input/petfinder-adoption-prediction/train_images"))
test = unir(test, opencv_por_mascota("../input/petfinder-adoption-prediction/test_images"))
print("Con fotos: train", train["img_cv_mean_brillo"].notna().mean().round(3),
      "| test", test["img_cv_mean_brillo"].notna().mean().round(3))
```

## Celda 7: NUEVA

```python
# CAMBIO 14: agregados por mascota de Google Vision (dominantColors, labelAnnotations, cropHints), todas las fotos
def valores_foto(ruta):
    # Google omite los campos que valen 0, por eso el valor por defecto es 0.
    pet_id = os.path.basename(ruta)[:-len(".json")].rsplit("-", 1)[0]
    with open(ruta, encoding="utf-8") as f:
        m = json.load(f)
    colores = m.get("imagePropertiesAnnotation", {}).get("dominantColors", {}).get("colors", [])
    recortes = m.get("cropHintsAnnotation", {}).get("cropHints", [])
    return (pet_id,
            [c.get("score", 0) for c in colores],
            [c.get("pixelFraction", 0) for c in colores],
            [e.get("score", 0) for e in m.get("labelAnnotations", [])],
            [r.get("confidence", 0) for r in recortes],
            [r.get("importanceFraction", 0) for r in recortes])

def vision_por_mascota(carpeta):
    fotos = Parallel(n_jobs=-1, batch_size=512)(delayed(valores_foto)(r) for r in glob.glob(os.path.join(carpeta, "*.json")))
    nombres = ["dom_score", "dom_pixfrac", "label_score", "crop_conf", "crop_importance"]
    filas = []
    for pet_id, *listas in fotos:                     # una fila por valor individual
        for nombre, lista in zip(nombres, listas):
            filas += [(pet_id, nombre, v) for v in lista]
    largo = pd.DataFrame(filas, columns=["PetID", "variable", "valor"])
    agg = largo.groupby(["PetID", "variable"])["valor"].agg(["mean", "max"]).unstack("variable")
    agg.columns = [f"vis_{var}_{estad}" for estad, var in agg.columns]
    pedidas = ["vis_dom_score_mean", "vis_dom_score_max", "vis_dom_pixfrac_mean", "vis_dom_pixfrac_max",
               "vis_label_score_max",
               "vis_crop_conf_mean", "vis_crop_conf_max", "vis_crop_importance_mean", "vis_crop_importance_max"]
    return agg[pedidas]

train = unir(train, vision_por_mascota("../input/petfinder-adoption-prediction/train_metadata"))
test = unir(test, vision_por_mascota("../input/petfinder-adoption-prediction/test_metadata"))
```

## Celda 8: NUEVA (tiene que ir ANTES de los `.join` de los preprocesados, porque ahí se borra el texto)

```python
# CAMBIO 22: Word2Vec sobre Description, entrenado SOLO con el train de cada fold (se usa en el entrenamiento)
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import zlib

# Tokens guardados aparte: el select_dtypes(exclude="O") de la celda siguiente saca la columna de texto
tokens_train = train["Description"].fillna("").astype(str).map(simple_preprocess)
tokens_test = test["Description"].fillna("").astype(str).map(simple_preprocess)

W2V_DIM = 100
W2V_COLS = [f"w2v_{k}" for k in range(W2V_DIM)]

def hash_fijo(texto):   # el hash de Python cambia en cada corrida; crc32 no -> resultado reproducible
    return zlib.crc32(texto.encode("utf-8"))

def vector_promedio(tokens, modelo):
    conocidas = [t for t in tokens if t in modelo.wv.key_to_index]
    return modelo.wv[conocidas].mean(axis=0) if conocidas else np.zeros(W2V_DIM)

def agregar_w2v(X_tr, X_va, X_te, tok_tr, tok_va, tok_te):
    modelo = Word2Vec(sentences=list(tok_tr), vector_size=W2V_DIM, window=5, min_count=2, workers=1, seed=42,
                      hashfxn=hash_fijo)
    salida = []
    for X, tok in ((X_tr, tok_tr), (X_va, tok_va), (X_te, tok_te)):
        vectores = pd.DataFrame(np.vstack([vector_promedio(t, modelo) for t in tok]), index=X.index, columns=W2V_COLS)
        salida.append(pd.concat([X, vectores], axis=1))
    return salida
```

## Celdas 9 y 10: sin cambios (los dos `.join` de los preprocesados de texto e imagen)

## Celda 11: REEMPLAZA la celda de entrenamiento

```python
# CAMBIO 12: semillas a promediar en cada fold
SEMILLAS = [0, 1, 2, 3, 4]

fold_preds = []
test_preds = []
for i, fold in enumerate(folds):
    X_train = train.drop(fold).drop("AdoptionSpeed", axis=1).select_dtypes(exclude="O")
    y_train = train.drop(fold)["AdoptionSpeed"]

    X_valid = train.loc[fold].drop("AdoptionSpeed", axis=1).select_dtypes(exclude="O")
    y_valid = train.loc[fold, "AdoptionSpeed"]

    # CAMBIO 22: Word2Vec entrenado con las descripciones del train de este fold; vectores para train, valid y test
    X_train, X_valid, X_test = agregar_w2v(
        X_train, X_valid, test[X_train.columns],
        tokens_train.loc[X_train.index], tokens_train.loc[X_valid.index], tokens_test.loc[test.index])

    # CAMBIO 12: un modelo por semilla, con 80% de filas y columnas al azar; se promedian las predicciones
    pred_valid, pred_test = [], []
    for semilla in SEMILLAS:
        # CAMBIO 01: regresión en vez de clasificación
        learner = LGBMRegressor(random_state=semilla, subsample=0.8, subsample_freq=1, colsample_bytree=0.8)
        # learner = LGBMClassifier()   # original
        # learner.fit(X_train, y_train, )   # original: quitado, el fit siguiente lo reemplazaba

        # CAMBIO 01: sin eval_metric=metric (es para 5 probabilidades); el early stopping usa el error cuadrático
        learner.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_valid, y_valid)],
                    callbacks=[early_stopping(5, verbose=False)])
        pred_valid.append(learner.predict(X_valid))
        pred_test.append(learner.predict(X_test[X_train.columns]))
    fold_preds.append(pd.Series(np.mean(pred_valid, axis=0), index=fold, name="AdoptionSpeed"))
    test_preds.append(pd.Series(np.mean(pred_test, axis=0), index=test.index))

fold_preds = pd.concat(fold_preds)
# CAMBIO 01: promedio de los 5 folds; los umbrales se aplican en la celda siguiente
test_preds = sum(test_preds) / len(test_preds)
```

## Celda 12: NUEVA, después del entrenamiento y antes de la submission

```python
# CAMBIO 01: umbrales optimizados para pasar del número continuo a la clase 0-4
def aplicar_cortes(pred, cortes):
    return np.digitize(pred, np.sort(cortes))     # 4 cortes ordenados -> clases 0..4

def optimizar_cortes(pred, y, inicio=(0.5, 1.5, 2.5, 3.5)):
    perdida = lambda c: -cohen_kappa_score(y, aplicar_cortes(pred, c), weights="quadratic")
    return np.sort(minimize(perdida, inicio, method="nelder-mead").x)

y_oof = train.loc[fold_preds.index, "AdoptionSpeed"]

# Medición honesta: los cortes de cada fold se eligen con los OTROS 4 folds
oof_clases = []
for fold in folds:
    resto = fold_preds.index.difference(fold)
    c = optimizar_cortes(fold_preds[resto], y_oof[resto])
    oof_clases.append(pd.Series(aplicar_cortes(fold_preds[fold], c), index=fold))
oof_clases = pd.concat(oof_clases)
kappas = [cohen_kappa_score(y_oof[f], oof_clases[f], weights="quadratic") for f in folds]
print("Kappa por fold:", [round(k, 4) for k in kappas])
print(f"Kappa media: {np.mean(kappas):.4f} ± {np.std(kappas, ddof=1):.4f}")

# Para la entrega: cortes elegidos con TODO el OOF
cortes = optimizar_cortes(fold_preds, y_oof)
print("Cortes:", np.round(cortes, 3))
test_preds = pd.Series(aplicar_cortes(test_preds, cortes), index=test_preds.index, name="AdoptionSpeed")
test_preds.value_counts().sort_index()
```

## Celda 13: sin cambios (`test_preds.to_csv("submission.csv")`)
