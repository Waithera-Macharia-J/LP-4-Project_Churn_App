import streamlit as st 

st.set_page_config(
    page_title='Predict',
    page_icon=':)',
    layout='wide'

)

# ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
#       'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
#      'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
#     'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
#    'MonthlyCharges', 'TotalCharges', 'Churn'],
    
    
def demo_form ():
    st.number_input()