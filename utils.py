import streamlit as st

feature_descriptions = """

1. **Gender**: Customer gender
2. **SeniorCitizen**: type of citizen
3. **Partner**: Does customer have partner? 
4. **Dependents**: does customer have dependents?
5. **tenure**: Does customer have tenure?
6. **PhoneService**: Does customer subscribe to phone service?
7. **MultipleLines**: Does custmer have multiple lines?
8. **InternetService**: Does customer subscribe to internet service
9. **OnlineSecurity**:  Does customer subscribe to online security
10. **OnlineBackup**:Does customer subscribe to online backup?
11. **DeviceProtection**: Does customer subscribe device protection?
12. **TechSupport**: Does customer subscribe to Tech support?
13. **StreamingTV**: Does customer subscribe to Steaming TV
14. **StreamingMovies**: Does customer subscribe to StreamingMovies
15. **Contract**: Month-to-month;two-year;one-year;
16. **PaperlessBilling**: Does customer take paperless billing?
17. **PaymentMethod**: Electronic check';'Mailed check';'Bank transfer (automatic)';'Credit card (automatic);
18. **MonthlyCharges**: What's the customers monthly charge??
19. **TotalCharges**: What's the customers total charges??




"""


column_1 = """
### Attrition Insight
Churn App is a Machine Learning application that  predicts the likelihood of a customer to churn froma telecommunication company based on various demographics.

### Key Features
- **View Data:** Customer data from Vodafone.
- **Dashboard:** Explore interactive data visualizations for insights.
- **Real-time Prediction:** Instantly see predictions for Customer Churn
- **History:** See past predictions made.

### User Benefits
- **Data-driven Decisions:** Make informed decisions backed by data analytics.
- **Easy Machine Learning:** Utilize powerful machine learning algorithms effortlessly.
- **Live Demo:** Watch a demo video to see the app in action.

[Watch Demo Video](link)
"""

column_2 = """
### Machine Learning Integration
- **Model Selection:** Choose between two advanced models for accurate predictions.
- **Seamless Integration:** Integrate predictions into your workflow with a user-friendly interface.
- **Probability Estimates:** Gain insights into the likelihood of predicted outcomes.

### Need Help?
For collaborations contact me at [joyce.macharia@azubiafrica.org](mailto:joyce.macharia@azubiafrica.org).
"""


#Build command
# mkdir .streamlit; cp /etc/secrets/secrets.toml ./.streamlit/; pip install --upgrade pip && pip install -r requirements.txt