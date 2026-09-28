"""Pure tax-calculation logic for the Tax Estimator Dashboard.

Kept free of any Streamlit dependency so it can be unit-tested in isolation.
Brackets below are the IRS 2024 federal income tax brackets for single filers.
"""

# (upper bound of bracket, marginal rate). Final bracket is unbounded.
TAX_BRACKETS_2024_SINGLE = [
    (11_600, 0.10),
    (47_150, 0.12),
    (100_525, 0.22),
    (191_950, 0.24),
    (243_725, 0.32),
    (609_350, 0.35),
    (float("inf"), 0.37),
]

TAX_YEAR = 2024
FILING_STATUS = "single"


def calculate_tax(taxable_income: float) -> float:
    """Marginal tax on taxable income using 2024 single-filer brackets."""
    if taxable_income <= 0:
        return 0.0

    tax = 0.0
    lower = 0.0
    for upper, rate in TAX_BRACKETS_2024_SINGLE:
        if taxable_income <= lower:
            break
        tax += (min(taxable_income, upper) - lower) * rate
        lower = upper

    return round(tax, 2)


def marginal_rate(taxable_income: float) -> float:
    """The marginal rate that applies to the last dollar of income."""
    if taxable_income <= 0:
        return 0.0
    for upper, rate in TAX_BRACKETS_2024_SINGLE:
        if taxable_income <= upper:
            return rate
    return TAX_BRACKETS_2024_SINGLE[-1][1]


def effective_rate(taxable_income: float, tax: float) -> float:
    """Average rate actually paid (0 when there is no taxable income)."""
    if taxable_income <= 0:
        return 0.0
    return round(tax / taxable_income, 4)


def estimate(salary: float, deductions: float) -> dict:
    """Full estimate for a given salary and deductions.

    Deductions reduce taxable income (never below zero); take-home pay is
    salary minus the tax owed.
    """
    salary = max(0.0, float(salary))
    deductions = max(0.0, float(deductions))

    taxable_income = max(0.0, round(salary - deductions, 2))
    tax = calculate_tax(taxable_income)
    net_salary = round(salary - tax, 2)

    return {
        "salary": round(salary, 2),
        "deductions": round(deductions, 2),
        "taxable_income": taxable_income,
        "tax_payable": tax,
        "net_salary": net_salary,
        "marginal_rate": marginal_rate(taxable_income),
        "effective_rate": effective_rate(taxable_income, tax),
        "tax_year": TAX_YEAR,
        "filing_status": FILING_STATUS,
    }
