import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title and Image
st.title("🏦 Financial Dashboard")
st.image("https://media.gettyimages.com/id/1925354468/photo/tax-word-written-on-an-office-table.jpg?s=612x612&w=gi&k=20&c=YDZS3PAmhm3uWj4WvCGitqClGqGCYBbYDRK7JOOll10=", width=400)

# User Input
salary = st.number_input("Enter your Annual Salary ($)", min_value=0, value=50000, step=1000)
deductions = st.number_input("Enter Deductions ($)", min_value=0, value=5000, step=500)

# Tax Brackets
brackets = {0: 0.10, 10000: 0.12, 40000: 0.22, 85000: 0.24, 160000: 0.32, 210000: 0.35, 530000: 0.37}

def calculate_tax(income):
    tax = 0
    prev_bracket = 0
    for bracket, rate in brackets.items():
        if income > bracket:
            tax += (min(income, bracket) - prev_bracket) * rate
            prev_bracket = bracket
    return tax

# Calculations
net_income = max(0, salary - deductions)
tax = calculate_tax(net_income)
net_salary = salary - tax

# Display Financial Summary
st.subheader("📊 Tax Breakdown")
st.write(f"**Annual Salary:** ${salary:,.2f}")
st.write(f"**Deductions:** ${deductions:,.2f}")
st.write(f"**Tax Payable:** ${tax:,.2f}")
st.write(f"**Net Salary After Tax:** ${net_salary:,.2f}")

# Pie Chart for Tax Breakdown
fig1, ax1 = plt.subplots()
labels = ['Tax Payable', 'Net Salary']
sizes = [tax, net_salary]
colors = ['red', 'green']
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
st.pyplot(fig1)

# Line Graph for Salary Growth Projection
st.subheader("📈 Salary Growth Projection")
years = np.arange(1, 11)
growth_rate = 0.05  # 5% annual increase
future_salaries = salary * (1 + growth_rate) ** years

fig2, ax2 = plt.subplots()
ax2.plot(years, future_salaries, marker='o', linestyle='-', color='blue')
ax2.set_xlabel("Years")
ax2.set_ylabel("Projected Salary ($)")
ax2.set_title("Projected Salary Growth Over 10 Years")
st.pyplot(fig2)

# Bar Chart for Tax Across Different Income Levels
st.subheader("📊 Tax Paid Across Different Incomes")
income_levels = [30000, 60000, 90000, 120000, 150000]
taxes_paid = [calculate_tax(income) for income in income_levels]

fig3, ax3 = plt.subplots()
ax3.bar(income_levels, taxes_paid, color='purple')
ax3.set_xlabel("Income Levels ($)")
ax3.set_ylabel("Tax Paid ($)")
ax3.set_title("Tax Paid at Different Income Levels")
st.pyplot(fig3)
