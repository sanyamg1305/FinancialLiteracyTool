import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
import random

st.set_page_config(page_title="Financial Buddy", layout="centered")
st.title("💸 Financial Buddy")
st.caption("Your one-stop tool to master personal finance as a student — powered by Python + Streamlit")

# ----------------- Tabs ------------------
tab1, tab2, tab3 = st.tabs(["📈 SIP Calculator", "🧾 Budgeting Tool", "🧠 Financial Quiz"])

# ----------------- TAB 1: SIP CALCULATOR ------------------
with tab1:
    st.header("What is an SIP?")
    st.markdown("""
    A **Systematic Investment Plan (SIP)** is a method of investing a fixed sum regularly in mutual funds.
    SIPs leverage **compounding** and **rupee cost averaging** to help grow your wealth over time.

    **Formula used:**
    ```
    FV = P × [(1 + r)^n - 1] × (1 + r) / r
    ```
    Where:
    - `FV`: Future Value
    - `P`: Monthly SIP
    - `r`: Monthly rate of return
    - `n`: Number of months
    """)

    monthly_sip = st.number_input("💰 Monthly SIP Amount (₹)", min_value=500, value=5000, step=500)
    years = st.slider("📆 Investment Duration (Years)", 1, 40, 10)
    annual_return = 0.15
    months = years * 12
    monthly_return = annual_return / 12

    invested_amount = monthly_sip * months
    wealth = 0
    total_wealth_progress = []
    invested_progress = []

    for i in range(months):
        wealth += monthly_sip * ((1 + monthly_return) ** (months - i))
        total_wealth_progress.append(wealth)
        invested_progress.append(monthly_sip * (i + 1))

    gain = wealth - invested_amount

    st.subheader("🔍 Summary")
    st.markdown(f"- **Total Invested:** ₹{invested_amount:,.0f}")
    st.markdown(f"- **Wealth Gained:** ₹{gain:,.0f}")
    st.markdown(f"- **Final Portfolio Value:** ₹{wealth:,.0f}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, months+1)), y=total_wealth_progress,
                             mode='lines', name='Total Portfolio Value', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=list(range(1, months+1)), y=invested_progress,
                             mode='lines', name='Invested Amount', line=dict(color='orange')))
    fig.update_layout(title="Growth of SIP Investment Over Time", xaxis_title="Month", yaxis_title="₹")
    st.plotly_chart(fig)

    st.info("💡 Start early. Even small SIPs can grow big thanks to compounding!")

# ----------------- TAB 2: BUDGETING TOOL ------------------
with tab2:
    st.header("📊 Plan Your Monthly Budget")

    monthly_income = st.number_input("💼 Your Monthly Income (₹)", min_value=1000, value=50000, step=1000)
    template_choice = st.selectbox("📋 Choose a Budget Template:", ["50/30/20 Rule", "Basic Essentials", "Custom"])

    if template_choice == "50/30/20 Rule":
        budget = {
            "Needs (50%)": monthly_income * 0.50,
            "Wants (30%)": monthly_income * 0.30,
            "Savings (20%)": monthly_income * 0.20
        }
    elif template_choice == "Basic Essentials":
        budget = {
            "Rent & Utilities": monthly_income * 0.30,
            "Food": monthly_income * 0.20,
            "Transport": monthly_income * 0.10,
            "Savings": monthly_income * 0.25,
            "Entertainment": monthly_income * 0.10,
            "Misc": monthly_income * 0.05
        }
    else:
        st.info("Enter custom budget categories 👇")
        categories = st.text_area("Comma-separated categories", "Rent,Food,Savings,Entertainment")
        categories = [c.strip() for c in categories.split(",") if c.strip()]
        budget = {}
        for cat in categories:
            budget[cat] = st.number_input(f"{cat} (₹)", min_value=0, value=0, step=100)

    total_allocated = sum(budget.values())
    st.markdown(f"**Total Allocated:** ₹{total_allocated:,.0f}")
    st.markdown(f"**Remaining Balance:** ₹{monthly_income - total_allocated:,.0f}")

    fig2 = go.Figure(data=[go.Pie(labels=list(budget.keys()), values=list(budget.values()), hole=.4)])
    fig2.update_layout(title="Your Monthly Budget Breakdown")
    st.plotly_chart(fig2)

    # Budget Excel Template
    st.subheader("📥 Download Budgeting Excel Template")
    budget_template = pd.DataFrame({
        "Category": list(budget.keys()),
        "Amount (₹)": list(budget.values())
    })

    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Budget')
        return output.getvalue()

    excel_data = to_excel(budget_template)
    st.download_button(label="📤 Download Excel Template",
                       data=excel_data,
                       file_name="budget_template.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Emergency fund tool
    st.header("🛡️ Emergency Fund Estimator")
    expenses = st.number_input("Your Avg Monthly Expenses (₹)", min_value=1000, value=20000)
    emergency_fund = expenses * 6
    st.markdown(f"👉 You should ideally have **₹{emergency_fund:,.0f}** as emergency savings (6 months of expenses).")

# ----------------- TAB 3: QUIZ ------------------
with tab3:
    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.correct = 0
        st.session_state.answers = []

    st.header("🧠 Financial Literacy Quiz Game")

    questions = [
        {
            "question": "What is a credit score primarily used for?",
            "options": ["Tracking your income", "Approving loans and credit", "Paying taxes", "Budgeting monthly"],
            "answer": "Approving loans and credit",
            "explanation": "A credit score helps banks determine your creditworthiness when applying for loans or credit cards."
        },
        {
            "question": "Which one offers higher potential returns?",
            "options": ["Fixed Deposit", "Mutual Fund"],
            "answer": "Mutual Fund",
            "explanation": "Mutual funds invest in market-linked instruments, which can give higher returns than fixed deposits over time."
        },
        {
            "question": "What is 'inflation'?",
            "options": ["Decrease in prices", "Rise in purchasing power", "Increase in prices over time", "Tax increase"],
            "answer": "Increase in prices over time",
            "explanation": "Inflation is the general rise in the price of goods and services, reducing the value of money over time."
        },
        {
            "question": "Which is a liability?",
            "options": ["Loan", "Fixed Deposit", "Mutual Fund", "Salary"],
            "answer": "Loan",
            "explanation": "A loan is money you owe — a liability on your personal balance sheet."
        },
        {
            "question": "Which investment is considered the safest?",
            "options": ["Stock Market", "Mutual Fund", "Fixed Deposit", "Crypto"],
            "answer": "Fixed Deposit",
            "explanation": "FDs offer guaranteed returns and are not affected by market fluctuations."
        },
        {
            "question": "What is the 50/30/20 rule?",
            "options": [
                "50% income for rent, 30% for food, 20% for fun",
                "A loan repayment rule",
                "A budgeting rule: 50% needs, 30% wants, 20% savings",
                "A taxation rule"
            ],
            "answer": "A budgeting rule: 50% needs, 30% wants, 20% savings",
            "explanation": "The 50/30/20 rule is a popular budgeting guideline for managing personal finances."
        },
        {
            "question": "What does SIP stand for?",
            "options": ["Single Investment Plan", "Systematic Investment Plan", "Secure Investment Product", "Saving Increment Program"],
            "answer": "Systematic Investment Plan",
            "explanation": "SIP allows you to invest a fixed amount regularly in mutual funds — harnessing compounding and consistency."
        },
        {
            "question": "What’s the safest way to build an emergency fund?",
            "options": ["In stocks", "In savings account or FD", "In crypto", "Via credit card"],
            "answer": "In savings account or FD",
            "explanation": "Emergency funds should be accessible and safe — savings account or fixed deposits are ideal."
        },
        {
            "question": "Which of these is an asset?",
            "options": ["Credit card debt", "Student loan", "Salary", "Mutual fund investment"],
            "answer": "Mutual fund investment",
            "explanation": "Assets are things you own that have value. Mutual funds are investments — and assets."
        },
        {
            "question": "Why is diversification important in investing?",
            "options": ["To focus returns", "To reduce tax", "To reduce risk", "To increase spending"],
            "answer": "To reduce risk",
            "explanation": "Diversifying across assets reduces the impact if one investment performs poorly."
        }
    ]

    random.seed(42)  # Fix seed for repeatable order
    q = questions[st.session_state.quiz_index]

    st.subheader(f"Question {st.session_state.quiz_index + 1} of {len(questions)}")
    st.write(q["question"])
    user_choice = st.radio("Choose your answer:", q["options"], key=f"q{st.session_state.quiz_index}")

    if st.button("Submit Answer"):
        st.session_state.answers.append((q["question"], user_choice, q["answer"], q["explanation"]))
        if user_choice == q["answer"]:
            st.success("✅ Correct!")
            st.session_state.correct += 1
        else:
            st.error("❌ Incorrect.")
            st.info(f"Correct Answer: **{q['answer']}**\n\n📘 {q['explanation']}")

        if st.session_state.quiz_index < len(questions) - 1:
            st.session_state.quiz_index += 1
            st.experimental_rerun()
        else:
            st.success("🎉 You've completed the quiz!")

            st.markdown("---")
            st.subheader("📊 Your Performance:")
            st.markdown(f"- Correct Answers: **{st.session_state.correct}/{len(questions)}**")

            score_pct = int((st.session_state.correct / len(questions)) * 100)
            if score_pct >= 90:
                level = "💎 Money Master"
            elif score_pct >= 70:
                level = "🚀 Growing Financier"
            elif score_pct >= 50:
                level = "📘 Budget Beginner"
            else:
                level = "🌱 Just Getting Started"

            st.markdown(f"🏅 Your Badge: **{level}**")

            st.subheader("🧐 Review Your Answers")
            for i, (question, user_ans, correct_ans, explanation) in enumerate(st.session_state.answers):
                st.markdown(f"**Q{i+1}: {question}**")
                st.markdown(f"- Your Answer: *{user_ans}*")
                st.markdown(f"- Correct Answer: **{correct_ans}**")
                st.markdown(f"📘 {explanation}")
                st.markdown("---")

            if st.button("🔁 Restart Quiz"):
                st.session_state.quiz_index = 0
                st.session_state.correct = 0
                st.session_state.answers = []
                st.experimental_rerun()
