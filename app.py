import streamlit as st


ask = st.Page("./pages/ask_questions.py", title="Select yt video", icon=":material/videocam:")
search = st.Page("./pages/search_video.py", title="Ask questions", icon=":material/school:")

pg = st.navigation([ask, search])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()