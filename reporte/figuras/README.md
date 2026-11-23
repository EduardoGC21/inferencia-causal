# Mapa de contexto

`mapa-municipios.png` es la figura que utiliza el apéndice F. Representa los municipios
de la muestra principal ya estimada, sin modificar sus pares, pesos o resultados.
Los dos paneles separan tratados y controles; un mismo municipio puede aparecer
en ambos en fechas distintas. El gris indica que no pertenece al grupo del panel.
Las superficies coloreadas no representan efectos ni tasas de siniestros.

La cartografía corresponde al Marco Geoestadístico del INEGI de diciembre de
2025, obtenida previamente del servicio del catálogo municipal. Se usa como
referencia geográfica actual y no como reconstrucción de límites históricos.
`mapa_muestra.json` conserva fuentes, metadatos y huellas de los 32 archivos
geográficos y de la muestra. La proyección es equirectangular, paralelo 23 N;
no se calculan áreas ni distancias.

Para regenerar sólo la figura desde el checkout, con la cartografía local:

```powershell
& ../../../.venv/Scripts/python.exe reporte/figuras/generar_mapa.py `
  --cartografia ../../../data/raw/cartografia-muestra `
  --muestra ../data/outputs/modelos/causal_muestras.csv
```

La compilación utiliza la figura entregada. No descarga cartografía ni vuelve
a estimar los modelos. La copia de reproducción incluye esta carpeta como
parte de las fuentes del documento.

## Trayectoria de siniestros registrados

`conteos-por-grupo.pdf` (figura 1a) muestra los promedios diarios
ponderados del día -28 al +13 y sombrea la base de los días -28 a -8.
`cambios-por-grupo.pdf` (figura 1b) muestra los cambios de cada grupo
frente a su propia base. Ambos paneles usan las series de la diapositiva 7.
Para reproducirlos desde la raíz del árbol de trabajo:

```powershell
& ../../.venv/Scripts/python.exe reporte/figuras/generar_series.py
```

El script lee los CSV `series-eventos.csv` y `efectos.csv` de
`presentacion/assets/datos/` y coteja la brecha entre grupos con los 21
coeficientes diarios de $M_0$ para el emparejamiento 1:muchos.

`trayectoria-siniestros.png` es la figura 1c. La función `figures` de
`src/choques/informe_final.py` la genera desde resultados existentes.
Distingue matching 1:muchos y 1:1; las barras representan intervalos del
95 % agrupados por estado y fecha. Las etiquetas y la presentación se
actualizaron sin reestimar modelos.
