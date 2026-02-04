"""
Introduction to Sankey Diagrams
Rush's Notebook.
TODO: copy over bio.csv from the data folder!
"""
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

# I'm keeping this commented,
# uncomment if you'd rather use browser
# for seeing the plots.
# pio.renderers.default = "browser"

BIO_DATA_PATH = "data/bio.csv"

def demo_minimal():
    """Minimal sankey: source nodes, target nodes, and values"""
    source = [0, 0, 1, 1]
    target = [2, 3, 2, 4]
    value = [1, 2, 1.5, 3]
    link = {"source": source, "target": target, "value": value}

    sk = go.Sankey(link=link)
    fig = go.Figure(sk)
    fig.show()

def demo_labels_styling():
    """Adding node labels and basic styling parameters (pad, thickness)"""
    s = [0, 0, 1, 1, 1, 2]
    t = [3, 4, 3, 3, 4, 3]
    v = [2, 1, 1, 1, 1, 1]

    link = {"source": s, "target": t, "value": v,
            'line': {'color': 'black' , 'width': 0.4}}
    node = {'label': ["A", "B", "C", "D", "E"],
            'pad': 5}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()

def demo_bidirectional():
    """Nodes as both sources and targets, with link and node line styling"""



def demo_colors_customization():
    """Advanced customization: individual link colors, node colors, and titles"""
    source = [2, 0, 0, 0, 1]
    target = [5, 3, 4, 5, 4]
    value = [10000, 40000, 20000, 20000, 2000]
    labels = ["Teaching", "Dogsitting", "Investments",
              "Living Expenses", "Wants", "Savings"]

    color_links = ["gainsboro"] * 5
    color_links[0] = "seagreen"


    link = {"source": source, "target": target, "value": value,
            'color':color_links}
    node = {"label": labels}

    fig = go.Figure(go.Sankey(node=node, link=link))
    fig.show()



def demo_string_problem():
    """Plotly requires integer node identifiers, not string labels"""

    # This doesn't work - plotly sankey expects integer node identifiers
    # Distinct labels occurring in the source and target
    # columns need to be mapped to integer codes 0...(n-1)
    df = pd.read_csv('data/bio.csv')

    # But this will work - values have been pre-encoded as numbers!
    # df = pd.read_csv('data/bio_encoded.csv')

    link = {'source': df.source, 'target': df.target, 'value': df.value,}
    node = {'label': ['?'] * 6}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()


def main():
    # demo_minimal()
    # demo_labels_styling()
    # demo_bidirectional()
    demo_colors_customization()
    # demo5_string_problem()  # Uncomment to show the error!


if __name__ == '__main__':
    main()