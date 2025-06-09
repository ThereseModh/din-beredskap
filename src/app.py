from retriever import retrieve_context
from generator import generate_answer
from profile_handler import (
    create_or_update_profile,
    print_profile,
    get_current_profile,
)


# Återanvändbar formattering av profilen
def format_profile(profile: dict) -> str:
    if not profile:
        return ""
    return (
        f"Användarens beredskapsprofil:\n"
        f"- Hushåll: {profile.get('household_size')} personer\n"
        f"- Varav barn: {profile.get('num_children')} st\n"
        f"- Boendeform: {profile.get('housing_type')}\n"
        f"- Plats: {profile.get('area_type')}\n"
        f"- Har bil: {'Ja' if profile.get('has_car') else 'Nej'}\n"
        f"- Husdjur: {'Ja' if profile.get('has_pets') else 'Nej'}\n"
        f"- Egen brunn: {'Ja' if profile.get('has_private_well') else 'Nej'}\n"
        f"- Vedeldning: {'Ja' if profile.get('has_wood_heating') else 'Nej'}\n"
        f"- Elberoende: {'Ja' if profile.get('electricity_dependent') else 'Nej'}\n"
        f"- Ort: {profile.get('location') or 'Ej angiven'}\n\n"
    )


# Hantera fritt ställd fråga
def handle_own_question(profile):
    question = input("\nVad vill du fråga AI:n? ").strip()
    if not question:
        print("Ingen fråga angavs.")
        return

    profile_context = format_profile(profile)
    context = retrieve_context(question)
    full_context = profile_context + context
    answer = generate_answer(question, full_context)

    print("\nAI:s svar:\n")
    print(answer)


def scenarios(scenario: str, profile: dict):
    profile_context = get_current_profile(profile) if profile else ""
    context = retrieve_context(scenario)
    full_context = profile_context + context
    answer = generate_answer(scenario, full_context)
    print("\nAI:s svar:\n")
    print(answer)


def handle_scenarios(profile):
    scenario_prompts = {
        "1": ("Strömavbrott", "Hur förbereder jag mig för ett längre strömavbrott?"),
        "2": ("Översvämning", "Vad bör jag tänka på vid översvämning?"),
        "3": ("Brand", "Hur förbereder jag mig för en brand i hemmet?"),
        "4": ("Matbrist", "Hur kan jag förbereda mig för brist på mat?"),
        "5": ("Vattenbrist", "Vad gör jag om dricksvattnet slutar fungera?"),
        "6": ("Krigshot", "Vad behöver jag vid krigshot eller allvarlig samhällskris?"),
        "7": ("Extrem kyla", "Hur håller jag mig varm utan el under vintern?"),
        "8": ("Evakuering", "Vad bör jag packa om jag måste evakuera?"),
    }

    while True:
        print("\nKrisscenarier – hur du hanterar dem")
        for key, (label, _) in scenario_prompts.items():
            print(f"{key}. {label}")
        print("0. Tillbaka till huvudmenyn")

        val = input("\nVälj ett scenario: ").strip()

        if val == "0":
            break

        if val in scenario_prompts:
            _, prompt = scenario_prompts[val]
            profile_context = format_profile(profile)
            context = retrieve_context(prompt)
            full_context = profile_context + context
            answer = generate_answer(prompt, full_context)

            print("\nAI:s svar:\n")
            print(answer)
        else:
            print("Ogiltigt val. Försök igen.")


def main():
    try:
        print(
            "Välkommen till Din Beredskap – AI-assistent för hemberedskap och krishantering!\n"
        )

        while True:
            print("\nVad vill du göra?")
            print("1. Ställ en egen fråga till AI:n")
            print("2. Utforska krisscenarier")
            print("3. Skapa eller uppdatera beredskapsprofil")
            print("4. Visa profil")
            print("5. Avsluta")

            choice = input("Välj (1/2/3/4/5): ").strip()
            profile = get_current_profile()

            if choice == "1":
                handle_own_question(profile)

            elif choice == "2":
                handle_scenarios(profile)

            elif choice == "3":
                create_or_update_profile()

            elif choice == "4":
                print_profile(profile)

            elif choice == "5":
                print("Avslutar.")
                break

            else:
                print("Ogiltigt val. Försök igen.")

    except KeyboardInterrupt:
        print("\nProgrammet avslutades med Ctrl+C.")


if __name__ == "__main__":
    main()
