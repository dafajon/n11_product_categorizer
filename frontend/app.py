import streamlit as st
from pages import comp0, comp1, comp2, comp3, comp4


st.sidebar.title("Provided Services")
selection = st.sidebar.selectbox("Select one of the services.", 
["--", "Explarotary Data Analysis",  "Category Suggestions", "Error Analysis"])

pages = {"--": comp0,
         "Explarotary Data Analysis": comp1,
         #"Train New Model": comp2,
         "Category Suggestions": comp3,
         "Error Analysis": comp4}


pages.get(selection, lambda: None)()
