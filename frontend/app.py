import streamlit as st
from pages import comp0, comp1, comp3


st.sidebar.title("Provided Services")
selection = st.sidebar.selectbox("Select one of the services.", 
["--", "Explarotary Data Analysis",  "Category Suggestions", "Error Analysis"])

pages = {"--": comp0,
         "Explarotary Data Analysis": comp1,
         "Category Suggestions": comp3}


pages.get(selection, lambda: None)()
