"""
Demonstrates: Binning, duplicates, merging, validation
Rush's Notebook
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# SECTION 1: CREATING NEW COLUMNS WITH BINNING
# =============================================================================

def demo_binning(df):
    """
    Create bins for avg cost -- custom boundaries AND quantile-based bins
    """
    df_binned = df.copy()
    print(df["avg_cost"].describe())

    # manual binning
    df_binned["avg_cost"] = pd.cut(df["avg_cost"],
           bins=[3000, 10000, 30000, 60000, 90000],
           labels=["low", "affordable", "pricey", "expensive"])

    print(df_binned["avg_cost"].value_counts())

    # quantile binning
    df_binned["avg_cost_binned_qt"] = pd.qcut(df["avg_cost"], 4,
                                   labels=["C1 (least expensive)", "C2",
                                           "C3", "C4 (most expensive)"])
    print(df_binned["avg_cost_binned_qt"].value_counts())



# =============================================================================
# SECTION 2: JOINING & MERGING DATAFRAMES
# =============================================================================

def random_sample(df, n):
    """Utility function-- return a sample of random data points
    from the data frame"""
    return df.sample(n=n)

def demo_concat_vertical(df):
    """
    Demonstrate pd.concat() for vertical stacking
    """
    df1 = random_sample(df, 30)
    df2 = random_sample(df, 30)

    df_combined = pd.concat([df1, df2],ignore_index=True)

    print(f"Shape of resulting df is {df_combined.shape}")
    print(df_combined.tail())

def demo_concat_pattern(df):
    """
    Useful pattern for looping through pages of data, collecting the dataframes
    together.
    """
    df_lst = []
    for x in range(20):
        # make a request for data
        df_lst.append(random_sample(df, 50))

    return pd.concat(df_lst, ignore_index=True)

def demo_merge_basics(df):
    """
    Demonstrate merging-- outer, inner, left, right
    """
    states = pd.DataFrame({
        "state": ["MA", "CA", "NY", "TX"],
        "income": [67000, 80000, 88000, 54000],
        "population": [2000000, 60000000, 12000000, 45000000]
    })

    df_merged = pd.merge(df, states, how="inner", on="state")
    print(f"Merged df has shape {df_merged.shape}")
    print(df_merged[["name", "state", "income"]])

    df_merged = pd.merge(df, states, how="left", on="state")
    print(f"Merged df has shape {df_merged.shape}")
    print(df_merged[["name", "state", "income"]])


# =============================================================================
# SECTION 3: DUPLICATE DETECTION & HANDLING
# =============================================================================

def demo_duplicates(df):
    """
    Detect and remove duplicates
    """
    print(f"Number of duplicates is {df.duplicated().sum()}")

    print(f"Number of duplicates when searching by name is "
          f"{df.duplicated(subset=["name"]).sum()}")

    # to view duplicates, use this as a mask
    print(df[df.duplicated(subset=["name"])]["name"].to_string())


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

    # making sure critical columns are not nan
    assert df[["name", "state"]].notna().all().all(), "Columns are empty!"

    # checking if adm rate in range
    assert (df["admission_rate"] > 0).all(), "Admission rate not above 0"


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
    df = pd.read_csv('data/college-scorecard.csv')

    # Binning
    demo_binning(df)

    # Merging
    demo_concat_vertical(df)
    df_sampled = demo_concat_pattern(df)
    # demo_merge_basics(df_sampled)

    # Duplicates
    demo_duplicates(df_sampled)

    # Validation
    validate_college_data(df)