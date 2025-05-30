from retriever import retrieve_context
from generator import generate_answer
from chunker import load_and_chunk_documents

if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    question = input("Ställ en beredskapsfråga: ")
    context = retrieve_context(question, chunks)
    answer = generate_answer(question, context)
    print("\nAI:s svar\n", answer)
