import streamlit as st
import requests

endpoint = "http://localhost:8000/n11/api/predict"

def app():
    st.title("N11 Product Categorization Service")

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
            
            st.write(payload)

            response = requests.post(endpoint, json=payload)

            st.write(response.status_code)
            st.write(response.json())


    
    
    

if __name__ == '__main__':
    app()