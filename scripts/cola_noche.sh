# Fila de la noche: traducción + notebooks 30 a 45, uno detrás del otro.
# Lo lanza cola_noche.ps1 (tarea programada de Windows "labo2_cola_noche").
cd /c/Users/eoinb/projects/labo2/notebooks
LOG=../docs/cola_noche.log
export HF_HUB_DISABLE_SYMLINKS_WARNING=1 PYTHONIOENCODING=utf-8
echo "inicio $(date)" > $LOG
for n in prep_traduccion 30_descripcion_ingles 31_texto_liviano_vader_ingles 32_texto_estructura_ingles 33_similitud_semillas_ingles 34_vecinos_texto_ingles 35_coseno_imagen_texto_ingles 36_nombre_tierno_corto 37_camada_vs_rescatista 38_entropia_colores_foto1 39_w2v_tierno_vs_urgente 40_deficit_fotos_rescatista 41_letras_alargadas 42_edad_vs_color1 43_imagen_rapido_vs_clavo 44_indice_grito 45_proyeccion_aleatoria_imagen; do
  t0=$(date +%s)
  if ../.venv/Scripts/jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 $n.ipynb > /dev/null 2>&1; then r=OK; else r=ERROR; fi
  echo "$n $r $(( ($(date +%s)-t0)/60 )) min $(date +%H:%M)" >> $LOG
done
echo "fin $(date)" >> $LOG
