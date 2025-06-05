import pandas as pd


def load_shelters(filepath="data/skyddsrum.csv"):
    """
    Läser in skyddsrumsdata från en CSV-fil och returnerar som en DataFrame.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Kunde inte läsa skyddsrumsfilen: {e}")
        return pd.DataFrame()


def search_shelters_by_city(df, city_name):
    """
    Söker efter skyddsrum i en viss ort och returnerar en sträng med formaterad information.
    Om skyddsrummet inte är verifierat av MSB visas en varning.
    """
    result = df[df["ort"].str.lower() == city_name.lower()]
    if result.empty:
        return f"Inga skyddsrum hittades i {city_name}."
    else:
        output = []
        for _, row in result.iterrows():
            info = (
                f"Namn: {row['namn']}\n"
                f"Adress: {row['adress']}, {row['ort']}\n"
                f"Kapacitet: {row['kapacitet']} personer\n"
                f"Yta: {row['yta_kvm']} kvm\n"
                f"Status: {row['status']}\n"
                f"Tillträde: {row['tillträde']}"
            )
            if not row["verifierad", True]:
                info += "\nOBS! Detta skyddsrum är ej verifierat av MSB."
            output.append(info)
        return "\n\n".join(output)


def add_custom_shelter(df, filepath="data/skyddsrum.csv"):
    """
    Låter användaren lägga till ett eget skyddsrum som sparas till fil och DataFrame.
    Det nya skyddsrummet markeras som ej verifierat (verifierad = False).
    """
    print("\nLägg till ett eget skyddsrum (ej verifierat av MSB)")
    try:
        name = input("Namn på skyddsrummet: ").strip()
        address = input("Adress: ").strip()
        city = input("Ort: ").strip()
        lat = float(input("Latitud (ex 57.71): ").strip())
        lon = float(input("Longitud (ex 11.97): ").strip())
        capacity = int(input("Kapacitet (antal personer): ").strip())
        area = int(input("Yta i kvm: ").strip())
        access = input("Tillträde (Allmänt/Privat): ").strip()

        new_id = df["id"].max() + 1 if not df.empty else 1

        new_shelter = {
            "id": new_id,
            "namn": name,
            "adress": address,
            "ort": city,
            "lat": lat,
            "long": lon,
            "kapacitet": capacity,
            "yta_kvm": area,
            "status": "Föreslaget",
            "tillträde": access,
            "verifierad": False,
        }

        df = pd.concat([df, pd.DataFrame([new_shelter])], ignore_index=True)
        df.to_csv(filepath, index=False)
        print("\nSkyddsrummet har lagts till!")
        return df

    except Exception as e:
        print(f"Ett fel uppstod: {e}")
        return df
