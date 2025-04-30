import streamlit as st



st.header("Youtube video title")

if "video_title" in st.session_state:
    st.header(st.session_state.video_title)
    st.text_input("Ask a question about the video", key="name2")
else:
    st.warning("Please enter a YouTube URL in the search page first")
    

