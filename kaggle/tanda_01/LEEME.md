# Tanda 01 — notebook 14 (mejor local: QWK CV 0.4178 ± 0.0148)

Dos notebooks, en este orden (el 14 usa la salida del primero):

| # | Carpeta | Qué hace | Inputs en Kaggle |
|---|---------|----------|------------------|
| 1 | `lab2-prep-imagenes-opencv` | Mide brillo, nitidez, aspecto y saturación de cada foto; guarda `train.parquet` y `test.parquet` | competencia `petfinder-adoption-prediction` |
| 2 | `lab2-14-vision-agregados-sobre-13` | Entrega: genera `submission.csv` | competencia + `nickel/examen-lab-ii-preprocesado-texto` + `nickel/examen-lab-ii-preprocesado-img` + `eoinbarry/lab2-prep-imagenes-opencv` |

Antes de subir: completar **Integrantes** en la primera celda del 14.

## Subir (cuenta Lab 2 `eoinbarry`)

```powershell
C:\Users\eoinb\projects\labo2\kaggle_lab2.ps1 kernels push -p C:\Users\eoinb\projects\labo2\kaggle\tanda_01\lab2-prep-imagenes-opencv
```
Esperar a que termine (estado `complete`):
```powershell
C:\Users\eoinb\projects\labo2\kaggle_lab2.ps1 kernels status eoinbarry/lab2-prep-imagenes-opencv
```
Recién ahí subir el 14:
```powershell
C:\Users\eoinb\projects\labo2\kaggle_lab2.ps1 kernels push -p C:\Users\eoinb\projects\labo2\kaggle\tanda_01\lab2-14-vision-agregados-sobre-13
```
Cuando termine, enviar desde la página del notebook (pestaña de salida / `submit`), como indica el profesor.

## Qué mirar en el log de Kaggle del 14
- `Con fotos: train 0.977 | test 0.971` (si da 0, el input `lab2-prep-imagenes-opencv` no se conectó).
- `Kappa media: 0.41xx` — puede diferir un poco del local (otras versiones de scikit-learn/LightGBM pueden armar otros folds).
- No aparece "Folds verificados contra data/folds.csv": es normal, ese archivo solo existe en la PC.
