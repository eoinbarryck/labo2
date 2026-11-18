# Corre la herramienta de Kaggle con la cuenta de Lab 2 (token en .kaggle\access_token, fuera de git).
# Uso: .\kaggle_lab2.ps1 competitions list -s petfinder
$raiz = $PSScriptRoot
$env:KAGGLE_API_TOKEN = (Get-Content -Raw "$raiz\.kaggle\access_token").Trim()
$env:KAGGLE_CONFIG_DIR = "$raiz\.kaggle"   # evita usar el kaggle.json de Lab 1
& "$raiz\.venv\Scripts\kaggle.exe" @args
