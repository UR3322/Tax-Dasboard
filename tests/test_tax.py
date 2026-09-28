"""Tests for tax_calculator.py. Run with: python tests/test_tax.py

Uses plain asserts so no test runner dependency is required.
Expected values cross-checked against the IRS 2024 single-filer brackets:
  10% to $11,600 · 12% to $47,150 · 22% to $100,525 · 24% to $191,950 ·
  32% to $243,725 · 35% to $609,350 · 37% above.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tax_calculator import calculate_tax, marginal_rate, effective_rate, estimate


def check(actual, expected, label):
    assert actual == expected, f"{label}: expected {expected}, got {actual}"
    print(f"  ok - {label}")


print("calculate_tax")
check(calculate_tax(0), 0.0, "zero income -> zero tax")
check(calculate_tax(-5000), 0.0, "negative income -> zero tax")
check(calculate_tax(11_600), 1_160.0, "top of 10% bracket")
# 1,160 + 35,550 * 0.12 = 5,426
check(calculate_tax(47_150), 5_426.0, "top of 12% bracket")
# 5,426 + 2,850 * 0.22 = 6,053
check(calculate_tax(50_000), 6_053.0, "$50k income")
# 5,426 + 53,375 * 0.22 = 17,168.5
check(calculate_tax(100_525), 17_168.5, "top of 22% bracket")
# 17,168.5 + 91,425 * 0.24 = 39,110.5
check(calculate_tax(191_950), 39_110.5, "top of 24% bracket")
# spot-check deep into the 37% bracket: 183,647.25 at $609,350
# + 90,650 * 0.37 = 33,540.50 -> 217,187.75
check(calculate_tax(700_000), 217_187.75, "$700k income (37% bracket)")

print("marginal_rate")
check(marginal_rate(0), 0.0, "zero income")
check(marginal_rate(11_600), 0.10, "boundary stays in lower bracket")
check(marginal_rate(11_601), 0.12, "just above boundary")
check(marginal_rate(1_000_000), 0.37, "top bracket")

print("effective_rate")
check(effective_rate(0, 0), 0.0, "zero income -> zero rate")
check(effective_rate(50_000, 6_053.0), 0.1211, "$50k effective rate")

print("estimate")
r = estimate(50_000, 5_000)
check(r["taxable_income"], 45_000.0, "deductions reduce taxable income")
# 1,160 + 33,400 * 0.12 = 5,168
check(r["tax_payable"], 5_168.0, "tax on $45k taxable")
check(r["net_salary"], 44_832.0, "take-home = salary - tax")
check(r["marginal_rate"], 0.12, "marginal rate at $45k")
r2 = estimate(30_000, 40_000)
check(r2["taxable_income"], 0.0, "deductions floored at zero taxable")
check(r2["tax_payable"], 0.0, "no tax when deductions exceed salary")
print("ALL TESTS PASSED")
