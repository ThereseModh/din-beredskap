from retriever import retrieve_context
from generator import generate_answer

if __name__ == "__main__":
    question = input("Ställ en beredskapsfråga: ")
    context = retrieve_context(question)
    answer = generate_answer(question, context)
    print("\nAI:s svar\n", answer)
