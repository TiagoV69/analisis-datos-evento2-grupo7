"""Reproduce las pruebas y cifras usadas en las fases 4 y 6.

Dependencias: pandas, numpy y scipy.
Ejecución desde cualquier carpeta:
    python validacion_estadistica.py

El script solo usa los CSV congelados de la fase 3. No descarga datos.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "fase3_preparacion_data" / "datos_procesados"
OUTPUT = Path(__file__).resolve().parent / "resultados"
OUTPUT.mkdir(exist_ok=True)
ALPHA = 0.05
RNG = np.random.default_rng(20261021)


def intervalo_bootstrap_spearman(x, y, repeticiones=10_000):
    """IC percentil 95% con semilla fija para una correlación de Spearman."""
    x = np.asarray(x)
    y = np.asarray(y)
    n = len(x)
    indices = RNG.integers(0, n, size=(repeticiones, n))
    valores = np.array(
        [stats.spearmanr(x[i], y[i]).statistic for i in indices]
    )
    return np.quantile(valores, [0.025, 0.975])


def correlacion_parcial_spearman(datos, x, y, controles):
    """Correlación entre residuos de rangos después de ajustar controles."""
    columnas = [x, y, *controles]
    muestra = datos[columnas].dropna()
    rangos = muestra.rank(method="average")
    z = np.column_stack(
        [np.ones(len(rangos)), *(rangos[c].to_numpy() for c in controles)]
    )
    residuo_x = rangos[x].to_numpy() - z @ np.linalg.lstsq(
        z, rangos[x].to_numpy(), rcond=None
    )[0]
    residuo_y = rangos[y].to_numpy() - z @ np.linalg.lstsq(
        z, rangos[y].to_numpy(), rcond=None
    )[0]
    resultado = stats.pearsonr(residuo_x, residuo_y)
    return len(muestra), resultado.statistic, resultado.pvalue


resumen = pd.read_csv(DATA / "resumen_pais.csv")
fact = pd.read_csv(DATA / "fact_covid_mensual.csv")
dim_pais = pd.read_csv(DATA / "dim_pais.csv")

pruebas = []

# H1: PIB per cápita frente a mortalidad acumulada por millón.
h1 = resumen[["pib_per_capita", "muertes_por_millon"]].dropna()
resultado_h1 = stats.spearmanr(h1["pib_per_capita"], h1["muertes_por_millon"])
ic_h1 = intervalo_bootstrap_spearman(
    h1["pib_per_capita"], h1["muertes_por_millon"]
)
pruebas.append(
    {
        "hipotesis": "H1",
        "prueba": "Spearman: PIB vs mortalidad acumulada por millón",
        "n": len(h1),
        "estadistico": resultado_h1.statistic,
        "p_valor": resultado_h1.pvalue,
        "ic95_inferior": ic_h1[0],
        "ic95_superior": ic_h1[1],
        "decision_h0_alpha_0_05": "Rechazar H0",
        "lectura": "Asociación positiva; dirección contraria a la esperada",
    }
)

n, estadistico, p_valor = correlacion_parcial_spearman(
    resumen,
    "pib_per_capita",
    "muertes_por_millon",
    ["pct_mayores_65"],
)
pruebas.append(
    {
        "hipotesis": "H1 - sensibilidad",
        "prueba": "Spearman parcial controlando % mayores de 65",
        "n": n,
        "estadistico": estadistico,
        "p_valor": p_valor,
        "ic95_inferior": np.nan,
        "ic95_superior": np.nan,
        "decision_h0_alpha_0_05": "Rechazar H0" if p_valor < ALPHA else "No rechazar H0",
        "lectura": "La asociación se reduce de forma importante al ajustar edad",
    }
)

# H2: cobertura final frente a mortalidad acumulada por millón.
h2 = resumen[["pct_vacunacion_completa", "muertes_por_millon"]].dropna()
resultado_h2 = stats.spearmanr(
    h2["pct_vacunacion_completa"], h2["muertes_por_millon"]
)
ic_h2 = intervalo_bootstrap_spearman(
    h2["pct_vacunacion_completa"], h2["muertes_por_millon"]
)
pruebas.append(
    {
        "hipotesis": "H2",
        "prueba": "Spearman: vacunación completa vs mortalidad acumulada",
        "n": len(h2),
        "estadistico": resultado_h2.statistic,
        "p_valor": resultado_h2.pvalue,
        "ic95_inferior": ic_h2[0],
        "ic95_superior": ic_h2[1],
        "decision_h0_alpha_0_05": "Rechazar H0",
        "lectura": "Asociación débil positiva; dirección contraria a la esperada",
    }
)

mediana_cobertura = h2["pct_vacunacion_completa"].median()
alta = h2.loc[
    h2["pct_vacunacion_completa"] >= mediana_cobertura, "muertes_por_millon"
]
baja = h2.loc[
    h2["pct_vacunacion_completa"] < mediana_cobertura, "muertes_por_millon"
]
welch = stats.ttest_ind(alta, baja, equal_var=False)
mann_whitney = stats.mannwhitneyu(alta, baja, alternative="two-sided")

for nombre, resultado, lectura in [
    (
        "Welch: mortalidad en países sobre/bajo mediana de vacunación",
        welch,
        "Diferencia de medias no significativa",
    ),
    (
        "Mann-Whitney: mortalidad sobre/bajo mediana de vacunación",
        mann_whitney,
        "Diferencia de distribución limítrofe y en dirección contraria",
    ),
]:
    pruebas.append(
        {
            "hipotesis": "H2",
            "prueba": nombre,
            "n": len(h2),
            "estadistico": resultado.statistic,
            "p_valor": resultado.pvalue,
            "ic95_inferior": np.nan,
            "ic95_superior": np.nan,
            "decision_h0_alpha_0_05": (
                "Rechazar H0" if resultado.pvalue < ALPHA else "No rechazar H0"
            ),
            "lectura": lectura,
        }
    )

n, estadistico, p_valor = correlacion_parcial_spearman(
    resumen,
    "pct_vacunacion_completa",
    "muertes_por_millon",
    ["pib_per_capita", "pct_mayores_65"],
)
pruebas.append(
    {
        "hipotesis": "H2 - sensibilidad",
        "prueba": "Spearman parcial controlando PIB y % mayores de 65",
        "n": n,
        "estadistico": estadistico,
        "p_valor": p_valor,
        "ic95_inferior": np.nan,
        "ic95_superior": np.nan,
        "decision_h0_alpha_0_05": "Rechazar H0" if p_valor < ALPHA else "No rechazar H0",
        "lectura": "Asociación ajustada negativa; evidencia de confusión",
    }
)

# Sensibilidad temporal: cobertura al cierre de 2021 y muertes desde 2022.
vac_2021 = fact.loc[
    fact["anio_mes"] == "2021-12", ["iso_code", "pct_vacunacion_completa"]
].rename(columns={"pct_vacunacion_completa": "vac_dic_2021"})
muertes_posteriores = (
    fact.loc[fact["anio_mes"] >= "2022-01"]
    .groupby("iso_code", as_index=False)["muertes_nuevas"]
    .sum()
    .rename(columns={"muertes_nuevas": "muertes_desde_2022"})
)
temporal = (
    dim_pais[
        ["iso_code", "poblacion", "pib_per_capita", "pct_mayores_65"]
    ]
    .merge(vac_2021, on="iso_code")
    .merge(muertes_posteriores, on="iso_code")
)
temporal["mortalidad_desde_2022_pm"] = (
    temporal["muertes_desde_2022"] / temporal["poblacion"] * 1_000_000
)
temporal_crudo = temporal[["vac_dic_2021", "mortalidad_desde_2022_pm"]].dropna()
resultado_temporal = stats.spearmanr(
    temporal_crudo["vac_dic_2021"], temporal_crudo["mortalidad_desde_2022_pm"]
)
pruebas.append(
    {
        "hipotesis": "H2 - sensibilidad temporal",
        "prueba": "Cobertura dic-2021 vs mortalidad desde ene-2022",
        "n": len(temporal_crudo),
        "estadistico": resultado_temporal.statistic,
        "p_valor": resultado_temporal.pvalue,
        "ic95_inferior": np.nan,
        "ic95_superior": np.nan,
        "decision_h0_alpha_0_05": "Rechazar H0",
        "lectura": "Asociación cruda positiva; puede reflejar confusión",
    }
)

n, estadistico, p_valor = correlacion_parcial_spearman(
    temporal,
    "vac_dic_2021",
    "mortalidad_desde_2022_pm",
    ["pib_per_capita", "pct_mayores_65"],
)
pruebas.append(
    {
        "hipotesis": "H2 - sensibilidad temporal",
        "prueba": "Correlación temporal parcial controlando PIB y edad",
        "n": n,
        "estadistico": estadistico,
        "p_valor": p_valor,
        "ic95_inferior": np.nan,
        "ic95_superior": np.nan,
        "decision_h0_alpha_0_05": "Rechazar H0" if p_valor < ALPHA else "No rechazar H0",
        "lectura": "No queda una asociación independiente significativa",
    }
)

pruebas_df = pd.DataFrame(pruebas)
pruebas_df.to_csv(OUTPUT / "resultados_pruebas.csv", index=False, encoding="utf-8-sig")

# KPIs globales para verificar las tarjetas del dashboard.
poblacion_total = resumen["poblacion"].sum()
con_vacunacion = resumen.dropna(subset=["pct_vacunacion_completa"])
cobertura_ponderada = np.average(
    con_vacunacion["pct_vacunacion_completa"],
    weights=con_vacunacion["poblacion"],
)
ultimo_mes = fact["anio_mes"].max()
mensual = fact.loc[fact["anio_mes"] == ultimo_mes]
poblacion_mes = dim_pais.loc[
    dim_pais["iso_code"].isin(mensual["iso_code"]), "poblacion"
].sum()
kpis = pd.DataFrame(
    [
        {
            "kpi": "Mortalidad acumulada por millón",
            "valor": resumen["muertes_acumuladas"].sum() / poblacion_total * 1_000_000,
            "unidad": "muertes por millón",
            "corte": ultimo_mes,
        },
        {
            "kpi": "Cobertura de vacunación completa",
            "valor": cobertura_ponderada,
            "unidad": "% ponderado por población",
            "corte": ultimo_mes,
        },
        {
            "kpi": "Brecha frente a 70%",
            "valor": max(0, 70 - cobertura_ponderada),
            "unidad": "puntos porcentuales",
            "corte": ultimo_mes,
        },
        {
            "kpi": "Mortalidad mensual por millón",
            "valor": mensual["muertes_nuevas"].sum() / poblacion_mes * 1_000_000,
            "unidad": "muertes por millón",
            "corte": ultimo_mes + " (parcial)",
        },
        {
            "kpi": "Incidencia mensual por 100.000",
            "valor": mensual["casos_nuevos"].sum() / poblacion_mes * 100_000,
            "unidad": "casos por 100.000",
            "corte": ultimo_mes + " (parcial)",
        },
        {
            "kpi": "Letalidad acumulada",
            "valor": resumen["muertes_acumuladas"].sum()
            / resumen["casos_acumulados"].sum()
            * 100,
            "unidad": "%",
            "corte": ultimo_mes,
        },
    ]
)
kpis.to_csv(OUTPUT / "resumen_kpis.csv", index=False, encoding="utf-8-sig")

# Tablas de soporte para las cifras narradas en el informe.
resumen_anual = (
    fact.assign(anio=fact["anio_mes"].str[:4])
    .groupby("anio", as_index=False)
    .agg(casos_nuevos=("casos_nuevos", "sum"), muertes_nuevas=("muertes_nuevas", "sum"))
)
resumen_anual.to_csv(
    OUTPUT / "resumen_anual.csv", index=False, encoding="utf-8-sig"
)

resumen_continente = (
    resumen.groupby("continente", as_index=False)
    .agg(
        poblacion=("poblacion", "sum"),
        casos_acumulados=("casos_acumulados", "sum"),
        muertes_acumuladas=("muertes_acumuladas", "sum"),
    )
)
resumen_continente["casos_por_millon"] = (
    resumen_continente["casos_acumulados"] / resumen_continente["poblacion"] * 1_000_000
)
resumen_continente["muertes_por_millon"] = (
    resumen_continente["muertes_acumuladas"] / resumen_continente["poblacion"] * 1_000_000
)
resumen_continente["letalidad_pct"] = (
    resumen_continente["muertes_acumuladas"]
    / resumen_continente["casos_acumulados"]
    * 100
)
resumen_continente.to_csv(
    OUTPUT / "resumen_continente.csv", index=False, encoding="utf-8-sig"
)

grupos_vacunacion = h2.assign(
    grupo=np.where(
        h2["pct_vacunacion_completa"] >= mediana_cobertura,
        "Alta (>= mediana)",
        "Baja (< mediana)",
    )
)
resumen_grupos = (
    grupos_vacunacion.groupby("grupo", as_index=False)
    .agg(
        n=("muertes_por_millon", "size"),
        media_muertes_por_millon=("muertes_por_millon", "mean"),
        mediana_muertes_por_millon=("muertes_por_millon", "median"),
    )
)
resumen_grupos.to_csv(
    OUTPUT / "resumen_grupos_vacunacion.csv", index=False, encoding="utf-8-sig"
)

top_mortalidad = resumen.nlargest(10, "muertes_por_millon")[
    ["iso_code", "pais", "continente", "muertes_por_millon", "nivel_vacunacion"]
]
top_mortalidad.to_csv(
    OUTPUT / "top_10_mortalidad.csv", index=False, encoding="utf-8-sig"
)

print("Pruebas estadísticas")
print(pruebas_df.to_string(index=False))
print("\nKPIs")
print(kpis.to_string(index=False))
print(f"\nSe escribieron 6 archivos de resultados en: {OUTPUT}")
