from retriever import retrieve_context
from generator import generate_answer
from shelters import load_shelters, search_shelters_by_city, add_custom_shelter
from profile_handler import (
    create_or_update_profile,
    print_profile,
    get_current_profile,
)


def main():
    try:
        print("Välkommen till Din Beredskap – AI-assistent för krisberedskap!\n")

        shelter_df = load_shelters()

        while True:
            print("\nVad vill du göra?")
            print("1. Ställ en beredskapsfråga till AI:n")
            print("2. Sök skyddsrum på ort")
            print("3. Lägg till eget skyddsrum")
            print("4. Skapa eller uppdatera beredskapsprofil")
            print("5. Visa profil")
            print("6. Avsluta")

            choice = input("Välj (1/2/3/4/5/6): ").strip()

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
                location = input("Ange ort: ")
                result = search_shelters_by_city(shelter_df, location)
                print("\nSökresultat:\n")
                print(result)

            elif choice == "3":
                shelter_df = add_custom_shelter(shelter_df)

            elif choice == "4":
                create_or_update_profile()

            elif choice == "5":
                profile = get_current_profile()
                print_profile(profile)

            elif choice == "6":
                print("Avslutar.")
                break

            else:
                print("Ogiltigt val. Försök igen.")

    except KeyboardInterrupt:
        print("\nProgrammet avslutades med Ctrl+C.")


if __name__ == "__main__":
    main()
