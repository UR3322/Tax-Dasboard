# 🏦 Tax Estimator Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)

A Streamlit dashboard that estimates U.S. federal income tax from an annual
salary and deductions, using the **IRS 2024 single-filer brackets** with a
proper marginal-rate calculation. Estimates are saved locally to a CSV file —
each record gets a unique **Customer ID** that can later be used to delete it.

> For illustration only — not tax advice.

## ✨ Features

- **Tax estimation form** — salary, deductions, and name
- **Correct marginal tax math** — bracket-by-bracket breakdown with an expandable
  view showing exactly how the tax was computed
- **Key metrics** — tax payable, net salary, effective tax rate, marginal rate
- **Visual breakdown** — pie chart of tax vs. take-home pay
- **Saved estimates** — every calculation stored in `customer_data.csv` and
  listed in a table
- **Delete by Customer ID** — remove your own record at any time
- **Tested core logic** — 21 assertions covering every bracket boundary
  (`python tests/test_tax.py`)

## 🛠️ Installation

```bash
git clone https://github.com/UR3322/Tax-Dasboard.git
cd Tax-Dasboard

pip install -r requirements.txt
```

## ▶️ Run

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

### Run the tests

```bash
python tests/test_tax.py
```

## 📁 Project structure

```
├── app.py              # Streamlit UI
├── tax_calculator.py   # Pure tax logic (no Streamlit dependency)
├── tests/
│   └── test_tax.py     # Bracket-boundary tests, plain asserts
├── requirements.txt
└── customer_data.csv   # Created at runtime; gitignored
```

## 📌 Technologies

- **Python** 🐍
- **Streamlit** 🎨
- **Pandas** 🗂️
- **Matplotlib** 📊

## 📜 License

MIT — see [LICENSE](LICENSE).

---

**Developed by: Abdul Samad Saleem & Muhammad Usman**
