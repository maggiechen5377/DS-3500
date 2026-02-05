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

    # collect all the unique src and target strings
    all_labels = pd.concat([df[src], df[targ]]).unique()

    # assign each one a number starting from 0

    # create a mapping (dict)
    labels = { }
    for i in range(len(all_labels)):
        labels[all_labels[i]] = i

    # update the src and targ columns in the df
    df[src] = df[src].map(lambda val: labels[val])
    df[targ] = df[targ].map(lambda val: labels[val])
    return df, labels


def make_sankey(df, src, targ, vals, **kwargs):
    """Generate a sankey diagram from dataframe.
    Talk about keyword args and positional args
    line_width : width of line for links
    """
    df, mapping = _code_mapping(df, src, targ)

    line_width = kwargs.get("line_width", None)

    link = {"source": df[src], "target": df[targ], "value": df[vals],
            "line": {"width": line_width}}
    node = {"label": list(mapping.keys())}
    fig = go.Figure(go.Sankey(link=link, node=node))
    # fig.show()
    return fig


def demo_wrapper_basic():
    """Using the wrapper with simple bio data: organ → gene"""
    bio = pd.read_csv('data/bio.csv')
    fig = make_sankey(bio, 'disease', 'gene', 'pubs')
    fig.show()

    bio2 = pd.read_csv('data/bio2.csv')
    fig = make_sankey(bio2, 'stage', 'organ', 'count',
                      line_width=1, orientation="v")
    fig.show()

def demo_multi_layer_stacking():
    """Multi-layer Sankey via dataframe stacking: stage → organ → gene.
    """
    bio = pd.read_csv('data/bio.csv')
    bio.columns = ["source", "target", "value"]
    bio2 = pd.read_csv('data/bio2.csv')
    bio2.columns = ["source", "target", "value"]
    combined = pd.concat([bio, bio2])

    fig = make_sankey(combined, "source", "target", "value")
    fig.show()

def practice_creating_sankey():
    '''Practice your own sankey diagram. Use the college dataset to study
    flow of students through the higher ed syste. You can use columns like
     selectivity (binned), college type (the control column is encoded already),
     and study earnings after college (binned). Great way to practice the
     entire pipeline of data cleaning/prep to creating summaries and then a
     Sankey diagram! '''


def main():
    # demo_wrapper_basic()
    demo_multi_layer_stacking()
    pass

if __name__ == '__main__':
    main()