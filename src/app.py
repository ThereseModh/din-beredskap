from retriever import retrieve_context
from generator import generate_answer
from shelters import load_shelters, search_shelters_by_city, add_custom_shelter
from profile_handler import create_or_update_profile, load_profile


def main():
    try:
        print("Välkommen till Din Beredskap – AI-assistent för krisberedskap!\n")

        profile = load_profile()
        shelter_df = load_shelters()

        while True:
            print("\nVad vill du göra?")
            print("1. Ställ en beredskapsfråga till AI:n")
            print("2. Sök skyddsrum på ort")
            print("3. Lägg till eget skyddsrum")
            print("4. Skapa eller uppdatera beredskapsprofil")
            print("5. Avsluta")

            choice = input("Välj (1/2/3/4/5): ").strip()

            if choice == "1":
                question = input("Din fråga: ")

                if profile:
                    profile_context = (
                        "Användarens beredskapsprofil:\n"
                        f"- Hushåll: {profile.get('household_size')}\n"
                        f"- Boendeform: {profile.get('housing_type')}\n"
                        f"- Husdjur: {profile.get('has_pets')}\n"
                        f"- Elberoende: {profile.get('electricity_dependent')}\n"
                        f"- Ort: {profile.get('location')}\n\n"
                    )
                else:
                    profile_context = ""

                context = retrieve_context(question)
                full_context = profile_context + context
                answer = generate_answer(question, full_context)
                print("\nAI:s svar:\n", answer)

            elif choice == "2":
                location = input("Ange ort: ")
                result = search_shelters_by_city(shelter_df, location)
                print("\nSökresultat:\n", result)

            elif choice == "3":
                shelter_df = add_custom_shelter(shelter_df)

            elif choice == "4":
                profile = create_or_update_profile()

            elif choice == "5":
                print("Avslutar.")
                break

            else:
                print("Ogiltigt val. Försök igen.")

    except KeyboardInterrupt:
        print("\nProgrammet avslutades med Ctrl+C.")


if __name__ == "__main__":
    main()
