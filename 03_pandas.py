"""
DS3500 - Lecture 3 Pandas Fundamentals
Demonstrates: DataFrames, loading data, selection, filtering, plotting
Rush's Notebook.
TODO: DO NOT CHANGE CODE IN PUBLIC REPO. COPY TO YOUR REPO!
command: cp <source> <destination>
documentation for command: https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html
TODO: Change name in this docstring on line 4 to your name.
"""

import pandas as pd
import matplotlib.pyplot as plt

PATH_TO_DATA = 'data/college-scorecard.csv'

# =============================================================================
# DEMO 1: Creating  and Loading DataFrames
# =============================================================================

def demo_create_dataframe():
    """Return a DataFrame created from scratch. This is simply a demo function
    to demonstrate how dataframes can be created from scratch. Useful for
    testing by creating a mock dataframe with only a couple of rows."""

def demo_load_data(csv_path):
    """Load the data from given path into a dataframe and return the dataframe.
    Folks, this is one line of code-- generally you won't create a function
    for something like this."""

# =============================================================================
# DEMO 2: Exploring Dataframes
# =============================================================================

def summarize_dataframe(df, opt = ""):
    """Utility function for quick summaries. You can do a variety of the following:
     shape, head, tail, sampling, columns, info, describe, dtypes. THIS IS SUPER
     HELPFUL! I suggest keeping this function in your pocket, handy for whenever you
     are working with a dataset. """
    if "describe" in opt:
        # example like this
        # print(df.describe().to_string())
        pass
    if "sample" in opt:
        pass
    if "info" in opt or not opt:
        pass

# =============================================================================
# DEMO 3: Column Selection and Operations
# =============================================================================

def demo_column_selection(df):
    """Different ways to select columns: single column, multiple columns,
    column operations, operator lifting."""

# =============================================================================
# DEMO 4: Row Filtering
# =============================================================================

def demo_filtering(df):
    """Boolean indexing and filtering.
    IMPORTANT: Must use & (and), | (or), ~ (not) - NOT Python's and, or, not
    IMPORTANT: Must use parentheses around each condition!"""

def find_schools(df, state, max_admission_rate):
    """Filter by state and below a certain
    admission rate."""

# =============================================================================
# DEMO 5: Quick Plotting
# =============================================================================

def demo_plotting(df):
    """Built-in pandas plotting for quick exploration. Class, pick one:
    - histogram for admission rate to understand (distribution)
    - scatter plot for admission rate vs median earnings (binary relationship)
    - bar chart for counts by state (top X states)
    """

# =============================================================================
# STUDENT EXERCISES
# =============================================================================

def exercise_1(df):
    """Get schools in California"""
    pass


def exercise_2(df):
    """Find large schools"""
    pass


def exercise_3(df):
    """Find affordable MA schools"""
    pass


def exercise_4_viz(df):
    """Plot enrollment vs cost"""
    pass


def exercise_5_challenge(df):
    """Filter NY schools and plot"""
    pass


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    # Load data -- this is how you generally load data (commented for this lecture)
    # df = pd.read_csv(PATH_TO_DATA)
    
    print("="*60)
    print("LECTURE 3: PANDAS FUNDAMENTALS")
    print("="*60)
    
    # Run demos (uncomment to run each)
    # print(demo_create_dataframe())
    # df = demo_load_data(PATH_TO_DATA)
    # summarize_dataframe(df, "describe")
    # demo_column_selection(df)
    # demo_filtering(df)
    # demo_plotting(df)
    # find_schools(df, "NY", 0.6)

    # Student exercises
    print("\nEXERCISES:")
    # ...