import streamlit as st 
import pyodbc 
import pandas as pd

st.set_page_config(
    page_title='View Data',
    page_icon='📄',
    layout='wide'

)
st.title('Customer data from Vodafone')


st.cache_resource(show_spinner='connecting to Database.....')
'''def initialize_connection():
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        +st.secrets['SERVER']
        +";DATABASE="
        +st.secrets['DATABASE']
        +";UID="
        +st.secrets['UID']
        +";PWD="
        +st.secrets['PWD']
        )
    
    return connection

conn = initialize_connection()'''


st.cache_data()
def db_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        
        df = pd.DataFrame.from_records(data=rows, columns=[ column[0] for column in cur.description])
        
    return df
st.cache_data()
def choose_all_features():
    query = "Select * from LP2_Telco_churn_first_3000"
    df = db_query(query)
    return df
    
def choose_numeric_features():
    query = "SELECT * FROM LP2_Telco_churn_first_3000"
    df = db_query(query)

    # Filter only numeric columns
    numeric_columns = df.select_dtypes(include=['number'])

    return numeric_columns
    
def choose_categorical_features():
    query = "SELECT * FROM LP2_Telco_churn_first_3000"
    df = db_query(query)

    # Filter only numeric columns
    category_columns = df.select_dtypes(include=['object'])

    return category_columns
    

if __name__ == '__main__':
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.selectbox('Choose a feature', options=['All Features', 'Numeric Features', 'Category Features'], key='chosen_columns'
                     )
        
    if st.session_state['chosen_columns'] == 'All Features':
        data = choose_all_features()
        st.dataframe(data)
    elif st.session_state['chosen_columns'] == 'Numeric Features':
        data = choose_numeric_features()
        st.dataframe(data)
    else :
        st.session_state['chosen_columns'] == 'Category Features'
        data = choose_categorical_features()
        st.dataframe(data)

    #st.write(st.session_state)
