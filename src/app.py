from retriever import retrieve_context
from generator import generate_answer


def main():
    print("Välkommen till Din Beredskap – AI-assistent för krisberedskap!\n")

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
