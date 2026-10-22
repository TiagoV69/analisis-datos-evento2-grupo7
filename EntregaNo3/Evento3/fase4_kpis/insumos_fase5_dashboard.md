# Traspaso de las fases 4 y 6 a la fase 5

Este archivo no implementa la fase 5. Define una guía para que el dashboard sea consistente con los KPIs y las conclusiones estadísticas ya validadas.

## Modelo

Importar desde `fase3_preparacion_data/datos_procesados`:

- `dim_pais.csv`
- `dim_tiempo.csv`
- `fact_covid_mensual.csv`

Crear relaciones uno a muchos desde ambas dimensiones hacia la tabla de hechos. No relacionar `resumen_pais.csv` con el modelo principal; puede usarse como tabla de comprobación, no como una segunda tabla de hechos activa.

## Propuesta de páginas y visualizaciones

### Página 1 · Resumen ejecutivo

1. **Tarjetas:** mortalidad acumulada por millón, cobertura completa, brecha de cobertura, incidencia mensual, mortalidad mensual y letalidad.
2. **Línea temporal:** casos y muertes nuevas por mes; preferiblemente con dos gráficos alineados para no mezclar escalas.
3. **Mapa coroplético:** mortalidad acumulada por millón por país.
4. **Barras horizontales:** diez países con mayor mortalidad por millón; permitir excluir microestados.
5. **Matriz o tabla con formato condicional:** país, cobertura, brecha, mortalidad por millón e incidencia del último mes.

### Página 2 · Validación de hipótesis

1. **Dispersión H1:** PIB per cápita en eje X, mortalidad por millón en Y, color por continente y tamaño por población. Usar escala logarítmica en X.
2. **Dispersión H2:** cobertura completa en X y mortalidad por millón en Y, color por grupo de edad o ingreso.
3. **Barras por cuartil de ingreso:** mediana de mortalidad por millón; usar mediana para reducir el efecto de valores extremos.
4. **Barras por nivel de vacunación:** mediana de mortalidad por millón, acompañada del número de países del grupo.
5. **Caja y bigotes**, si la herramienta lo permite: distribución de mortalidad por nivel de vacunación o cuartil de ingreso.

## Interactividad mínima

- Segmentadores sincronizados: continente, país, grupo de ingreso, grupo de edad, nivel de vacunación y fecha.
- Seleccionar un continente debe filtrar mapa, series, tarjetas y tabla.
- Un botón debe restablecer filtros.
- Los tooltips deben mostrar población, último mes reportado y si es microestado.
- Mostrar el aviso de periodo parcial cuando el corte sea agosto de 2024.

## Mensajes que sí puede mostrar el dashboard

- “Se observa una asociación positiva entre PIB y mortalidad reportada; no implica causalidad”.
- “La asociación cruda entre vacunación y mortalidad es débil y cambia al controlar variables de contexto”.
- “Los resultados agregados por país no permiten estimar eficacia individual de las vacunas”.

## Mensajes que deben evitarse

- “El PIB causa más muertes”.
- “Las vacunas aumentan la mortalidad”.
- “La vacunación no funciona”.
- “África fue el continente menos afectado” sin añadir la advertencia sobre subregistro, estructura etaria y capacidad diagnóstica.
