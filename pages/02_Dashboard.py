from winreg import QueryInfoKey
import streamlit as st
import pandas as pd
import pyodbc
import seaborn as sns
import matplotlib.pyplot as plt

# Page title and icon
st.set_page_config(
    page_title="Dashboard",
    page_icon="📈"
)

@st.cache_resource(show_spinner='connecting to Database.....')
def initialize_connection():
    connection = pyodbc.connect(
        "DRIVER={SQL Server};SERVER="
        + st.secrets['SERVER']
        + ";DATABASE="
        + st.secrets['DATABASE']
        + ";UID="
        + st.secrets['UID']
       + ";PWD="
        + st.secrets['PWD']
    )
    return connection

conn = initialize_connection()

# Function to execute SQL QueryInfoKey and return DataFrame
@st.cache_data()
def query_database(query):
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        df = pd.DataFrame.from_records(data=rows, columns=[column[0] for column in cur.description])
    return df

# Function to load dataset from file
def load_dataset(file_path):
    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    return df

# Function to display visualizations for each feature
def display_visualizations(data):
    st.subheader('Visualizations')

    # Set style
    sns.set_style('whitegrid')

    # Create columns layout
    col1, col2 = st.columns(2)

    # Chart for Gender
    with col1:
        st.write("### Gender Distribution")
        gender_counts = data['gender'].value_counts()
        plt.figure(figsize=(10, 6))
        gender_plot = sns.barplot(x=gender_counts.index, y=gender_counts.values, palette='pastel')
        gender_plot.set_title('Gender Distribution')
        gender_plot.set_xlabel('Gender')
        gender_plot.set_ylabel('Count')
        st.pyplot(fig=gender_plot.figure)

    # Chart for Tenure
    with col2:
        st.write("### Tenure Distribution")
        plt.figure(figsize=(10, 6))
        tenure_plot = sns.histplot(data['tenure'], bins=20, kde=True, color='skyblue')
        tenure_plot.set_title('Tenure Distribution')
        tenure_plot.set_xlabel('Tenure')
        tenure_plot.set_ylabel('Frequency')
        st.pyplot(fig=tenure_plot.figure)

    # Chart for Contract
    with col1:
        st.write("### Contract Distribution")
        contract_counts = data['Contract'].value_counts()
        plt.figure(figsize=(10, 6))
        contract_plot = sns.barplot(x=contract_counts.index, y=contract_counts.values, palette='pastel')
        contract_plot.set_title('Contract Distribution')
        contract_plot.set_xlabel('Contract Type')
        contract_plot.set_ylabel('Count')
        st.pyplot(fig=contract_plot.figure)

    # Chart for Payment Method
    with col2:
        st.write("### Payment Method Distribution")
        payment_counts = data['PaymentMethod'].value_counts()
        plt.figure(figsize=(10, 6))
        payment_plot = sns.barplot(x=payment_counts.index, y=payment_counts.values, palette='pastel')
        payment_plot.set_title('Payment Method Distribution')
        payment_plot.set_xlabel('Payment Method')
        payment_plot.set_ylabel('Count')
        payment_plot.set_xticklabels(payment_plot.get_xticklabels(), rotation=45, horizontalalignment='right')
        st.pyplot(fig=payment_plot.figure)

    # Chart for Monthly Charges
    with col1:
        st.write("### Monthly Charges Distribution")
        plt.figure(figsize=(10, 6))
        monthly_charges_plot = sns.histplot(data['MonthlyCharges'], bins=20, kde=True, color='lightgreen')
        monthly_charges_plot.set_title('Monthly Charges Distribution')
        monthly_charges_plot.set_xlabel('Monthly Charges')
        monthly_charges_plot.set_ylabel('Frequency')
        st.pyplot(fig=monthly_charges_plot.figure)

    # Chart for Total Charges
    with col2:
        st.write("### Total Charges Distribution")
        total_charges_numeric = pd.to_numeric(data['TotalCharges'], errors='coerce').dropna()
        plt.figure(figsize=(10, 6))
        total_charges_plot = sns.histplot(total_charges_numeric, bins=20, kde=True, color='salmon')
        total_charges_plot.set_title('Total Charges Distribution')
        total_charges_plot.set_xlabel('Total Charges')
        total_charges_plot.set_ylabel('Frequency')
        st.pyplot(fig=total_charges_plot.figure)

    senior_citizens_data = data[data['SeniorCitizen'] == 1]

    if 'Churn' in senior_citizens_data.columns:
        # Map 'True' and 'False' to 'Yes' and 'No' for the 'Churn' column
        senior_citizens_data['Churn'] = senior_citizens_data['Churn'].map({True: 'Yes', False: 'No'})

        # Count the number of churns (Yes or No) among Senior Citizens
        senior_citizens_churn_counts = senior_citizens_data['Churn'].value_counts()

        # Visualization
        st.write("### Churn Distribution Among Senior Citizens")
        plt.figure(figsize=(10, 6))
        churn_plot = sns.barplot(x=senior_citizens_churn_counts.index, y=senior_citizens_churn_counts.values,
                                palette='pastel')
        churn_plot.set_title('Churn Distribution Among Senior Citizens')
        churn_plot.set_xlabel('Churn')
        churn_plot.set_ylabel('Count')
        st.pyplot(churn_plot.figure)

    with col2:
        if 'Churn' in data.columns:
            data['Churn'] = data['Churn'].map({True: 'Yes', False: 'No'})

            # Count the number of churns (Yes or No) for the entire dataset
            churn_counts = data['Churn'].value_counts()

            # Visualization as a pie chart
            fig, ax = plt.subplots()
            ax.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', startangle=90,
                   colors=['#ff9999', '#66b3ff'])
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            plt.title(' Churn Distribution')

            # Display the plot
            st.pyplot(fig)

# Function to perform Exploratory Data Analysis (EDA)
def perform_eda(data):
    st.subheader('Exploratory Data Analysis (EDA)')

# Function to calculate Key Performance Indicators (KPIs)
def calculate_kpis(data):
    st.subheader('Key Performance Indicators (KPIs)')

    # Check if 'Churn' column exists
    if 'Churn' in data.columns:
        # Calculate KPIs
        total_customers = len(data)
        average_tenure = data['tenure'].mean()
        total_monthly_charges = data['MonthlyCharges'].sum()
        churned_customers = len(data[data['Churn'] == 'Yes'])
        churn_rate = (churned_customers / total_customers) * 100
        total_revenue = pd.to_numeric(data['TotalCharges'], errors='coerce').sum()
        average_revenue = total_revenue / total_customers

        # Create a DataFrame to hold KPIs
        kpi_data = {
            'KPI Name': ['Total Customers', 'Average Tenure', 'Total Monthly Charges', 'Churned Customers', 'Churn Rate',
                         'Total Revenue', 'Average Revenue'],
            'Value': [total_customers, f"{average_tenure:.2f}", f"${total_monthly_charges:.2f}", churned_customers,
                      f"{churn_rate:.2f}", f"${total_revenue:.2f}", f"${average_revenue:.2f}"]
        }
        kpi_df = pd.DataFrame(kpi_data)

        st.table(kpi_df)
    else:
        st.warning("Churn column not found in the dataset.")

# Load data from the database
conn = initialize_connection()

# Title of the dashboard
st.title('Churn Analysis')

# Add selectbox to choose between EDA and KPIs
selected_analysis = st.selectbox('Select Analysis Type', ['Exploratory Data Analysis (EDA)', 'Key Performance Indicators (KPIs)'])

# Add selectbox to choose dataset
selected_dataset = st.selectbox('Select Dataset',
                                ['LP2_Telco_churn_first_3000', 'Telco-churn-second-2000.xlsx', 'LP2_Telco-churn-last-2000.csv'])

if selected_dataset == 'LP2_Telco_churn_first_3000':
    # Load data from the first dataset
    data = query_database(
        "SELECT gender, tenure, Contract, PaymentMethod, SeniorCitizen, Churn, MonthlyCharges, TotalCharges FROM LP2_Telco_churn_first_3000")
else:
    # Load data from the selected file
    file_path = f"data/{selected_dataset}"
    data = load_dataset(file_path)

# Perform the selected analysis
if selected_analysis == 'Exploratory Data Analysis (EDA)':
    perform_eda(data)
else:
    calculate_kpis(data)

# Display visualizations (always shown regardless of the selected analysis)
display_visualizations(data)
