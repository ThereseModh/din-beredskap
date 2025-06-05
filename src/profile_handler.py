import json
from pathlib import Path

PROFILE_PATH = Path("data/profile.json")


def create_or_update_profile():
    if PROFILE_PATH.exists():
        with PROFILE_PATH.open("r", encoding="utf-8") as f:
            profile = json.load(f)
        print("\nEn tidigare profil hittades:")
        for key, value in profile.items():
            print(f"- {key.capitalize()}: {value}")
        update = input("\nVill du uppdatera profilen? (j/n): ").strip().lower()
        if update != "j":
            return profile

    print("\nSkapa din personliga beredskapsprofil:")

    try:
        household_size = int(input("Hur många personer finns i hushållet? ").strip())
        housing_type = input("Bor du i hus eller lägenhet? ").strip().lower()
        has_pets = input("Har du husdjur? (j/n): ").strip().lower() == "j"
        electricity_dependent = (
            input(
                "Är någon i hushållet elberoende (t.ex. medicinsk utrustning)? (j/n): "
            )
            .strip()
            .lower()
            == "j"
        )
        location = input("Ange din ort (frivilligt): ").strip()

        profile = {
            "household_size": household_size,
            "housing_type": housing_type,
            "has_pets": has_pets,
            "electricity_dependent": electricity_dependent,
            "location": location,
        }

        PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with PROFILE_PATH.open("w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

        print("\nProfilen har sparats!")
        return profile

    except Exception as e:
        print(f"Ett fel uppstod: {e}")
        return {}


def load_profile():
    if PROFILE_PATH.exists():
        with PROFILE_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}
