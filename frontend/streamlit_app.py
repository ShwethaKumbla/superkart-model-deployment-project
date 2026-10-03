import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title='SuperKart Sales Forecaster', layout='centered')
st.title('SuperKart Sales Revenue Forecaster')
st.markdown('Enter product and store details below to predict quarterly sales revenue.')
st.markdown('---')

BACKEND_URL = 'http://backend:7860'

with st.form('prediction_form'):
    st.subheader('Product Details')
    col1, col2 = st.columns(2)
    with col1:
        product_weight = st.number_input('Product Weight (kg)', min_value=0.0,
                                         max_value=30.0, value=12.66, step=0.01)
        product_area = st.number_input('Product Allocated Area', min_value=0.0,
                                       max_value=1.0, value=0.027, step=0.001,
                                       format='%.4f')
        product_id_char = st.selectbox('Product ID Prefix', ['FD', 'NC', 'DR'])
    with col2:
        product_mrp = st.number_input('Product MRP (Rs.)', min_value=0.0,
                                      max_value=500.0, value=117.08, step=0.01)
        product_sugar = st.selectbox('Sugar Content', ['Low Sugar', 'Regular', 'No Sugar'])
        product_type_cat = st.selectbox('Product Category', ['Perishables', 'Non Perishables'])

    st.subheader('Store Details')
    col3, col4 = st.columns(2)
    with col3:
        store_size = st.selectbox('Store Size', ['Small', 'Medium', 'High'])
        city_type = st.selectbox('City Type', ['Tier 1', 'Tier 2', 'Tier 3'])
    with col4:
        store_type = st.selectbox('Store Type',
                                  ['Supermarket Type1', 'Supermarket Type2',
                                   'Departmental Store', 'Food Mart'])
        store_age = st.number_input('Store Age (Years)', min_value=0, max_value=100, value=16)

    submitted = st.form_submit_button('Predict Sales Revenue')

if submitted:
    payload = {
        'Product_Weight': product_weight,
        'Product_Sugar_Content': product_sugar,
        'Product_Allocated_Area': product_area,
        'Product_MRP': product_mrp,
        'Store_Size': store_size,
        'Store_Location_City_Type': city_type,
        'Store_Type': store_type,
        'Product_Id_char': product_id_char,
        'Store_Age_Years': store_age,
        'Product_Type_Category': product_type_cat,
    }
    try:
        response = requests.post(f'{BACKEND_URL}/v1/predict', json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            predicted = result['predicted_sales']
            st.success(f'Predicted Sales Revenue: Rs. {predicted:,.2f}')
            st.info(
                f'This product-store combination is forecast to generate '
                f'Rs. {predicted:,.2f} in sales this quarter.'
            )
        else:
            st.error(f'API Error: {response.status_code} — {response.text}')
    except requests.exceptions.ConnectionError:
        st.error('Cannot connect to backend. Ensure the backend container is running on port 7860.')
    except Exception as e:
        st.error(f'Unexpected error: {str(e)}')
