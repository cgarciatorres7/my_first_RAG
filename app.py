import streamlit as st


ask = st.Page("./pages/ask_questions.py", title="Ask questions", icon=":material/videocam:")
search = st.Page("./pages/search_video.py", title="Select yt video", icon=":material/school:")

pg = st.navigation([search, ask])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()