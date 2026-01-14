"""
Data Cleaning Fundamentals
Imputation and Outlier Detection
Rush's Notebook
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PATH_TO_FILE = "data/college-scorecard.csv"

# =============================================================================
# DEMO 1: Missing Data Detection
# =============================================================================
def demo_missing_detection(df):
    """
    Detect missing data through summaries and visualizations.
    """

# =============================================================================
# DEMO 2: Missing Data Strategies
# =============================================================================

def demo_drop_strategies(df):
    """
    Demonstrate dropping strategies for missing data
    """


def demo_fill_strategies(df):
    """
    Demonstrate filling strategies for missing data. Remember folks, you can
    do imputation with constants, statistical measures, forward/backward fills,
    or group-based values.
    """

# =============================================================================
# DEMO 3: Identifying Unusual Values
# =============================================================================

def identify_unusual_schools(df, column):
    """
    Identify statistically unusual schools using IQR method (there is also a
    standard deviation approach, called the z-score method).

    Args:
        df: College DataFrame
        column: Column to analyze

    Returns:
        DataFrame of unusual schools
    """


# =============================================================================
# DEMO 4: Analysis Decisions with Unusual Cases
# =============================================================================

def analyze_all_schools(df):
    """
    Analysis including all schools (including most selective)
    """

def analyze_accessible_schools(df, max_selectivity=0.30):
    """
    Analysis excluding most selective schools
    Focus on colleges accessible to typical students

    Args:
        df: College DataFrame
        max_selectivity: Maximum selectivity threshold
    """


# =============================================================================
# STUDENT EXERCISES
# =============================================================================

def exercise_1_utility(df):
    """Create a reusable missing data summary function. This can be really useful
    as a utility function! Have it be something where you can use this function
    for a quick glimpse as well as a detailed breakdown on the missing data in
    a dataset."""

    pass

def exercise_2_identify_unusual(df):
    """Identify outlier school based on other variables."""
    pass


def exercise_3_analysis_decision(df):
    """Compare analyses with and without selective schools. Produce a plot
    where both correlations are visible."""
    pass


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    # Load data
    df = pd.read_csv(PATH_TO_FILE)

    print("="*60)
    print("DATA CLEANING FUNDAMENTALS")
    print("="*60)
    print()

    # DEMO 1: Missing Data
    # demo_missing_detection(df)
    # df_dropped = demo_drop_strategies(df)
    # df_filled = demo_fill_strategies(df)

    # DEMO 2: Unusual Values
    # selective = identify_unusual_schools(df, 'admission_rate')

    # DEMO 3: Analysis Decisions
    # analyze_all_schools(df)
    # analyze_accessible_schools(df, max_selectivity=0.30)
