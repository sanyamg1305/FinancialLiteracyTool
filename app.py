import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Financial Buddy", layout="centered")

# --- SIP Calculator ---
def sip_calculator():
    st.header("📈 SIP Calculator")
    
    st.markdown("A **Systematic Investment Plan (SIP)** allows you to invest a fixed amount regularly in mutual funds. It helps you build wealth over time through **power of compounding**.")

    monthly_investment = st.number_input("Monthly Investment (₹)", min_value=100, value=1000, step=100)
    annual_return = st.slider("Expected Annual Return (%)", 5.0, 20.0, 12.0)
    years = st.slider("Investment Duration (Years)", 1, 40, 10)

    months = years * 12
    monthly_rate = annual_return / 12 / 100
    invested_amount = monthly_investment * months

    future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) * (1 + monthly_rate) / monthly_rate)

    st.markdown(f"**Invested Amount:** ₹{invested_amount:,.0f}")
    st.markdown(f"**Total Value (Future Wealth):** ₹{future_value:,.0f}")
    st.markdown(f"**Total Gain:** ₹{(future_value - invested_amount):,.0f}")

    # Plot
    x = np.arange(1, months + 1)
    invested = x * monthly_investment
    wealth = monthly_investment * (((1 + monthly_rate) ** x - 1) * (1 + monthly_rate) / monthly_rate)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=invested, name="Invested Amount", line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=x, y=wealth, name="Total Wealth", line=dict(color='green')))
    fig.update_layout(title="SIP Growth Over Time", xaxis_title="Months", yaxis_title="Amount (₹)")
    st.plotly_chart(fig, use_container_width=True)

# --- Budgeting Tool ---
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Budget Template')
    return output.getvalue()

def budgeting_tool():
    st.header("📊 Budgeting Tool")
    st.markdown("Use this template to **track your monthly income and expenses**.")

    budget_template = pd.DataFrame({
        "Category": ["Income", "Rent", "Groceries", "Utilities", "Transport", "Entertainment", "Savings"],
        "Amount (₹)": [0, 0, 0, 0, 0, 0, 0]
    })

    excel_data = to_excel(budget_template)
    st.download_button("📥 Download Budget Template", excel_data, file_name="budget_template.xlsx")

    st.markdown("You can open the Excel file and start filling in your details. Remember, **spend less than you earn!**")

# --- Financial Quiz ---
def quiz_tool():
    st.header("🧠 Financial Literacy Quiz")
    
    questions = [
        {
            "question": "What does SIP stand for?",
            "options": ["Systematic Investment Plan", "Standard Insurance Policy", "Savings Interest Program", "Safe Investment Plan"],
            "answer": "Systematic Investment Plan"
        },
        {
            "question": "Which one has more risk?",
            "options": ["Fixed Deposit", "Mutual Fund", "Savings Account", "Recurring Deposit"],
            "answer": "Mutual Fund"
        },
        {
            "question": "What is a credit score used for?",
            "options": ["Checking bank balance", "Loan eligibility", "Income tax filing", "Tracking investments"],
            "answer": "Loan eligibility"
        },
        {
            "question": "Which is not a tax-saving instrument?",
            "options": ["PPF", "ELSS", "FD (5 years)", "Credit Card"],
            "answer": "Credit Card"
        },
        {
            "question": "Which one is NOT a type of mutual fund?",
            "options": ["Equity Fund", "Debt Fund", "Savings Fund", "Hybrid Fund"],
            "answer": "Savings Fund"
        },
        {
            "question": "If inflation increases, your money’s value:",
            "options": ["Increases", "Decreases", "Stays same", "Doubles"],
            "answer": "Decreases"
        },
        {
            "question": "UPI stands for?",
            "options": ["Unified Payment Interface", "Universal Pay Info", "User Payment India", "Unique Payment ID"],
            "answer": "Unified Payment Interface"
        },
        {
            "question": "Best way to avoid credit card debt?",
            "options": ["Pay minimum due", "Pay full bill monthly", "Ignore bill", "Get more cards"],
            "answer": "Pay full bill monthly"
        },
        {
            "question": "What is a fixed deposit?",
            "options": ["Loan", "Insurance", "Investment for fixed time", "Mutual fund"],
            "answer": "Investment for fixed time"
        },
        {
            "question": "Which one gives ownership in a company?",
            "options": ["Bond", "FD", "Stock", "PPF"],
            "answer": "Stock"
        },
    ]

    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = 0
        st.session_state.quiz_wrong = []

    if not st.session_state.quiz_submitted:
        answers = []
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            selected = st.radio("", q["options"], key=f"q_{i}")
            answers.append(selected)

        if st.button("✅ Submit Quiz"):
            score = 0
            wrong = []
            for i, q in enumerate(questions):
                if answers[i] == q["answer"]:
                    score += 1
                else:
                    wrong.append((q["question"], answers[i], q["answer"]))
            st.session_state.quiz_submitted = True
            st.session_state.quiz_score = score
            st.session_state.quiz_wrong = wrong

    else:
        st.success(f"🎉 You scored {st.session_state.quiz_score} out of {len(questions)}!")
        if st.session_state.quiz_wrong:
            st.warning("Here are the questions you got wrong:")
            for q_text, your_ans, correct_ans in st.session_state.quiz_wrong:
                st.markdown(f"- ❌ **{q_text}**\n  - Your answer: {your_ans}\n  - Correct answer: {correct_ans}")
        if st.button("🔄 Retake Quiz"):
            st.session_state.quiz_submitted = False
            st.experimental_rerun()

# --- Main App ---
st.title("💰 Financial Buddy")
tab1, tab2, tab3 = st.tabs(["SIP Calculator", "Budgeting Tool", "Financial Quiz"])

with tab1:
    sip_calculator()
with tab2:
    budgeting_tool()
with tab3:
    quiz_tool()
