import streamlit as st
from src.retriever import query_pinecone, rag_promt
from src.embedding import process_video


if st.session_state.video_url:
    main_header_message = st.session_state.video_title
    main_text_message = "You can now ask questions about the video"


else:
    main_header_message = "Youtube video title Loading"
    main_text_message = "Please go back and enter a YouTube URL in the search page first"
    
main_header = st.header(main_header_message)
main_text = st.write(main_text_message)

ask_question_input = st.text_input("Ask a question about the video", key="name2")
if st.button("Ask a question"):
    if ask_question_input != "":
        with st.spinner("Searching for answer..."):
            if 'processed_video' not in st.session_state:
                url = process_video(st.session_state.video_url)
                st.session_state.processed_video = True
            else:
                print("Video already processed")
            answer = query_pinecone(ask_question_input)
            promt = rag_promt(ask_question_input, answer)
            #response = chat_completion(promt)
            st.write(answer.matches[0].metadata['text'])
            st.write("--------------------------------")
            st.write("You can find the part of the video here:")
            st.write(answer.matches[0].metadata['url'])
            st.write("--------------------------------")
            st.write(promt)

    else:
        st.write("Please enter a question")


