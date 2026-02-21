import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# color palette
PRIMARY_COLOR = "#E63946"
BG_COLOR = "#f9f9f9"
FONT_COLOR = "#333333"


# animated map

def make_animated_choropleth(all_years_df: pd.DataFrame, disease: str):
    """
    Create an animated choropleth world map with a built-in Play/Pause button
    and year slider inside the Plotly figure itself.
    User can press play or drag the slider directly on the chart — this is the dynamic visualization.
    """
    fig = px.choropleth(
        all_years_df,
        locations="Code",
        color="Deaths",
        hover_name="Country",
        animation_frame="Year",
        color_continuous_scale="Reds",
        range_color=[0, all_years_df["Deaths"].quantile(0.95)],
        title=f"<b>{disease}</b> — Deaths Worldwide (1990–2019)",
        labels={"Deaths": "Deaths"},)

    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        geo=dict(bgcolor=BG_COLOR, showframe=False, showcoastlines=True),
        coloraxis_colorbar=dict(title="Deaths"),
        margin=dict(l=0, r=0, t=50, b=20),
        font=dict(color=FONT_COLOR),
        title_font_size=16,
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            y=-0.08,
            x=0.5,
            xanchor="center",
            buttons=[
                dict(label="▶ Play", method="animate",
                     args=[None, {"frame": {"duration": 400, "redraw": True}, "fromcurrent": True}]),
                dict(label="⏸ Pause", method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]),])])
    return fig


# top 10 bar chart

def make_top_bar(top_df: pd.DataFrame, disease: str, year: int):
    """
    Horizontal bar chart of top 10 countries by deaths.
    """
    fig = px.bar(
        top_df.sort_values("Deaths"),
        x="Deaths",
        y="Country",
        orientation="h",
        title=f"Top 10 Countries — {disease} ({year})",
        color="Deaths",
        color_continuous_scale="Reds",
        labels={"Deaths": "Deaths", "Country": ""},)

    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=50, b=10),
        font=dict(color=FONT_COLOR),
        title_font_size=14,)
    return fig


# trend line chart

def make_trend_chart(trend_df: pd.DataFrame, disease: str, countries: list):
    """
    Line chart showing death trends over time for selected countries.
    """
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


# disease breakdown

def make_disease_breakdown(breakdown_df: pd.DataFrame, country: str, year: int):
    """
    Horizontal bar chart of all diseases for a single country/year.
    Shows top 15 causes only for readability.
    """
    top15 = breakdown_df.head(15)
    fig = px.bar(
        top15.sort_values("Deaths"),
        x="Deaths",
        y="Disease",
        orientation="h",
        title=f"All Causes of Death — {country} ({year})",
        color="Deaths",
        color_continuous_scale="Blues",)

    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=50, b=10),
        font=dict(color=FONT_COLOR),
        title_font_size=14,
        height=500,)
    return fig


# sunburst chart

def make_sunburst(sunburst_df: pd.DataFrame, year: int):
    """
    Clickable sunburst chart: World → Region → Country → Disease.
    Click any segment to drill down, click the center to zoom back out.
    """
    fig = px.sunburst(
        sunburst_df,
        path=["Region", "Country", "Disease"],
        values="Deaths",
        color="Deaths",
        color_continuous_scale="Reds",
        title=f"<b>Causes of Death by Region → Country → Disease ({year})</b>",
        maxdepth=2,)

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Deaths: %{value:,}<br>% of parent: %{percentParent:.1%}<extra></extra>",
        insidetextorientation="radial",)

    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        margin=dict(l=0, r=0, t=60, b=0),
        font=dict(color=FONT_COLOR),
        title_font_size=15,
        coloraxis_colorbar=dict(title="Deaths"),
        height=580,)
    return fig