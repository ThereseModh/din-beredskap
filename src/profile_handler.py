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
        num_children = int(input("Hur många av dessa är barn? ").strip())
        housing_type = input("Bor du i hus eller lägenhet? ").strip().capitalize()
        area_type = input("Bor du i tätort eller på landsbygd? ").strip().capitalize()
        has_car = input("Har du bil? (j/n): ").strip().lower() == "j"
        has_pets = input("Har du husdjur? (j/n): ").strip().lower() == "j"
        has_private_well = input("Har du egen brunn? (j/n): ").strip().lower() == "j"
        has_wood_heating = (
            input("Har du möjlighet till vedeldning? (j/n): ").strip().lower() == "j"
        )
        electricity_dependent = (
            input("Är någon elberoende (t.ex. medicinsk utrustning)? (j/n): ")
            .strip()
            .lower()
            == "j"
        )
        location = input("Ange din ort (frivilligt): ").strip()

        profile = {
            "household_size": household_size,
            "num_children": num_children,
            "housing_type": housing_type,
            "area_type": area_type,
            "has_car": has_car,
            "has_pets": has_pets,
            "has_private_well": has_private_well,
            "has_wood_heating": has_wood_heating,
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


def get_current_profile():
    return load_profile() or {}


def print_profile(profile: dict):
    if not profile:
        print("\nIngen profil hittades.\n")
        return

    print("\nDin beredskapsprofil:\n")
    print(f"- Hushåll: {profile.get('household_size')} personer")
    print(f"- Varav barn: {profile.get('num_children')} st")
    print(f"- Boendeform: {profile.get('housing_type')}")
    print(f"- Plats: {profile.get('area_type')}")
    print(f"- Har bil: {'Ja' if profile.get('has_car') else 'Nej'}")
    print(f"- Husdjur: {'Ja' if profile.get('has_pets') else 'Nej'}")
    print(f"- Egen brunn: {'Ja' if profile.get('has_private_well') else 'Nej'}")
    print(f"- Vedeldning: {'Ja' if profile.get('has_wood_heating') else 'Nej'}")
    print(f"- Elberoende: {'Ja' if profile.get('electricity_dependent') else 'Nej'}")
    print(f"- Ort: {profile.get('location') or 'Ej angiven'}\n")
