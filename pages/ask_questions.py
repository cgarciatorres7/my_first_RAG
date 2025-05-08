import streamlit as st
from src.retriever import query_pinecone, get_transcriptions
from src.embedding import process_video


main_header_message = None
main_text_message = None

if st.session_state.video_title:
    main_header_message = st.session_state.video_title
    main_text_message = "You can now ask questions about the video"
    
else:
    main_text_message = "Youtube video title Loading"
    main_text_message = "Please go back and enter a YouTube URL in the search page first"
    
main_header = st.header(main_header_message)
main_text = st.write(main_text_message)

ask_question_input = st.text_input("Ask a question about the video", key="name2")
if st.button("Ask a question"):
    if ask_question_input != "":
        with st.spinner("Searching for answer..."):
            xc = query_pinecone(ask_question_input)
            transcriptions = get_transcriptions(xc)
            st.write(transcriptions)
    else:
        st.write("Please enter a question")


