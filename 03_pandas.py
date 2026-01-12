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
    return pd.DataFrame({
        "name": ["Rush", "Calvin", "Anushka", "Anya"],
        "age": [25, 20, 29, 29],
        "major": ["comp sci", "env engn", "data sci + psych", "data sci"]
    })


def demo_load_data(csv_path):
    """Load the data from given path into a dataframe and return the dataframe.
    Folks, this is one line of code-- generally you won't create a function
    for something like this."""
    return pd.read_csv(csv_path)


# =============================================================================
# DEMO 2: Exploring Dataframes
# =============================================================================

def summarize_dataframe(df, opt=""):
    """Utility function for quick summaries. You can do a variety of the following:
     shape, head, tail, sampling, columns, info, describe, dtypes. THIS IS SUPER
     HELPFUL! I suggest keeping this function in your pocket, handy for whenever you
     are working with a dataset. """
    if "describe" in opt:
        # example like this
        print(df.describe().to_string())
    if "shape" in opt:
        print(df.shape)
    if "sample" in opt:
        print(df.sample(n=5))
    if "info" in opt or not opt:
        df.info()


# =============================================================================
# DEMO 3: Column Selection and Operations
# =============================================================================

def demo_column_selection(df):
    """Different ways to select columns: single column, multiple columns,
    column operations, operator lifting."""
    print(df["city"].value_counts())
    print(df[["name", "state", "admission_rate"]])
    # print((df["tuition_in_state"] + df["tuition_out_state"]) / 2)
    df["tuition_in_state"] + 10


# =============================================================================
# DEMO 4: Row Filtering
# =============================================================================

def demo_filtering(df):
    """Boolean indexing and filtering.
    IMPORTANT: Must use & (and), | (or), ~ (not) - NOT Python's and, or, not
    IMPORTANT: Must use parentheses around each condition!"""
    mask = df["avg_cost"] > 30000
    # print(df[mask])

    print(df[(df["state"] == "NY") & (df["avg_cost"] > 30000)])


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
    df.plot.scatter(x="median_earnings_10yr", y="admission_rate")


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

    print("=" * 60)
    print("LECTURE 3: PANDAS FUNDAMENTALS")
    print("=" * 60)

    # Run demos (uncomment to run each)
    print(demo_create_dataframe())
    df = demo_load_data(PATH_TO_DATA)
    # print(df)
    summarize_dataframe(df, "sample-shape-info")
    # demo_column_selection(df)
    # demo_filtering(df)
    demo_plotting(df)
    # find_schools(df, "NY", 0.6)
    plt.show()

    # Student exercises
    print("\nEXERCISES:")
    # ...