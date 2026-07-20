import streamlit as st
import requests

st.title("Retail Banking and Wealth Advisor")
question =st.text_input("Enter your quetsion")

if st.button("Get Advice"):
    payload = {
        "question" :question,
        "customer_profile":{
        "customer_id":"C002",
        "age" :39,
        "income":130000,
        "employment":"salaried",
        "risk_appetite":"moderate",
        "goals":[
          {
              "goal":"Car Purchase",
              "target_amount":20000000,
              "years":2
          }
      ],
        "existing_investments":{
          "equity" :1000000,
          "debt":300000,
          "fd":1000000

      },
        "liabilities":{
        "home_loan":3000000
      },
        "monthly_expenses":50000,
        "credit_score":750

  }
    }

    response = requests.post(
        "http://127.0.0.1:8000/query",
        json=payload
    )

    if response.status_code ==200:
        st.write(response.json()["answer"])
    else:
        st.error("Failed to get a response")
