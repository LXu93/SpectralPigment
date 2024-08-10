import streamlit as st

def intr_page():
    st.title("home")
    if st.button("Get Start"):
        st.switch_page("main_page.py")
        
pg = st.navigation([
    st.Page(intr_page, title="Introduce of our project"),
    st.Page("main_page.py", title="Click here to start"),
])
pg.run()