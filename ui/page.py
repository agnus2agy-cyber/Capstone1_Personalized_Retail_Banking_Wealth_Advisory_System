import streamlit as st
import requests


st.set_page_config(
    page_title="Retail Banking and Wealth Advisor",
    layout="wide"
)

st.title("Retail Banking and Wealth Advisor")


# =====================================================
# Initialize Chat History
# =====================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =====================================================
# Create Two Columns
# =====================================================

left_col, right_col = st.columns([1, 2])


# =====================================================
# Left Side - PDF Upload + Customer Profile
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


            try:

                with st.spinner("Uploading PDF..."):

                    response = requests.post(
                        "http://127.0.0.1:8000/query/v1/retail/upload",
                        files=files,
                        timeout=120
                    )


                if response.status_code == 200:

                    st.success(
                        "PDF loaded successfully"
                    )

                else:

                    st.error(response.text)


            except requests.exceptions.ConnectionError:

                st.error(
                    "Upload service is not running."
                )


            except requests.exceptions.Timeout:

                st.warning(
                    "PDF upload timeout."
                )



    # =====================================================
    # Customer Profile
    # =====================================================

    st.divider()

    st.subheader("Customer Profile")


    customer_id = st.text_input(
        "Customer ID"
    )


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
        [
            "Salaried",
            "Self Employed",
            "Business"
        ]
    )


    risk_appetite = st.selectbox(
        "Risk Appetite",
        [
            "Low",
            "Moderate",
            "High"
        ]
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


    goal = st.text_input(
        "Goal"
    )


    amount = st.number_input(
        "Target Amount Needed",
        min_value=0
    )


    years = st.number_input(
        "Years to achieve Goal",
        min_value=1
    )



# =====================================================
# Right Side - Chat
# =====================================================

with right_col:

    st.subheader("Financial Advisor Chat")


    # Display history

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


    question = st.chat_input(
        "Ask your financial question"
    )


    if question:


        # Store user message

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )


        customer_profile = {

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


        payload = {

            "question": question,

            "customer_profile": customer_profile,

            "chat_history": st.session_state.chat_history

        }


        try:

            with st.spinner(
                "Processing request..."
            ):

                response = requests.post(

                    "http://127.0.0.1:8000/query/v1/retail",

                    json=payload,

                    timeout=120

                )


            if response.status_code == 200:


                answer = response.json()["answer"]


                st.session_state.chat_history.append(

                    {
                        "role": "assistant",
                        "content": answer
                    }

                )


                st.rerun()


            else:

                st.error(response.text)



        except requests.exceptions.ConnectionError:

            st.error(
                "Financial Advisor server is not running."
            )


        except requests.exceptions.Timeout:

            st.warning(
                "Financial Advisor server timeout."
            )


        except requests.exceptions.RequestException as e:

            st.error(
                f"API Error: {e}"
            )



    if st.button("Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()
