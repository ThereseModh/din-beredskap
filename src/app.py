from retriever import retrieve_context
from generator import generate_answer
from skyddsrum import sök_skyddsrum_efter_ort, load_skyddsrum_data


def main():
    print("Välkommen till Din Beredskap – AI-assistent för krisberedskap!\n")

    skyddsrum_df = load_skyddsrum_data()

    while True:
        print("\nVad vill du göra?")
        print("1. Ställ en beredskapsfråga till AI:n")
        print("2. Sök skyddsrum på ort")
        print("3. Avsluta")

        val = input("Välj (1/2/3): ").strip()

        if val == "1":
            fråga = input("Din fråga: ")
            context = retrieve_context(fråga)
            svar = generate_answer(fråga, context)
            print("\nAI:s svar:\n", svar)
        elif val == "2":
            ort = input("Ange ort: ")
            resultat = sök_skyddsrum_efter_ort(skyddsrum_df, ort)
            print(resultat)
        elif val == "3":
            print("Avslutar.")
            break
        else:
            print("Ogiltigt val.")

    try:
        question = input("Ställ en beredskapsfråga: ").strip()

        if not question:
            print("Du måste skriva en fråga.")
            return

        print("\nSöker efter relevant information...")
        context = retrieve_context(question)

        print("\nGenererar AI-svar...")
        answer = generate_answer(question, context)

        print("\nAI:s svar:\n")
        print(answer)

    except KeyboardInterrupt:
        print("\nAvslutar.")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")


if __name__ == "__main__":
    main()
