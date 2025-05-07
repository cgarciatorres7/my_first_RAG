import streamlit as st
from src.retriever import query_pinecone, get_transcriptions
from src.embedding import process_video

st.header("Youtube video title Loading")
st.write("Please go back and enter a YouTube URL in the search page first")

if st.button("Ask a question"):
    
    #rsponse = process_video(st.session_state.video_url)
    try:
        print("Hello")
        if st.session_state.video_title:
            st.header(st.session_state.video_title)
            st.text_input("Ask a question about the video", key="name2")
            if st.button("Ask a question"):
                xc = query_pinecone(st.session_state.question)
                transcriptions = get_transcriptions(xc)
                st.write(transcriptions)
        
    except KeyError as e:
        st.warning("Please enter a YouTube URL in the search page first")


