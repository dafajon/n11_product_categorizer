import streamlit as st

def app():

    st.markdown(
    '<h1 style="text-align:center;color:black;font-weight:bolder;font-size:100px;">Doğuş Teknoloji<br>N11 Datathon</h1>',
    unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center;color:white;"><u>AIDEO<u></h2>', unsafe_allow_html=True)

    st.header("""
    Multi-class text classification service with various components: """)

    st.subheader("- Exploratory Data Analysis on input training data. 🧐 ")
    st.subheader("- Product category suggestion over user free-text input. 🧩")

if __name__ == "__main__":
    app()
