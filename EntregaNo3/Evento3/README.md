# Análisis de datos de COVID-19

Proyecto de Business Intelligence basado en datos de **Our World in Data (OWID)** para el análisis mundial del COVID-19 entre enero de 2020 y agosto de 2024.

## Integrantes

- Leidy Melissa Trejos Pamplona
- Ferney Orlando López Copete
- Santiago Varela Jiménez
- Jose Ricardo Quiros Garcia

## Objetivo

Transformar los datos históricos de COVID-19 en información útil para la toma de decisiones, mediante la preparación de un modelo de datos, la definición de KPIs y la validación estadística de la relación entre mortalidad, PIB per cápita y cobertura de vacunación.

## Metodología

Se limpiaron y transformaron los datos de OWID, eliminando agregados y duplicados y organizándolos en un modelo estrella con dimensiones de país y tiempo. Se definieron seis KPIs: mortalidad acumulada por millón, cobertura completa, brecha de vacunación, mortalidad mensual, incidencia mensual y letalidad. Las hipótesis se evaluaron con correlación de Spearman, pruebas de Welch y Mann–Whitney, usando un nivel de significancia de 0,05 y análisis de sensibilidad para controlar PIB y envejecimiento poblacional.

## Resultados

- 775.900.191 casos y 7.058.885 muertes reportadas.
- Mortalidad global: 884,78 muertes por millón.
- Cobertura completa ponderada: 65,32%.
- Letalidad acumulada: 0,91%.
- PIB y mortalidad: ρ = 0,601; p < 0,001, asociación positiva contraria a la esperada.
- Vacunación y mortalidad: ρ = 0,156; p = 0,0217, asociación cruda débil e inestable al controlar variables de contexto.

## Conclusiones

Los resultados muestran asociaciones estadísticas, pero no permiten establecer causalidad. Las relaciones cambian al considerar edad, ingreso, calidad del reporte y temporalidad, por lo que no es válido concluir que un mayor PIB o la vacunación causen más mortalidad. Los KPIs deben utilizarse para monitorear tendencias, comparar territorios y priorizar países con mortalidad reciente elevada, brechas de cobertura y poblaciones envejecidas.
