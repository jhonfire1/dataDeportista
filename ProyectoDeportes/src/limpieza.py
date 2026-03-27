import pandas as pd

DEPORTES_VALIDOS = {
    # Natación
    "natacion": "Natación",
    "natació": "Natación",
    "Natacion": "Natación",
    "Natació": "Natación",
    "NATACIÓN": "Natación",
    "natación": "Natación",
    "Natación": "Natación",
    
    # Tenis
    "tenis": "Tenis",
    "Tenis": "Tenis",
    "TENIS": "Tenis",
    "tennis": "Tenis",
    "Tennis": "Tenis",
    
    # Rugby
    "Rugby": "Rugby",
    "RUGBY": "Rugby",
    "rugby": "Rugby",
    
    # Ciclismo
    "ciclismo": "Ciclismo",
    "Ciclismo": "Ciclismo",
    "CICLISMO": "Ciclismo",
    
    # Voleibol
    "VOLEIBOL": "Voleibol",
    "Voleibol": "Voleibol",
    "voleibol": "Voleibol",
    "Volleyball": "Voleibol",
    "volleyball": "Voleibol",
    
    # Fútbol
    "FÚTBOL": "Fútbol",
    "fútbol": "Fútbol",
    "futbol": "Fútbol",
    "FUTBOL": "Fútbol",
    "Fútbol": "Fútbol",
    "Futbol": "Fútbol",
    
    # Atletismo
    "Atletismo": "Atletismo",
    "ATLETISMO": "Atletismo",
    "atletismo": "Atletismo",
    
    # Baloncesto
    "Baloncesto": "Baloncesto",
    "baloncesto": "Baloncesto",
    "BALONCESTO": "Baloncesto",
    "Basketball": "Baloncesto",
    "basketball": "Baloncesto",
    
    # Boxeo
    "Boxeo": "Boxeo",
    "BOXEO": "Boxeo",
    "boxeo": "Boxeo"
}


PESO_MIN = 55
PESO_MAX = 110

ENTRENAMIENTO_MIN = 1
ENTRENAMIENTO_MAX = 25

def limpiar_deportistas(df: pd.DataFrame) -> pd.DataFrame:
    
    # normalizar nombres de columnas
    df = df.copy()
    df.columns = df.columns.str.lower().str.strip()

    # validar columnas requeridas
    requeridas = {
    "nombre", "deporte", "edad", "peso_kg", "altura_cm",
    "frecuencia_cardiaca_bpm", "horas_entrenamiento_semana",
    "rendimiento_score", "posicion"}
    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise ValueError(f"Columnas faltantes: {faltantes}")
    
    # limpiar espacios en valores de texto
    for col in ["nombre", "deporte","posicion"]:
        df[col] = df[col].str.strip()

    df["deporte"] = (
        df["deporte"]
        .str.lower()
        .str.strip()
        .map(DEPORTES_VALIDOS)
    )

    # convertir peso_kg : reemplazar coma decimal y convertir a float
    for col in ["peso_kg"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .pipe(pd.to_numeric, errors="coerce")
        )
    
    df["edad"] = pd.to_numeric(df["edad"], errors="coerce")
    df["edad"] = df["edad"].fillna(df["edad"].mean())

    # eliminar duplicados antes de calcular estadísticas
    df = df.drop_duplicates()


    # eliminar outliers con IQR (acotado al rango válido)
    q1 = df["peso_kg"].quantile(0.25)
    q3 = df["peso_kg"].quantile(0.75)
    iqr = q3 - q1
    li = max(q1 - 1.5 * iqr, PESO_MIN)
    ls = min(q3 + 1.5 * iqr, PESO_MAX)
    df = df[(df["peso_kg"] >= li) & (df["peso_kg"] <= ls)]


    q1 = df["horas_entrenamiento_semana"].quantile(0.25)
    q3 = df["horas_entrenamiento_semana"].quantile(0.75)
    iqr = q3 - q1
    li = max(q1 - 1.5 * iqr, ENTRENAMIENTO_MIN)
    ls = min(q3 + 1.5 * iqr, ENTRENAMIENTO_MAX)
    df = df[(df["horas_entrenamiento_semana"] >= li) & (df["horas_entrenamiento_semana"] <= ls)]

    # descartar peso fuera de rango válido antes de calcular promedio
    for col in ["peso_kg",]:
        df[col] = df[col].where(df[col].between(PESO_MIN, PESO_MAX))

    # calcular promedio
    promedio_peso = df["peso_kg"].mean()
    #imputar y rellenar valores vacios con el promedio
    df["peso_kg"] = df["peso_kg"].fillna(promedio_peso)

    # rendimiento a numerico
    df['rendimiento_score'] = pd.to_numeric(df['rendimiento_score'], errors='coerce')
    
    # Eliminar filas donde el score sea nulo, porque no sirven para el análisis de rendimiento
    df = df.dropna(subset=['rendimiento_score'])

    return df