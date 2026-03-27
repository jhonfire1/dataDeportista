import pandas as pd

def Resumen_datos(df):
    resumen = {
        "Total Deportistas": len(df),
        "Promedio rendimiento": round(df["rendimiento_score"].mean(), 2),
        "Promedio edad": round(df["edad"].mean(), 2),

    }
    return pd.Series(resumen)


#método que retorna el promedio por carrera
def Promedio_por_deporte(df):
    return (
        df.groupby("deporte")["rendimiento_score"]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={"rendimiento_score": "promedio"})
        .sort_values("promedio", ascending=False)
    )

def Deportistas_destacados(df):
    return df[df["rendimiento_score"] > 7.0].sort_values("rendimiento_score", ascending=False)