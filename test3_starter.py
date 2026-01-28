"""
DS3500 Practical Exam 1 - Version 3
City Employee Salaries
Name: _________________
Date: _________________
"""

import pandas as pd
import json


def load_and_clean_salaries(filepath):
    """Load and clean employee salary data from JSON."""
    data = json.load(open(filepath))
    pass


def calculate_median_salary_by_department(df):
    """Calculate median salary by department."""
    pass


# ============================================
# TEST CODE - DO NOT MODIFY
# ============================================
if __name__ == '__main__':
    print("Loading and cleaning data...")
    df = load_and_clean_salaries('employee_salaries.json')

    assert isinstance(df, pd.DataFrame), "Must return a DataFrame"
    assert len(df) > 0, "DataFrame should not be empty"
    assert 'annual_salary' in df.columns, "Must have annual_salary column"
    assert df['annual_salary'].notna().all(), "No null salaries allowed"
    assert (df['annual_salary'] > 0).all(), "All salaries must be > 0"
    print(f"✓ Loaded {len(df)} valid employees")

    # clean up data
    df["department"] = df["department"].str.title()

    print("\nCalculating median salaries by department...")
    median_salaries = calculate_median_salary_by_department(df)

    assert isinstance(median_salaries, pd.Series), "Must return a Series"
    assert len(median_salaries) > 0, "Results should not be empty"
    assert (median_salaries > 0).all(), "All median salaries must be positive"
    print(f"✓ Calculated median salaries for {len(median_salaries)} departments")

    print("\n" + "=" * 50)
    print("MEDIAN SALARIES BY DEPARTMENT")
    print("=" * 50)
    print(median_salaries.sort_values(ascending=False).to_string())

    print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")