import pandas as pd


def load_skyddsrum_data(filepath="data/skyddsrum.csv"):
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Kunde inte läsa skyddsrumsfilen: {e}")
        return pd.DataFrame()


def sök_skyddsrum_efter_ort(df, ort_namn):
    resultat = df[df["ort"].str.lower() == ort_namn.lower()]
    if resultat.empty:
        return f"Inga skyddsrum hittades i {ort_namn}."
    else:
        return resultat
