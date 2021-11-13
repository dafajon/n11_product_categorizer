import streamlit as st
import pandas as pd


@st.cache
def data(uploaded_file: None):
    if uploaded_file is not None:
        data = pd.read_csv('data/train_n11.csv', sep='|')
        data = data[~data.CATEGORY_ID.isna()]
        data.CATEGORY_ID = data.CATEGORY_ID.astype(int)
        return data, data['CATEGORY_ID'].value_counts()
    else:
        return None, None

def app():
    uploaded_file = st.file_uploader("Choose a .csv file")
    _, _  = data(uploaded_file)

if __name__ == '__main__':
    app()