import streamlit as st

st.set_page_config(page_title="Test Nav", layout="wide")

def page1():
    st.write("# Page 1")
    st.write("This is page 1")

def page2():
    st.write("# Page 2") 
    st.write("This is page 2")

pages = [
    st.Page(page1, title="Page 1"),
    st.Page(page2, title="Page 2"),
]

pg = st.navigation(pages, position="top")
pg.run()