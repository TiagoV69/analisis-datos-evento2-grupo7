# Analisis de Datos - Evento 2 - Grupo 7

Curso: Analisis de Datos | Docente: Daniel Alexis Nieto Mora | 2026-2

## Integrantes
- SANTIAGO VARELA JIMENEZ 

## Estructura
- `01_exploracion/` - Exploracion y seleccion de bases de datos
- `02_eda/` - Analisis exploratorio de datos
- `03_preprocesamiento/` - Preprocesamiento y reduccion de dimensionalidad
- `data/` - No se suben los datasets crudos por su peso, ver `data/README.md` para los enlaces de descarga
- `video/` - Guion y enlace del video final

## Como contribuir
Commits directos a `main`, cada quien trabaja en su carpeta correspondiente para evitar conflictos. Commits descriptivos y en espanol (ej: "Agrega revision de valores faltantes").

## Datasets explorados
1. **IBM HR Attrition** (tabular) - prediccion de rotacion de empleados
2. **Heart Disease UCI** (tabular) - prediccion de enfermedad cardiaca
3. **Intel Image Classification** (imagenes) - clasificacion de escenas, 6 clases, ~14000 imagenes

**Dataset seleccionado para las fases 2 y 3: Heart Disease.** Los otros dos se conservan como parte de la exploración exigida en la fase 1. Heart Disease permite trabajar con medidas continuas y categorías en una base de tamaño manejable; la selección se documenta al final del notebook de exploración.

## Avance actual
- HECHO Repositorio creado y estructurado
- HECHO Fase 1: exploracion, carga y justificacion de los 3 datasets
- [ ] Fase 2: analisis exploratorio de datos (EDA)
  - Implementadas las secciones 2.1–2.4 del análisis inicial y 2.5–2.8 de relaciones multivariadas, hipótesis, visualizaciones e insights. Pendiente de revisión conjunta del equipo.
- [ ] Fase 3: preprocesamiento y reduccion de dimensionalidad
- [ ] Video final

## Ejecutar el EDA

El análisis utiliza **Heart Disease** en [`02_eda/02_eda_heart.ipynb`](02_eda/02_eda_heart.ipynb), a partir de la misma fuente usada en la exploración y en la actualización del equipo. Se conservan sus secciones 2.1–2.4 y se añaden seis figuras multivariadas, cinco hipótesis y ocho hallazgos calculados desde los datos. Las figuras están en [`02_eda/figuras_heart/`](02_eda/figuras_heart/); las que comienzan por `00_` corresponden al análisis previo. No se reportan pruebas de significancia.

El notebook anterior se renombró para reflejar el dataset correcto y se retiraron del EDA las figuras de IBM HR. Esta copia de Heart Disease contiene códigos cuya recodificación no está claramente documentada: se usan las etiquetas `target = 0` y `target = 1`, sin asumir su equivalencia con ausencia o presencia de enfermedad. Se documentan un registro repetido y códigos por revisar en `ca` y `thal`, además de un análisis de sensibilidad.

Desde la raíz del repositorio:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/jupyter-execute --inplace --timeout=180 02_eda/02_eda_heart.ipynb
```

También se puede abrir el notebook en VS Code o Jupyter y seleccionar el entorno `.venv`. Se verificó con Python 3.14 y las versiones de `requirements.txt`. Al ejecutar todas las celdas se actualizan las salidas y las figuras.

El CSV se lee desde `data/Heart_Disease_UCI.csv`; si no existe, se descarga automáticamente de la fuente de la fase 1. Ver [`data/README.md`](data/README.md) para la procedencia, las limitaciones de la codificación y la huella del archivo analizado. Los datasets y `.venv` permanecen excluidos de Git.
