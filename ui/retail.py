import json
import streamlit as st
import requests

st.set_page_config(page_title="Retail Banking and Wealth Advisor", layout="wide")

st.title("Retail Banking and Wealth Advisor")

# Create two columns
left_col, right_col = st.columns([1, 2])

# =====================================================
# Left Side - PDF Upload
# =====================================================
with left_col:

    st.subheader("Upload PDF")

    uploaded_pdf = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

    if uploaded_pdf is not None:

        if st.button("Upload PDF"):

            files = {
            "file": (
                uploaded_pdf.name,
                uploaded_pdf.getvalue(),
                "application/pdf"
            )
        }
            response = requests.post(
            "http://127.0.0.1:8000/query/v1/retail/upload",
            files=files
        )

            if response.status_code == 200:
                st.success("PDF uploaded successfully.")
            else:
                st.error(response.text)

# =====================================================
# Right Side - Customer Details
# =====================================================
with right_col:

    st.subheader("Customer Profile")

    customer_id = st.text_input("Customer ID")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=90
    )

    income = st.number_input(
        "Annual Income",
        min_value=0
    )

    employment = st.selectbox(
        "Employment",
        ["Salaried", "Self Employed", "Business"]
    )

    risk_appetite = st.selectbox(
        "Risk Appetite",
        ["Low", "Moderate", "High"]
    )

    monthly_expense = st.number_input(
        "Monthly Expense",
        min_value=0
    )

    credit_score = st.number_input(
        "Credit Score",
        min_value=300,
        max_value=900
    )

    st.subheader("Financial Details")

    equity = st.number_input(
        "Equity Investments",
        min_value=0
    )

    debt = st.number_input(
        "Debt",
        min_value=0
    )

    fd = st.number_input(
        "Fixed Deposit",
        min_value=0
    )

    loan = st.number_input(
        "Loan",
        min_value=0
    )

    st.subheader("Goal")

    goal = st.text_input("Goal")

    amount = st.number_input(
        "Target Amount Needed",
        min_value=0
    )

    years = st.number_input(
        "Years to achieve Goal",
        min_value=1
    )

    st.subheader("Question")

    question = st.text_input("Enter your question")

# =====================================================
# Submit Button
# =====================================================
    try:

     if st.button("Get Advice", type="primary"):

        pdf_file = None

        if uploaded_pdf is not None:
            pdf_file = (
                uploaded_pdf.name,
                uploaded_pdf.getvalue(),
                "application/pdf"
            )

        payload = {
            "question": question,
            "customer_profile": {
                "customer_id": customer_id,
                "age": age,
                "income": income,
                "employment": employment,
                "risk_appetite": risk_appetite,
                "goals": [
                    {
                        "goal": goal,
                        "target_amount": amount,
                        "years": years
                    }
                ],
                "existing_investments": {
                    "equity": equity,
                    "debt": debt,
                    "fd": fd
                },
                "liabilities": {
                    "home_loan": loan
                },
                "monthly_expenses": monthly_expense,
                "credit_score": credit_score
            }
        }

        with st.spinner("Generating Advice..."):

            
                response = requests.post(
                    "http://127.0.0.1:8000/query/v1/retail",
                    json=payload
                )

        if response.status_code == 200:
            st.success("Advice Generated Successfully")
            st.write(response.json()["answer"])
        else:
            st.error("Failed to get a response")
            st.write(response.text)

    except requests.exceptions.ConnectionError:
       st.error(
        "Financial Advisor server is not running. Please start it and try again."
       )

    except requests.exceptions.Timeout:
       st.warning(
        "Financial Advisor server is taking too long to respond."
       )

    except requests.exceptions.RequestException as e:
       st.error(f"API Error: {e}")