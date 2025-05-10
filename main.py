from src.embedding import process_video
from src.retriever import query_pinecone, rag_promt, chat_completion

def main():
    #process_video("https://www.youtube.com/watch?v=IELMSD2kdmk")
    answer = query_pinecone("Who is Matei Zaharia?")
    promt = rag_promt("Who is Matei Zaharia?", answer)
    response = chat_completion(promt)

if __name__ == "__main__":
    main()
    