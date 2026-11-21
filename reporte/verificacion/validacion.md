# Validación con datos sintéticos

Comando desde la raíz: python -m choques validar.

PyFixest 0.70.0. 8 pruebas unitarias aprobadas.

- Diseño final: calibre por tratado heterogéneo; base limpia del mismo día; log con ceros y transformación previa al promedio; elegibilidad invariante a registros, cobertura, anomalías y episodios posteriores; segregación de Villa de Pozos y límites semanales; CRV3 con efectos fijos reestimados.
- Preparación: 366 días bisiestos por clave, dos accidentes con campos idénticos se retienen, un cero con continuidad, un faltante, día inválido, año ajeno y una exposición enlazada a dos fuentes sin duplicar el panel.
- Trazabilidad: rechazo de ZIP o panel alterado, fuente duplicada, nombre y fecha incompatibles. Una consolidación fallida conserva los insumos anteriores.
- Pista estatal: la excepción se aplica al par focal y el efecto conocido es 2.
- Culiacán: se exige el calendario previo completo, se aceptan 12 donantes para la comparación focal y la figura omite la brecha cuando no se puede calcular.
- Elegibilidad: control contaminado con cambio de 100, arrastre previo, anticipación, cobertura incompleta, fecha sin controles y efecto nulo.
- Reponderación: ATT de 5 con 1 y 3 tratados y efectos de 2 y 6.
- Regresión: matriz explícita de efectos fijos y congruencias con PyFixest en coeficiente y correcciones CRV1. EE estado 0.5579520177, GL 4; EE estado-fecha 0.5958029692, GL 4.
- Adopción única: comparación del día cero con pyfixest.lpdid en una cohorte y controles nunca tratados.
- Covariables municipales: cierre estricto, faltantes, confidencialidad y cero; claves y territorio; soporte y pesos compartidos; vecino 1:1, distancia, cero, desempate y reutilización; muestra común M0–M3; regresión ponderada, Wald matricial y conciliación de nueve cruces de hora y gravedad. Contraste nocturno por clase con covarianza compartida y celdas sin registros.
- Selección: cobertura con tres meses anteriores, anomalías de fecha, conteos publicados y corte de exposición en el día de inicio.
