"""Tax Estimator Dashboard — Streamlit UI.

Estimates U.S. federal income tax (IRS 2024 single-filer brackets) from an
annual salary and deductions. Estimates are saved locally to customer_data.csv
(next to this file) and can be deleted with the issued Customer ID.
"""

import os
import uuid

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from tax_calculator import TAX_BRACKETS_2024_SINGLE, TAX_YEAR, estimate

st.set_page_config(
    page_title="Tax Estimator Dashboard",
    page_icon="🏦",
    layout="centered",
)

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "customer_data.csv")
COLUMNS = ["Customer ID", "Name", "Salary", "Deductions", "Taxable Income",
           "Tax Payable", "Net Salary", "Tax Year"]


def load_data() -> pd.DataFrame:
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=COLUMNS)


def save_data(data: pd.DataFrame) -> None:
    data.to_csv(CSV_FILE, index=False)


st.title("🏦 Tax Estimator Dashboard")
st.caption(f"U.S. federal income tax estimate · IRS {TAX_YEAR} single-filer brackets · "
           "for illustration only, not tax advice.")

# ---------------- Estimate form ----------------
with st.form("estimate_form"):
    name = st.text_input("Full name", placeholder="Jane Doe").strip()
    salary = st.number_input("Annual salary ($)", min_value=0.0, value=50000.0, step=1000.0)
    deductions = st.number_input("Deductions ($)", min_value=0.0, value=5000.0, step=500.0)
    submitted = st.form_submit_button("Calculate Tax")

if submitted:
    if salary <= 0:
        st.error("Please enter an annual salary greater than zero.")
    else:
        result = estimate(salary, deductions)
        customer_id = str(uuid.uuid4())[:8]

        data = load_data()
        new_entry = pd.DataFrame([{
            "Customer ID": customer_id,
            "Name": name or "—",
            "Salary": result["salary"],
            "Deductions": result["deductions"],
            "Taxable Income": result["taxable_income"],
            "Tax Payable": result["tax_payable"],
            "Net Salary": result["net_salary"],
            "Tax Year": result["tax_year"],
        }])
        save_data(pd.concat([data, new_entry], ignore_index=True))

        st.subheader("📊 Tax Breakdown")
        st.info(f"**Customer ID:** `{customer_id}` — keep this to delete your record later.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Tax payable", f"${result['tax_payable']:,.2f}")
        col2.metric("Net salary after tax", f"${result['net_salary']:,.2f}")
        col3.metric("Effective tax rate", f"{result['effective_rate'] * 100:.2f}%")

        st.write(f"**Annual salary:** ${result['salary']:,.2f}")
        st.write(f"**Deductions:** ${result['deductions']:,.2f}")
        st.write(f"**Taxable income:** ${result['taxable_income']:,.2f}")
        st.write(f"**Marginal rate:** {result['marginal_rate'] * 100:.0f}% "
                 "(rate on your last dollar of income)")

        # Pie: tax vs take-home (skip when there is nothing to split)
        if result["tax_payable"] > 0 or result["net_salary"] > 0:
            fig, ax = plt.subplots()
            ax.pie(
                [result["tax_payable"], result["net_salary"]],
                labels=["Tax payable", "Net salary"],
                autopct="%1.1f%%",
                colors=["#ef4444", "#10b981"],
                startangle=90,
            )
            ax.axis("equal")
            st.pyplot(fig)
            plt.close(fig)

        # How the tax was built up, bracket by bracket
        with st.expander("See bracket-by-bracket breakdown"):
            rows = []
            lower = 0.0
            for upper, rate in TAX_BRACKETS_2024_SINGLE:
                if result["taxable_income"] <= lower:
                    break
                portion = min(result["taxable_income"], upper) - lower
                rows.append({
                    "Bracket": f"${lower:,.0f} – "
                               f"{('$' + f'{upper:,.0f}') if upper != float('inf') else '∞'}",
                    "Rate": f"{rate * 100:.0f}%",
                    "Taxed amount": f"${portion:,.2f}",
                    "Tax": f"${portion * rate:,.2f}",
                })
                lower = upper
            st.table(pd.DataFrame(rows))

st.divider()

# ---------------- Saved estimates ----------------
st.subheader("💾 Saved Estimates")
saved = load_data()
if saved.empty:
    st.caption("No estimates saved yet.")
else:
    st.dataframe(saved, use_container_width=True, hide_index=True)

st.divider()

# ---------------- Delete ----------------
st.subheader("🗑️ Delete Your Data")
delete_id = st.text_input("Enter your Customer ID", placeholder="e.g. a1b2c3d4").strip()
if st.button("Delete"):
    data = load_data()
    if not delete_id:
        st.error("Please enter a Customer ID.")
    elif delete_id in data["Customer ID"].values:
        save_data(data[data["Customer ID"] != delete_id])
        st.success("✅ Record deleted successfully.")
        st.rerun()
    else:
        st.error("❌ Customer ID not found.")
