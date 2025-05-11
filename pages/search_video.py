import streamlit as st
from pytubefix import YouTube
from pytubefix.exceptions import RegexMatchError
from src.embedding import process_video  # Add this import since you'll need it

def get_video_title(url: str) -> str:
    """
    Get the title of a YouTube video from its URL.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Title of the video
        
    Raises:
        Exception: If video cannot be accessed or URL is invalid
    """
    try:
        yt = YouTube(url)
        return yt.title
    except RegexMatchError:
        print(RegexMatchError)
        return None
    

st.header("Here's project :blue[Oppenheimer]: A YouTube Search tool with NLP. :sunglasses:")
st.write("How to use: Select a youtube video, then ask any question about the video")
youtube_url = st.text_input("Enter YouTube video URL")

ASK_QUESTIONS_BUTTON_DISABLED = True

# Input for YouTube URL
if youtube_url != "":
    video_title = get_video_title(youtube_url)
    print(video_title)
    if video_title:
        st.session_state.video_title = video_title
        st.session_state.video_url = youtube_url
        ASK_QUESTIONS_BUTTON_DISABLED = False
    else:
        st.error("Could not get video title: Please enter a valid YouTube URL")
        
    
if st.session_state.show_ask_page and youtube_url:
    st.switch_page("pages/ask_questions.py")

process_video_button = st.button("Process Video", disabled=ASK_QUESTIONS_BUTTON_DISABLED)

if process_video_button:
    with st.spinner("Processing video..."):
        #process_video(youtube_url)
        print("Finished")
    
    st.session_state.show_ask_page = True
    st.success("Video processed! You can now go to the Ask Questions page.")
        # Redirect to ask_questions page
    st.rerun()

