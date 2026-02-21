import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# Color Palette
BG_COLOR = "#f9f9f9"
FONT_COLOR = "#333333"


# Tab 1: Choropleth Map

def make_choropleth(map_df: pd.DataFrame, disease: str, year: int):
    """Static choropleth world map for a given disease and year."""
    fig = px.choropleth(
        map_df,
        locations="Code",
        color="Deaths",
        hover_name="Country",
        color_continuous_scale="Reds",
        title=f"<b>{disease}</b> — Deaths Worldwide ({year})",
        labels={"Deaths": "Deaths"},)
    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        geo=dict(bgcolor=BG_COLOR, showframe=False, showcoastlines=True),
        coloraxis_colorbar=dict(title="Deaths"),
        margin=dict(l=0, r=0, t=50, b=0),
        font=dict(color=FONT_COLOR),
        title_font_size=16,)
    return fig


# Tab 2: Trend Line Chart

def make_trend_chart(trend_df: pd.DataFrame, disease: str, countries: list):
    """Line chart showing death trends over time for selected countries."""
    if trend_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Select at least one country", showarrow=False,
                           font=dict(size=14, color="gray"), xref="paper", yref="paper", x=0.5, y=0.5)
    else:
        fig = px.line(
            trend_df,
            x="Year",
            y="Deaths",
            color="Country",
            title=f"<b>{disease}</b> — Death Trend Over Time",
            markers=True,)
    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=10, r=10, t=50, b=10),
        font=dict(color=FONT_COLOR),
        title_font_size=14,
        legend_title_text="Country",)
    return fig


# Tab 3: Sunburst Chart

def make_sunburst(sunburst_df: pd.DataFrame, year: int):
    """
    Clickable sunburst chart: Region → Country → Disease.
    Click any segment to drill down. Click the center to zoom back out.
    """
    fig = px.sunburst(
        sunburst_df,
        path=["Region", "Country", "Disease"],
        values="Deaths",
        color="Deaths",
        color_continuous_scale="Reds",
        title=f"<b>Causes of Death by Region → Country → Disease ({year})</b>",)
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Deaths: %{value:,}<br>% of parent: %{percentParent:.1%}<extra></extra>",
        insidetextorientation="radial",
    )
    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        margin=dict(l=0, r=0, t=60, b=0),
        font=dict(color=FONT_COLOR),
        title_font_size=15,
        coloraxis_colorbar=dict(title="Deaths"),
        height=580,)
    return fig