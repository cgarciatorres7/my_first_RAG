import streamlit as st
from src.embedding import process_video

st.header("Here's project :blue[Oppenheimer]: A YouTube Search tool with NLP. :sunglasses:")

st.write("How to use: Select a youtube video, then ask any question about the video")


user_input = st.text_input("Enter the Youtube URL that you want to analyze", key="name")

if st.button("Process video"):
    # Call the greet_user function with the user input
    if user_input:
        process_video(user_input)
        st.success("Corrcto")  # Display the greeting
    else:
        st.error("Please enter a youtube video")