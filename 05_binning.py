"""
AdvanceDemonstrates: Binning, duplicates, merging, validation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# SECTION 1: CREATING NEW COLUMNS WITH BINNING
# =============================================================================

def demo_binning(df):
    """
    Create bins for cost_avg -- custom boundaries AND quantile-based bins
    """

# =============================================================================
# SECTION 2: JOINING & MERGING DATAFRAMES
# =============================================================================

def demo_concat_vertical():
    """
    Demonstrate pd.concat() for vertical stacking

    """

def random_sample(df, n):
    """Utility function-- return a sample of random data points
    from the data frame"""
    return df.sample(n=n)

def demo_concat_pattern(df):
    """
    Useful pattern for looping through pages of data, collecting the dataframes
    together.
    """

def demo_merge_basics():
    """
    Demonstrate merging-- outer, inner, left, right
    """
    states = pd.DataFrame({
        "state": ["MA", "CA", "NY", "TX"],
        "income": [67000, 80000, 88000, 54000],
        "population": [2000000, 60000000, 12000000, 45000000]
    })

# =============================================================================
# SECTION 3: DUPLICATE DETECTION & HANDLING
# =============================================================================

def demo_duplicates(df):
    """
    Detect and remove duplicates
    """


# =============================================================================
# SECTION 4: DATA VALIDATION
# =============================================================================
def validate_college_data(df):
    """
    Assertion-based validation - stops if something wrong
    Assert:
    1. Required columns exist
    2. No missing in critical columns
    3. Value ranges correct (admission_rate in [0,1], enrollment > 0)
    4. No duplicates
    5. Data types correct

    Raises AssertionError if any check fails
    """

# =============================================================================
# STUDENT EXERCISES
# =============================================================================

def exercise_1_binning(df):
    """
    Task: Create 'size_category' column using pd.cut()

    Use enrollment column with bins:
    - Small: 0-5000
    - Medium: 5000-15000
    - Large: 15000+

    Return: Series with size categories
    """
    # TODO: Your code here
    pass


def exercise_2_quantiles(df):
    """
    Task: Create 'earnings_tier' using pd.qcut()

    Split median_earnings_10yr into 4 equal groups (quartiles)
    Labels: ['Low', 'Medium', 'High', 'Very High']

    Return: Series with earnings tiers
    """
    # TODO: Your code here
    pass


def exercise_3_merge(df):
    """
    Task: Merge college data with region data

    Create a DataFrame with state-to-region mapping:
    - MA, NY, CT → Northeast
    - CA, OR, WA → West
    - TX, FL → South

    Merge with df using left join on 'state'

    Return: Merged DataFrame with new 'region' column
    """
    # TODO: Your code here
    pass

# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    # Load data
    df = pd.read_csv('data/college_scorecard_subset.csv')

    # Binning
    # demo_binning(df)

    # Duplicates
    # demo_duplicates(demo_concat_pattern(df))

    # Merging
    # demo_concat_vertical()
    # demo_concat_pattern()
    # demo_merge_basics()

    # Validation
    # validate_college_data(df)
