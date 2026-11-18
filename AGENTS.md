# AGENTS.md — PetFinder Adoption Prediction

> Plantilla para la raíz de tu repo. La leen Codex, Cursor, Copilot y otros agentes.
> Para Claude Code: copiala como `CLAUDE.md` o creá un `CLAUDE.md` con la línea `@AGENTS.md`.
> Adaptá todo lo que esté entre `<< >>` y borrá lo que no aplique. Más corto y preciso > más largo.

## Objetivo
Predecir `AdoptionSpeed` (0–4, ordinal) de mascotas publicadas en PetFinder.my.
Métrica oficial: **Quadratic Weighted Kappa (QWK)**. Cualquier cambio se juzga por QWK en CV, no por intuición.

## Datos (`<<data/>>`, NO versionado, NO modificar)
- `train.csv` / `test.csv`: una fila por publicación. Clave: `PetID`. Agrupador: `RescuerID`.
- `breed_labels.csv`, `color_labels.csv`, `state_labels.csv`: diccionarios de códigos.
- `train_images/`, `test_images/`: `<PetID>-<n>.jpg` (n = 1..PhotoAmt).
- `train_metadata/`, `test_metadata/`: JSON de Google Vision por imagen (labels, colores, crop hints).
- `train_sentiment/`, `test_sentiment/`: JSON de Google Natural Language sobre `Description`.
- Target: 0 = mismo día · 1 = 1–7 días · 2 = 8–30 · 3 = 31–90 · 4 = sin adopción a los 100 días.

## Validación (no negociable)
- CV: `<<StratifiedGroupKFold(n_splits=5), groups=RescuerID, seed=42>>`. El mismo rescatista no puede estar en train y valid.
- Los folds viven en `<<data/folds.csv>>`. **Nunca regenerarlos** sin que lo pida explícitamente.
- Reportar siempre: QWK por fold, media y desvío, y delta contra el baseline vigente.
- Los thresholds para pasar de regresión a clases 0–4 se optimizan **solo con datos de train de cada fold**.

## Reglas anti-leakage
- No leer `test.csv` para nada que no sea generar el submission final.
- Encodings, TF-IDF, SVD, escalados: `fit` dentro del fold, sobre train del fold.
- No usar features derivadas del target fuera de fold (target encoding siempre out-of-fold).
- Si el QWK de CV sube más de `<<0.02>>` de golpe: **detenerse y reportar**, no seguir iterando.

## Estructura del repo
- `src/features/`: una función por grupo de features; reciben y devuelven DataFrame indexado por `PetID`.
- `src/train.py`: entrena con un config YAML de `configs/`.
- `experiments/`: un archivo `EXP-###.md` por experimento (ver `spec-experimento.md`).
- `experiments/log.csv`: `exp_id, fecha, descripcion, qwk_cv_mean, qwk_cv_std, decision`.

## Comandos
- Instalar: `<<pip install -r requirements.txt>>`
- Correr CV: `<<python src/train.py --config configs/baseline.yaml>>`
- Tests rápidos: `<<pytest -q>>`

## Cómo trabajar conmigo (para el agente)
- Antes de codear: leé el spec del experimento y confirmá en 3 líneas qué vas a cambiar.
- Cambios mínimos y acotados al spec. No refactorizar lo que no pide el spec.
- No cambiar la métrica, los folds ni la semilla.
- Al terminar: actualizar `experiments/log.csv` y escribir un resumen con resultado, deltas y dudas.
- Si algo es ambiguo, preguntar en vez de suponer.
