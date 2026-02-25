"""
DS3500 Practical Exam 2 - Starter Code
ShopSmart E-commerce Customer Analytics

This file loads and processes customer journey data.
You will add your visualization in the designated section.
"""
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Global constants
DATA_FILE = 'data.csv'

# Column names
CUSTOMER_ID_COL = 'customer_id'
AGE_COL = 'age'
LOCATION_COL = 'location'
DEVICE_TYPE_COL = 'device_type'
SESSION_DURATION_COL = 'session_duration'
ITEMS_VIEWED_COL = 'items_viewed'
CART_VALUE_COL = 'cart_value'
STAGE_COL = 'stage'
CUSTOMER_SEGMENT_COL = 'customer_segment'
DAYS_SINCE_SIGNUP_COL = 'days_since_signup'
MARKETING_SOURCE_COL = 'marketing_source'
PROMO_CODE_USED_COL = 'promo_code_used'
ABANDONED_CART_EMAILS_COL = 'abandoned_cart_emails_sent'

# Categorical orderings
STAGE_ORDER = ['Browse', 'Add to Cart', 'Checkout Started',
               'Purchase Complete', 'Review Left']
DEVICE_TYPE_ORDER = ['Mobile', 'Desktop', 'Tablet']
SEGMENT_ORDER = ['New', 'Returning', 'VIP']


def load_data(filepath):
    """
    Load the e-commerce customer journey dataset.
    """
    df = pd.read_csv(filepath)
    return df


def clean_data(df):
    """
    Clean and prepare the customer journey data for analysis.
    """
    # Make a copy to avoid modifying original
    df_clean = df.copy()

    # Ensure categorical columns have proper ordering
    df_clean[STAGE_COL] = pd.Categorical(df_clean[STAGE_COL],
                                         categories=STAGE_ORDER,
                                         ordered=True)

    df_clean[DEVICE_TYPE_COL] = pd.Categorical(df_clean[DEVICE_TYPE_COL],
                                               categories=DEVICE_TYPE_ORDER,
                                               ordered=False)

    df_clean[CUSTOMER_SEGMENT_COL] = pd.Categorical(df_clean[CUSTOMER_SEGMENT_COL],
                                                    categories=SEGMENT_ORDER,
                                                    ordered=True)

    # Ensure numeric columns are proper types
    df_clean[AGE_COL] = df_clean[AGE_COL].astype(int)
    df_clean[SESSION_DURATION_COL] = df_clean[SESSION_DURATION_COL].astype(float)
    df_clean[ITEMS_VIEWED_COL] = df_clean[ITEMS_VIEWED_COL].astype(int)
    df_clean[CART_VALUE_COL] = df_clean[CART_VALUE_COL].astype(float)
    df_clean[DAYS_SINCE_SIGNUP_COL] = df_clean[DAYS_SINCE_SIGNUP_COL].astype(int)
    df_clean[ABANDONED_CART_EMAILS_COL] = df_clean[ABANDONED_CART_EMAILS_COL].astype(int)

    # Ensure boolean column is proper type
    df_clean[PROMO_CODE_USED_COL] = df_clean[PROMO_CODE_USED_COL].astype(bool)

    # Remove any potential duplicates
    df_clean = df_clean.drop_duplicates(subset=[CUSTOMER_ID_COL])

    return df_clean

def create_visualization(df):
    """
    Create the required visualization.
    *** YOU WILL IMPLEMENT THIS FUNCTION DURING THE EXAM ***
    """
    pass

def main():
    # Load and clean the data
    df = load_data(DATA_FILE)
    df_clean = clean_data(df)

    # Create and display visualization
    fig = create_visualization(df_clean)

if __name__ == "__main__":
    main()