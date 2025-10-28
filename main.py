from src.embedding import process_video
from src.retriever import query_pinecone
from src.generation import complete_rag

def main():
    video_url = input("Enter a YouTube video URL: ")
    if video_url:
        process_video(video_url)
        question = input("Enter a question: ")
        if question:
            answer = query_pinecone(question)
            response = complete_rag(query=question, query_results=answer)
            print(response)
        else:
            print("No question provided")
    else:
        print("No video URL provided")

if __name__ == "__main__":
    main()