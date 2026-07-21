import streamlit as st
import requests

st.title("Retail Banking and Wealth Advisor")

st.subheader("Customer Profile")

customer_id=st.text_input("Customer ID")
age =st.number_input("Age",
                     min_value=18,
                     max_value=90,
                     )
income=st.number_input("Annual Income",
                       min_value=0,
                       )

employment=st.selectbox("Employment",
                        ["salaried","Self Employed","Business"]
                        )
risk_appetite=st.selectbox("Risk Appetite",
                          ["Low","Moderate","High"] 
                        )
monthly_expense=st.number_input("Monthly Expense",
                                min_value=0
                                )
credit_score=st.number_input("Credit Score",
                             min_value=300,
                             max_value=900
                             )
st.subheader("Financial Details")

equity=st.number_input("Equity Investments",
                       min_value=0
                       )
debt=st.number_input("Debt",
                       min_value=0
                       )
fd=st.number_input("Fixed Deposit",
                       min_value=0
                       )
loan=st.number_input("Loan",
                       min_value=0
                       )
st.subheader("Goal")

goal=st.text_input("Goal")
amount=st.number_input("Target Amount Needed",
                       min_value=0
                       )
years=st.number_input("Years to achieve goal",
                       min_value=1
                       )

st.subheader("Question")

question =st.text_input("Enter your question")

if st.button("Get Advice"):
    payload = {
        "question" :question,
        "customer_profile":{
        "customer_id":customer_id,
        "age" :age,
        "income":income,
        "employment":employment,
        "risk_appetite":risk_appetite,
        "goals":[
          {
              "goal":goal,
              "target_amount":amount,
              "years":years
          }
      ],
        "existing_investments":{
          "equity" :equity,
          "debt":debt,
          "fd":fd

      },
        "liabilities":{
        "home_loan":loan
      },
        "monthly_expenses":monthly_expense,
        "credit_score":credit_score

  }
    }

    with st.spinner("Generating...."):

        response = requests.post(
        "http://127.0.0.1:8000/query",
        json=payload
    )

    if response.status_code ==200:
        st.success("Generated")
        st.write(response.json()["answer"])
    else:
        st.error("Failed to get a response")
