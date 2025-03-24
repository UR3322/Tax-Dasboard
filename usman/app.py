import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import uuid
import os

# CSV File Path
CSV_FILE = "customer_data.csv"

# Load existing data or create a new DataFrame
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Customer ID", "Name", "Salary", "Deductions", "Tax Payable", "Net Salary"])

# Save data to CSV
def save_data(data):
    data.to_csv(CSV_FILE, index=False)

# Tax Calculation Function
def calculate_tax(income):
    tax_brackets = {
        0: 0.10, 10000: 0.12, 40000: 0.22, 85000: 0.24,
        160000: 0.32, 210000: 0.35, 530000: 0.37
    }
    tax = 0
    prev_bracket = 0
    for bracket, rate in tax_brackets.items():
        if income > bracket:
            tax += (min(income, bracket) - prev_bracket) * rate
            prev_bracket = bracket
    return tax

# Dashboard UI
st.title("🏦 Tax Estimator Dashboard")
st.image("https://media.gettyimages.com/id/1925354468/photo/tax-word-written-on-an-office-table.jpg?s=612x612&w=gi&k=20&c=YDZS3PAmhm3uWj4WvCGitqClGqGCYBbYDRK7JOOll10=", width=300)

# Customer Info
name = st.text_input("Enter Your Name")
salary = st.number_input("Enter Your Annual Salary ($)", min_value=0, value=50000, step=1000)
deductions = st.number_input("Enter Deductions ($)", min_value=0, value=5000, step=500)

if st.button("Calculate Tax"):
    net_income = max(0, salary - deductions)
    tax = calculate_tax(net_income)
    net_salary = salary - tax
    customer_id = str(uuid.uuid4())[:8]  # Generate a unique ID

    # Load and update data
    data = load_data()
    new_entry = pd.DataFrame({
        "Customer ID": [customer_id], "Name": [name], "Salary": [salary],
        "Deductions": [deductions], "Tax Payable": [tax], "Net Salary": [net_salary]
    })
    data = pd.concat([data, new_entry], ignore_index=True)
    save_data(data)
    
    # Display Results
    st.subheader("📊 Tax Breakdown")
    st.write(f"**Customer ID:** {customer_id}")
    st.write(f"**Annual Salary:** ${salary:,.2f}")
    st.write(f"**Deductions:** ${deductions:,.2f}")
    st.write(f"**Tax Payable:** ${tax:,.2f}")
    st.write(f"**Net Salary After Tax:** ${net_salary:,.2f}")

    # Graph
    fig, ax = plt.subplots()
    labels = ['Tax Payable', 'Net Salary']
    sizes = [tax, net_salary]
    colors = ['red', 'green']
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    st.pyplot(fig)

# Delete Customer Data
st.subheader("🗑️ Delete Your Data")
delete_id = st.text_input("Enter Customer ID to Delete Data")
if st.button("Delete"):
    data = load_data()
    if delete_id in data["Customer ID"].values:
        data = data[data["Customer ID"] != delete_id]
        save_data(data)
        st.success("✅ Data deleted successfully!")
    else:
        st.error("❌ Customer ID not found!")
