"""
Lecture 2: Reusable Sankey Components & Multi-Layer Visualization
Building wrapper functions and dataframe stacking techniques
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# pio.renderers.default = "browser"


def _code_mapping(df, src, targ):
    """Map labels in src and targ columns to integers.
    Return the df and labels
    Talk about internal/helper functions."""


def make_sankey(df, src, targ, vals, **kwargs):
    """Generate a sankey diagram from dataframe.
    Talk about keyword args and positional args"""


def demo_wrapper_basic():
    """Using the wrapper with simple bio data: organ → gene"""
    bio = pd.read_csv('data/bio.csv')
    make_sankey(bio, 'disease', 'gene', 'pubs')


def demo_multi_layer_stacking():
    """Multi-layer Sankey via dataframe stacking: stage → organ → gene.
    """

def practice_creating_sankey():
    '''Practice your own sankey diagram. Use the college dataset to study
    flow of students through the higher ed syste. You can use columns like
     selectivity (binned), college type (the control column is encoded already),
     and study earnings after college (binned). Great way to practice the
     entire pipeline of data cleaning/prep to creating summaries and then a
     Sankey diagram! '''


def main():
    # demo_wrapper_basic()
    # demo_multi_layer_stacking()
    pass

if __name__ == '__main__':
    main()