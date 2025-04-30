import streamlit as st
from src.embedding import download_audio


st.header("Here's project :blue[Oppenheimer]: A YouTube Search tool with NLP. :sunglasses:")

st.write("How to use: Select a youtube video, then ask any question about the video")

# Input for YouTube URL
youtube_url = st.text_input("Enter YouTube video URL")

if youtube_url:
    try:
        # Get video info and store in session state
        video_info = download_audio(youtube_url)
        st.session_state.video_title = video_info["video_name"]
        st.session_state.video_url = youtube_url
        # Redirect to ask_questions page
        st.switch_page("pages/ask_questions.py")
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")