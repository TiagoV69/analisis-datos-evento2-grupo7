# Datos del proyecto

Los archivos de datos se conservan localmente y están excluidos de Git. Este README sí se versiona.

## Heart Disease: base seleccionada para el EDA y la fase 3

- [CSV utilizado en la exploración y en el EDA del equipo](https://raw.githubusercontent.com/sharmaroshan/Heart-UCI-Dataset/master/heart.csv).
- Guardar como `data/Heart_Disease_UCI.csv`.
- Copia analizada: 303 registros, 14 columnas, 138 registros de clase 0 y 165 de clase 1.
- Se identifica una fila idéntica adicional: 302 registros únicos, sin identificador de paciente para decidir automáticamente si corresponde eliminarla.
- SHA-256 del archivo descargado: `7c3014365675306819510a49ff289efbec1d1a6a666a2dc7652f1547b383d859`.

El notebook `02_eda/02_eda_heart.ipynb` lee primero este archivo local. Si no existe, utiliza la URL de la exploración y guarda una copia. Las siguientes ejecuciones pueden hacerse sin conexión. El notebook imprime la huella de la copia local; una nueva serialización del CSV puede cambiarla aunque conserve sus valores. El enlace apunta a una rama que puede cambiar: conservar el archivo permite reproducir la ejecución documentada.

### Procedencia y códigos

La [documentación de UCI](https://archive.ics.uci.edu/dataset/45/heart+disease) corresponde al conjunto original. El archivo usado por el equipo procede de una [copia recodificada en GitHub](https://github.com/sharmaroshan/Heart-UCI-Dataset). Su README describe el objetivo original `num`, con valores 0–4, pero el CSV tiene `target` binario; tampoco explica por completo las transformaciones de las categorías.

El análisis mantiene **clase 0 y clase 1** sin asignarles significado clínico. Se debe verificar la correspondencia de `target` antes de interpretar presencia o ausencia de enfermedad. También se conservan y señalan los cinco registros con `ca=4` y los dos con `thal=0` para revisar su recodificación. El EDA incluye un escenario temporal sin estos códigos y sin filas repetidas, sin modificar el archivo original.

## Otras bases de la exploración

- **IBM HR Attrition:** [CSV utilizado en el notebook de exploración](https://raw.githubusercontent.com/pplonski/datasets-for-start/refs/heads/master/employee_attrition/HR-Employee-Attrition-All.csv).
- **Intel Image Classification:** la fase 1 espera las carpetas de clases en `data/seg_train/seg_train/`. El notebook no incluye un enlace de descarga de estas imágenes.

Estas dos bases se conservan en la exploración, pero no se requieren para ejecutar el EDA seleccionado de Heart Disease.
