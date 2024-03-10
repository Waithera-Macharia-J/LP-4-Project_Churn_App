import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os
import datetime

st.set_page_config(
    page_title='Predict',
    page_icon='🤖',
    layout='wide'
)

@st.cache_resource(show_spinner='Loading models')
def decision_tree_pipeline():
    pipeline = joblib.load('./models/Decision Tree_model.joblib')
    return pipeline

 
@st.cache_resource(show_spinner='Loading models')
def random_forest_pipeline(): 
    pipeline = joblib.load('./models/Random Forest_model.joblib')  
    return pipeline


def choose_model():
    
    column1, column2 = st.columns(2)
    
    with column1:
        st.selectbox ('Please select a model', options=['Decision Tree Model', 'Random Forest Model'],key= 'selected_model')    
    with column2:
        pass
    
    if st.session_state['selected_model'] == 'Decision Tree Model':
        pipeline = decision_tree_pipeline()
    else:
        pipeline = random_forest_pipeline()
        
    encoder = joblib.load('./models/encoder.joblib')

    return pipeline, encoder



if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None  
            
if 'probability' not in st.session_state:
    st.session_state['probability'] = None


def make_prediction(pipeline, encoder):
    gender = st.session_state['gender']
    SeniorCitizen = st.session_state['SeniorCitizen']
    Partner = st.session_state['Partner']
    Dependents = st.session_state['Dependents']
    tenure = st.session_state['tenure']
    PhoneService = st.session_state['PhoneService']
    MultipleLines = st.session_state['MultipleLines']
    InternetService = st.session_state['InternetService']
    OnlineSecurity = st.session_state['OnlineSecurity']
    OnlineBackup = st.session_state['OnlineBackup']
    DeviceProtection = st.session_state['DeviceProtection']
    TechSupport = st.session_state['TechSupport']
    StreamingTV = st.session_state['StreamingTV']
    StreamingMovies = st.session_state['StreamingMovies']
    Contract = st.session_state['Contract']
    PaperlessBilling = st.session_state['PaperlessBilling']
    PaymentMethod = st.session_state['PaymentMethod']
    MonthlyCharges = st.session_state['MonthlyCharges']
    TotalCharges = st.session_state['TotalCharges']
    
    
    columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure','PhoneService', 'MultipleLines',
               'InternetService', 'OnlineSecurity','OnlineBackup', 'DeviceProtection', 'TechSupport', 
               'StreamingTV','StreamingMovies', 'Contract', 'PaperlessBilling', 
               'PaymentMethod','MonthlyCharges', 'TotalCharges']
    
    data = [[gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService,MultipleLines, InternetService, OnlineSecurity,OnlineBackup,DeviceProtection, TechSupport, StreamingTV,StreamingMovies, Contract, PaperlessBilling, PaymentMethod,MonthlyCharges, TotalCharges]]
    
    # Create a dataframe
    df = pd.DataFrame(data, columns=columns)
    
     
    df ['Prediction time'] = datetime.date.today()
    df ['Model Used'] = st.session_state['selected_model']
    
    df.to_csv('./data/history.csv', mode = 'a', header =not os.path.exists('./data/history.csv'), index=False)
   
    #Make prediction
    pred = pipeline.predict(df) 
    pred = int(pred[0])
    prediction = encoder.inverse_transform([pred])
    
    # Get probabilities
    probability = pipeline.predict_proba(df)
    
    # updating state
    st.session_state['prediction'] = prediction
    st.session_state['probability'] = probability
    
    return prediction,probability

def info_form():
    
    pipeline, encoder = choose_model()

    with st.form('input feature'):
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write('### Personal Details')
            # Add input fields and store values in input_features dictionary
            st.selectbox('Select Gender:', options=['Male','Female'], key='gender')
            st.selectbox('SeniorCitizen:', options=['Yes', 'No'], key='SeniorCitizen')
            st.selectbox('Partner:', options=['Yes','No'], key='Partner')
            st.selectbox('Dependents:', options=['Yes','No'], key='Dependents')
            st.number_input('Tenure:', min_value= 0, max_value = 71, step=1, key='tenure')
            

        with col2:
            st.write('### Services Subscribed to')
            # Subscriptions input fields
            st.selectbox('PhoneService:', options=['Yes','No'], key='PhoneService')
            st.selectbox('MultipleLines:', options=['Yes','No'], key='MultipleLines')
            st.selectbox('InternetService:',options=['Yes','No'],key='InternetService')
            st.selectbox('OnlineSecurity:',options=['Yes','No'],key='OnlineSecurity')
            st.selectbox('OnlineBackup:',options=['Yes','No'],key='OnlineBackup')
            st.selectbox('DeviceProtection:',options=['Yes','No'],key='DeviceProtection')
            st.selectbox('TechSupport:',options=['Yes','No'],key='TechSupport')
            st.selectbox('StreamingTV:',options=['Yes','No'],key='StreamingTV')
            st.selectbox('StreamingMovies:',options=['Yes','No'],key='StreamingMovies')
            

        with col3:
            st.write('### Payment Options')
            # Input fields for payment methods
            st.selectbox('Contract:', options=['Month-to-month','Two year','One year'], key='Contract')
            st.selectbox('PaperlessBilling:', options=['Yes','No'], key='PaperlessBilling')
            st.selectbox('PaymentMethod:', options=['Electronic check','Mailed check','Bank transfer (automatic)','Credit card (automatic)'], key='PaymentMethod')
            st.number_input('MonthlyCharges:',min_value= 0,  key='MonthlyCharges')
            st.number_input('TotalCharges:', min_value =0, key='TotalCharges')
            
        st.form_submit_button('Predict', on_click=make_prediction, kwargs=dict(pipeline = pipeline, encoder = encoder))
        
        
if __name__ == '__main__':
    st.title('Predictor')
    info_form()
    
    prediction = st.session_state['prediction']
    probability = st.session_state['probability']  
         
    if not prediction:
        st.markdown('### Prediction will show here')
    elif prediction == 'Yes':
        probability_of_true = probability[0][0] * 100        
        st.markdown(f'### Customer will churn with a probability of:{round(probability_of_true, 2)}%')
    else:
        probability_of_false = probability[0][1] * 100 
        st.markdown(f'### Customer will not churn with a probability of:{round (probability_of_false,2)}%')

    st.write(st.session_state)