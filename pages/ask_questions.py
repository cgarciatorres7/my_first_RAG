import streamlit as st
from src.retriever import get_rag_response, query_pinecone, get_transcriptions


st.header("Youtube video title")

if "video_title" in st.session_state:
    st.header(st.session_state.video_title)
    st.text_input("Ask a question about the video", key="name2")
    
    if st.button("Ask a question"):
        xc = query_pinecone(st.session_state.question)
        transcriptions = get_transcriptions(xc)
        st.write(transcriptions)
        
        
else:
    st.warning("Please enter a YouTube URL in the search page first")
    

