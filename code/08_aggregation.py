"""
Grouping Review, Pivot Tables, Windowing
ONLINE LECTURE - This is going to be more of a workbook.
Dataset: data/air_quality.csv
- 3 Boston neighborhoods: Roxbury, Kenmore Sq, South Boston
- 8 pollutant sensors (CO, NO, NO2, NOx, O3, PM10, PM2.5, SO2)
- 23 days of measurements (January 2026)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load_data(filepath='air_quality.csv'):
    """
    Load and prepare the air quality dataset
    """
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])

    return df


###############################################################################
# PART 1: GROUPING  AND PIVOT TABLES
###############################################################################

def demo_basic_groupby(df):
    """
    Use groupby to calculate this:
    Q: What's the average pollution per neighborhood?
    """


def demo_multi_groupby(df):
    """
    Use groupby to answer this:
    Q: What if I want BOTH neighborhood AND sensor?
    This creates the "hard to read" problem that pivot solves.
    """

def demo_pivot_basic(df):
    """
    Q: For Roxbury only, show mean readings for all sensors.
    """


def demo_pivot_sensors(df):
    """
        Use a pivot table to answer this:
        Q: Compare PM2.5 levels across neighborhoods over time
        Shows LONG vs WIDE format
    """


###############################################################################
# WINDOWING
###############################################################################

def demo_rolling_basic(df):
    """
    Try computing the rolling 3-day averages for Roxbury's PM2.5 data
    and plotting it.
    """

if __name__ == '__main__':
    # Load data
    df = load_data("data/air_quality.csv")

    # Grouping and Pivot tables
    # demo_basic_groupby(df)
    # demo_multi_groupby(df)
    #
    # demo_pivot_basic(df)
    # demo_pivot_sensors(df)

    # Windowing
    # demo_rolling_basic(df)



