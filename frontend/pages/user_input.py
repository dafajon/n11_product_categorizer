import streamlit as st
import requests
import pandas as pd
import numpy as np

endpoint = "http://192.168.88.88:8000/n11/api/predict"

def app():
    st.title("N11 Product Category Suggestion Service")

    n_prod = st.text_input("Please input number of products.", "1")
    if n_prod is not None:
        n_prod = int(n_prod)

        form = st.form(key='my_form')
        inputs = []
        for i in range(n_prod):
            title_input = form.text_input(label=f'Please input product {i+1} title.')
            product_input = form.text_input(label=f'Please input product {i+1} description.')
            inputs.append((title_input, product_input))
        
        submit_button = form.form_submit_button(label='Submit')

        if submit_button:
            payload_content = [{"DESCRIPTION": inp[1], "TITLE": inp[0]} for inp in inputs]
            payload = {"content": payload_content, "datapath": "string"}
            
            with st.spinner("Predicting..."):
                response = requests.post(endpoint, json=payload)

            predicted_category = response.json()["preds"]
            probs = response.json()["top3prob"]
            top3_category = response.json()["top3"]

            st.success(f'Prediction Complete')

            st.header("PREDICTED CATEGORIES")
            st.subheader("Do they suit your product?")
            images = pd.read_csv('data/category_image.csv')
            for i, prod in enumerate(top3_category):
                st.header(f"Product {i+1}")
                for j, cat in enumerate(prod):
                    conf = probs[i][j]
                    if conf > 0.05:
                        st.text(f"Suggested Category: {cat}, Confidence: {conf}")
                        cols = st.columns(5)
                        prev_imgs = []
                        for col in cols:
                            imagelink = np.random.choice(images.loc[images.CATEGORY_ID == cat, 'image_links'])
                            while imagelink in prev_imgs:
                                imagelink = np.random.choice(images.loc[images.CATEGORY_ID == cat, 'image_links'])
                            prev_imgs.append(imagelink)
                            with col:
                                st.image(imagelink)



if __name__ == '__main__':
    app()
