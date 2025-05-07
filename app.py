import streamlit as st

# Initialize session state if it doesn't exist
if 'show_ask_page' not in st.session_state:
    st.session_state.show_ask_page = False

search = st.Page("./pages/search_video.py", title="Select yt video", icon=":material/school:")

# Only include the ask page in navigation if show_ask_page is True
pages = [search]
if st.session_state.show_ask_page:
    ask = st.Page("./pages/ask_questions.py", title="Ask questions", icon=":material/videocam:")
    pages.append(ask)

pg = st.navigation(pages)
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()