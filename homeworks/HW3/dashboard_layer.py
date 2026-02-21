import panel as pn
import api_layer as api
import viz_layer as viz

pn.extension("plotly", "tabulator")


# WIDGET BANK
years = api.get_years()
diseases = api.get_diseases()
countries = api.get_countries()

# Tab 1 — Animated World Map (no year slider needed, animation is inside the chart
map_disease_select = pn.widgets.Select(
    name="Disease / Cause of Death",
    value="Cardiovascular Diseases",
    options=diseases,
    width=280,)

# Tab 2 — Trend over time
trend_disease_select = pn.widgets.Select(
    name="Disease",
    value="Cardiovascular Diseases",
    options=diseases,
    width=280,)

country_multi = pn.widgets.MultiChoice(
    name="Select Countries (up to 6)",
    value=["United States", "China", "India"],
    options=countries,
    max_items=6,
    width=280,)

# Tab 3 — Sunburst
sunburst_year = pn.widgets.IntSlider(
    name="Year",
    start=1990,
    end=2019,
    value=2019,
    step=1,
    width=280,)

sunburst_top_n = pn.widgets.IntSlider(
    name="Top N Countries per Region",
    start=3,
    end=10,
    value=5,
    step=1,
    width=280,)

data_search_country = pn.widgets.Select(
    name="Filter by Country",
    value="All",
    options=["All"] + countries,
    width=280,)

data_search_disease = pn.widgets.Select(
    name="Filter by Disease",
    value="All",
    options=["All"] + diseases,
    width=280,)

# ─────────────────────────────────────────────
# REACTIVE CALLBACKS
# ─────────────────────────────────────────────

# Tab 1: Animated World Map

@pn.depends(map_disease_select)
def animated_map_plot(disease):
    all_df = api.get_all_years_data(disease)
    return pn.pane.Plotly(viz.make_animated_choropleth(all_df, disease), height=500, sizing_mode="stretch_width")

@pn.depends(map_disease_select)
def map_summary_card(disease):
    # Show stats for the most recent year
    stats = api.get_summary_stats(disease, 2019)
    return pn.pane.Markdown(f"""
### 📊 Quick Stats — 2019
| Metric | Value |
|---|---|
| **Total Deaths Worldwide** | {stats['total']:,} |
| **Average per Country** | {stats['mean']:,} |
| **Highest Burden Country** | {stats['max_country']} |
| **Deaths in Top Country** | {stats['max_deaths']:,} |
""", width=280)


# Tab 2: Trend Over Time

@pn.depends(trend_disease_select, country_multi)
def trend_plot(disease, countries):
    trend_df = api.get_trend_data(disease, countries)
    return pn.pane.Plotly(viz.make_trend_chart(trend_df, disease, countries), height=450, sizing_mode="stretch_width")

@pn.depends(trend_disease_select, country_multi)
def top_bar_plot(disease, countries):
    top_df = api.get_top_countries(disease, 2019, n=10)
    return pn.pane.Plotly(viz.make_top_bar(top_df, disease, 2019), height=360, sizing_mode="stretch_width")


# Tab 3: Sunburst

reset_button = pn.widgets.Button(name="↺ Reset View", button_type="primary", width=280)
reset_counter = pn.widgets.IntInput(value=0, visible=False)

def on_reset(event):
    reset_counter.value += 1

reset_button.on_click(on_reset)

@pn.depends(sunburst_year, sunburst_top_n, reset_counter)
def sunburst_plot(year, top_n, _counter):
    sb_df = api.get_sunburst_data(year, top_n)
    return pn.pane.Plotly(viz.make_sunburst(sb_df, year), height=600, sizing_mode="stretch_width")


# Tab 4: Raw Data

@pn.depends(data_search_country, data_search_disease)
def raw_data_table(country, disease):
    df = api.load_data().copy()
    if country != "All":
        df = df[df["Country"] == country]
    cols = ["Country", "Code", "Year"]
    if disease != "All":
        cols += [disease]
    else:
        cols += api.get_diseases()
    return pn.widgets.Tabulator(
        df[cols].reset_index(drop=True),
        pagination="remote",
        page_size=20,
        sizing_mode="stretch_width",
        height=500,)


# LAYOUT

header = pn.pane.Markdown(
    "# 🌍 Global Causes of Death Dashboard\n"
    "*Explore death counts by disease, country, and year (1990–2019) — Source: Our World in Data*",
    sizing_mode="stretch_width",
    styles={"background": "#E63946", "color": "white", "padding": "16px 24px", "border-radius": "8px"},)

# Tab 1
tab1_controls = pn.Column(
    pn.pane.Markdown("### 🔧 Controls"),
    map_disease_select,
    pn.pane.Markdown(
        "_Press ▶ Play on the map to animate through 1990–2019, or drag the year slider inside the chart._",
        styles={"font-size": "12px", "color": "gray"},),
    pn.layout.Divider(),
    map_summary_card,
    width=300,
    styles={"background": "#f0f0f0", "padding": "16px", "border-radius": "8px"},)

tab1 = pn.Row(
    tab1_controls,
    pn.Column(animated_map_plot, sizing_mode="stretch_width"),
    sizing_mode="stretch_width",)

# Tab 2
tab2_controls = pn.Column(
    pn.pane.Markdown("### 🔧 Controls"),
    trend_disease_select,
    country_multi,
    pn.pane.Markdown(
        "_Select up to 6 countries to compare trends over time._",
        styles={"font-size": "12px", "color": "gray"},),
    width=300,
    styles={"background": "#f0f0f0", "padding": "16px", "border-radius": "8px"},)

tab2 = pn.Row(
    tab2_controls,
    pn.Column(trend_plot, sizing_mode="stretch_width"),
    sizing_mode="stretch_width",)

# Tab 3 — Sunburst layout
tab5_controls = pn.Column(
    pn.pane.Markdown("### 🔧 Controls"),
    sunburst_year,
    sunburst_top_n,
    reset_button,
    pn.pane.Markdown(
        "_Click any segment to drill down. Use ↺ Reset View to return to the top level._",
        styles={"font-size": "12px", "color": "gray"},),
    width=300,
    styles={"background": "#f0f0f0", "padding": "16px", "border-radius": "8px"},)

tab5 = pn.Row(
    tab5_controls,
    pn.Column(sunburst_plot, sizing_mode="stretch_width"),
    sizing_mode="stretch_width",)

# Tab 4
tab4_controls = pn.Column(
    pn.pane.Markdown("### 🔧 Filters"),
    data_search_country,
    data_search_disease,
    pn.pane.Markdown(
        "_Browse and filter the raw dataset. Pagination shows 20 rows at a time._",
        styles={"font-size": "12px", "color": "gray"},),
    width=300,
    styles={"background": "#f0f0f0", "padding": "16px", "border-radius": "8px"},)

tab4 = pn.Row(
    tab4_controls,
    pn.Column(raw_data_table, sizing_mode="stretch_width"),
    sizing_mode="stretch_width",)

# Tabs
tabs = pn.Tabs(
    ("🗺️ World Map Explorer", tab1),
    ("📈 Trend Over Time", tab2),
    ("🌐 Region Explorer", tab5),
    ("📋 Raw Data", tab4),
    sizing_mode="stretch_width",)

# Final layout
dashboard = pn.Column(
    header,
    pn.layout.Divider(),
    tabs,
    sizing_mode="stretch_width",
    styles={"padding": "16px"},)

# ─────────────────────────────────────────────
# SERVE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    dashboard.show(port=5006, open=True)
elif __name__.startswith("bokeh"):
    dashboard.servable()