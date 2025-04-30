import streamlit as st
from src.retriever import query_pinecone


st.header("Youtube video title")

if "video_title" in st.session_state:
    st.header(st.session_state.video_title)
    st.text_input("Ask a question about the video", key="name2")
    
    if st.button("Ask a question"):
        xc = query_pinecone(st.session_state.video_url)
        transcriptions = get_transcriptions(xc)
        audio_time = get_audio_time(xc)
        audio_url = get_audio_url(xc)
        st.write(transcriptions)
        st.write(audio_time)
        st.write(audio_url)
        
else:
    st.warning("Please enter a YouTube URL in the search page first")
    

