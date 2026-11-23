# Reproducción del escrito en una copia limpia

Este es el registro histórico de la reproducción analítica anterior a la
edición aprobada. El PDF final y su compilación editorial se identifican en
[revision-editorial.json](revision-editorial.json). No se repitió el flujo
completo durante la revisión editorial.


Fecha local 2026-11-22T13:58:14.
Copia worktrees/reproduccion-rjg8q7fb. La misma .venv cargó el código de la copia.
La descarga verificó los originales copiados por SHA-256 contra el manifiesto.
Se regeneraron 117 productos con SHA-256 idéntico.
El PDF conserva texto, distribución de líneas y saltos de página por pdftotext -layout.
PDF binario idéntico: sí; incluido en el inventario SHA-256.
La validación sintética tiene SHA-256 idéntico, sin normalizar su contenido.
El log completo se guarda en reproduccion-ejecucion.txt.

| Etapa | Segundos |
| --- | ---: |
| descargar | 2.09 |
| consolidar | 1.52 |
| preparar | 82.75 |
| validar | 7.95 |
| estimar | 245.38 |
| analizar | 4.84 |
| graficar | 6.32 |
| compilar | 4.82 |

## Productos cotejados

- data/inputs/episodios.csv
- data/inputs/fuentes_eventos.csv
- data/interim/atus.parquet
- data/interim/fecha_invalida.parquet
- data/processed/conteos_diarios.parquet
- data/processed/exposiciones.parquet
- data/processed/panel_diario.parquet
- data/processed/municipios/cambios_territoriales.csv
- data/processed/municipios/censo.parquet
- data/processed/municipios/conapo.parquet
- data/processed/municipios/saic.parquet
- data/processed/municipios/vmrc.parquet
- data/outputs/modelos/balance.csv
- data/outputs/modelos/causal_balance.csv
- data/outputs/modelos/causal_calendario.csv
- data/outputs/modelos/causal_cruce.csv
- data/outputs/modelos/causal_descartes.csv
- data/outputs/modelos/causal_efectos.csv
- data/outputs/modelos/causal_elegibilidad.csv
- data/outputs/modelos/causal_exclusiones_calendario.csv
- data/outputs/modelos/causal_fechas_base.csv
- data/outputs/modelos/causal_medicion.csv
- data/outputs/modelos/causal_morelia_donantes.csv
- data/outputs/modelos/causal_muestras.csv
- data/outputs/modelos/causal_omision_estado.csv
- data/outputs/modelos/causal_soporte.csv
- data/outputs/modelos/causal_uniones.csv
- data/outputs/modelos/causal_vinculos.csv
- data/outputs/modelos/causal_wald_semanal.csv
- data/outputs/modelos/cobertura_covariables.csv
- data/outputs/modelos/comparaciones_municipales.csv
- data/outputs/modelos/composicion_sensibilidades.csv
- data/outputs/modelos/covariables_por_fecha.csv
- data/outputs/modelos/culiacan.csv
- data/outputs/modelos/culiacan_controles.csv
- data/outputs/modelos/culiacan_descartes_territoriales.csv
- data/outputs/modelos/culiacan_placebos.csv
- data/outputs/modelos/culiacan_soporte.csv
- data/outputs/modelos/descartes_denominador_censal.csv
- data/outputs/modelos/descartes_muestra_comun.csv
- data/outputs/modelos/descartes_municipales.csv
- data/outputs/modelos/diagnosticos.csv
- data/outputs/modelos/estimaciones.csv
- data/outputs/modelos/franjas_x_gravedad.csv
- data/outputs/modelos/franjas_y_gravedad.csv
- data/outputs/modelos/frecuencias_franjas_x_gravedad.csv
- data/outputs/modelos/frecuencias_franjas_y_gravedad.csv
- data/outputs/modelos/historial.csv
- data/outputs/modelos/historial_pares.csv
- data/outputs/modelos/modelos_m0_m3.csv
- data/outputs/modelos/muestra.csv
- data/outputs/modelos/muestras_municipales.csv
- data/outputs/modelos/muestras_sensibilidades.csv
- data/outputs/modelos/pesos_por_fecha.csv
- data/outputs/modelos/reparto_controles.csv
- data/outputs/modelos/sensibilidades_seleccion.csv
- data/outputs/modelos/soporte_denominador_censal.csv
- data/outputs/modelos/soporte_municipal.csv
- data/outputs/modelos/tasas_saic.csv
- data/outputs/modelos/tasas_vmrc.csv
- data/outputs/modelos/tramos_y_base.csv
- data/outputs/modelos/vmrc_cobertura.csv
- data/outputs/modelos/vmrc_registros_no_municipales.csv
- data/outputs/modelos/wald_modelos.csv
- data/outputs/modelos/wald_previos.csv
- data/outputs/tablas/calendario.csv
- data/outputs/tablas/calidad.csv
- data/outputs/tablas/calidad.tex
- data/outputs/tablas/causal_balance.tex
- data/outputs/tablas/causal_balance_prepost.tex
- data/outputs/tablas/causal_bases.tex
- data/outputs/tablas/causal_calendario.tex
- data/outputs/tablas/causal_cifras.tex
- data/outputs/tablas/causal_cruce.tex
- data/outputs/tablas/causal_inferencia.tex
- data/outputs/tablas/causal_modelos.tex
- data/outputs/tablas/causal_omision.tex
- data/outputs/tablas/causal_perdidas.tex
- data/outputs/tablas/causal_persistencia.tex
- data/outputs/tablas/causal_placebo.tex
- data/outputs/tablas/causal_previos.tex
- data/outputs/tablas/causal_principales.tex
- data/outputs/tablas/causal_progresion_principal.tex
- data/outputs/tablas/causal_sensibilidades.tex
- data/outputs/tablas/causal_soporte.tex
- data/outputs/tablas/causal_trazabilidad.tex
- data/outputs/tablas/causal_uniones.tex
- data/outputs/tablas/causal_uniones_aux.tex
- data/outputs/tablas/cifras.tex
- data/outputs/tablas/comparacion_matching.tex
- data/outputs/tablas/contraste_nocturno_por_gravedad.tex
- data/outputs/tablas/descriptivos.csv
- data/outputs/tablas/descriptivos.tex
- data/outputs/tablas/efectos.csv
- data/outputs/tablas/horizontes.tex
- data/outputs/tablas/influencia.csv
- data/outputs/tablas/influencia.tex
- data/outputs/tablas/peso_estado.csv
- data/outputs/tablas/peso_id_episodio.csv
- data/outputs/tablas/principales.tex
- data/outputs/tablas/releases.csv
- data/outputs/tablas/resumen_catalogo.csv
- data/outputs/tablas/sensibilidad_matching.tex
- data/outputs/figuras/calendario.pdf
- data/outputs/figuras/calendario.png
- data/outputs/figuras/causal_dinamica.pdf
- data/outputs/figuras/causal_dinamica.png
- data/outputs/figuras/culiacan.pdf
- data/outputs/figuras/culiacan.png
- data/outputs/figuras/dinamica.pdf
- data/outputs/figuras/dinamica.png
- data/outputs/figuras/dinamica_municipal.pdf
- data/outputs/figuras/dinamica_municipal.png
- data/raw/manifiesto.csv
- data/raw/anios.csv
- data/outputs/modelos/validacion.md
- repo/reporte/main.pdf
