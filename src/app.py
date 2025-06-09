from retriever import retrieve_context
from generator import generate_answer
from profile_handler import (
    create_or_update_profile,
    print_profile,
    get_current_profile,
)


def main():
    try:
        print(
            "Välkommen till Din Beredskap – AI-assistent för hemberedskap och krishantering!\n"
        )

        while True:
            print("\nVad vill du göra?")
            print("1. Ställ en beredskapsfråga till AI:n")
            print("2. Skapa eller uppdatera beredskapsprofil")
            print("3. Visa profil")
            print("4. Avsluta")

            choice = input("Välj (1/2/3/4): ").strip()

            if choice == "1":
                profile = get_current_profile()
                question = input("\nDin fråga: ")

                if profile:
                    profile_context = (
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

                else:
                    profile_context = ""

                context = retrieve_context(question)
                full_context = profile_context + context
                answer = generate_answer(question, full_context)

                print("\nAI:s svar:\n")
                print(answer)

            elif choice == "2":
                create_or_update_profile()

            elif choice == "3":
                profile = get_current_profile()
                print_profile(profile)

            elif choice == "4":
                print("Avslutar.")
                break

            else:
                print("Ogiltigt val. Försök igen.")

    except KeyboardInterrupt:
        print("\nProgrammet avslutades med Ctrl+C.")


if __name__ == "__main__":
    main()
