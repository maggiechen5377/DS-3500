import pandas as pd

# constants

DATA_PATH = "cause_of_deaths.csv"

DISEASES = [
    "Meningitis", "Alzheimer's Disease and Other Dementias", "Parkinson's Disease",
    "Nutritional Deficiencies", "Malaria", "Drowning", "Interpersonal Violence",
    "Maternal Disorders", "HIV/AIDS", "Drug Use Disorders", "Tuberculosis",
    "Cardiovascular Diseases", "Lower Respiratory Infections", "Neonatal Disorders",
    "Alcohol Use Disorders", "Self-harm", "Exposure to Forces of Nature",
    "Diarrheal Diseases", "Environmental Heat and Cold Exposure", "Neoplasms",
    "Conflict and Terrorism", "Diabetes Mellitus", "Chronic Kidney Disease",
    "Poisonings", "Protein-Energy Malnutrition", "Road Injuries",
    "Chronic Respiratory Diseases", "Cirrhosis and Other Chronic Liver Diseases",
    "Digestive Diseases", "Fire, Heat, and Hot Substances", "Acute Hepatitis"
]

# regions mapping
REGION_MAP = {
    "AFR": "Africa", "AMR": "Americas", "EMR": "Eastern Mediterranean",
    "EUR": "Europe", "SEAR": "South-East Asia", "WPR": "Western Pacific"
}

# data Loading

_df = None

def load_data() -> pd.DataFrame:
    global _df
    if _df is None:
        _df = pd.read_csv(DATA_PATH)
        _df.columns = _df.columns.str.strip()
        _df = _df.rename(columns={"Country/Territory": "Country"})
    return _df


# query functions

def get_years() -> list:
    df = load_data()
    return sorted(df["Year"].unique().tolist())


def get_countries() -> list:
    """Return sorted list of all countries."""
    df = load_data()
    return sorted(df["Country"].unique().tolist())


def get_diseases() -> list:
    """Return list of all disease/cause columns."""
    return DISEASES


def get_map_data(disease: str, year: int) -> pd.DataFrame:
    """
    Return a DataFrame with Country, Code, and death count
    for a given disease and year. Used for choropleth map.
    """
    df = load_data()
    filtered = df[df["Year"] == year][["Country", "Code", disease]].copy()
    filtered = filtered.rename(columns={disease: "Deaths"})
    filtered = filtered.dropna(subset=["Deaths"])
    return filtered


def get_top_countries(disease: str, year: int, n: int = 10) -> pd.DataFrame:
    """
    Return top N countries by death count for a given disease and year.
    """
    df = get_map_data(disease, year)
    return df.nlargest(n, "Deaths").reset_index(drop=True)


def get_trend_data(disease: str, countries: list) -> pd.DataFrame:
    """
    Return year-over-year death counts for selected countries and disease.
    Used for the trend line chart.
    """
    df = load_data()
    filtered = df[df["Country"].isin(countries)][["Country", "Year", disease]].copy()
    filtered = filtered.rename(columns={disease: "Deaths"})
    return filtered.sort_values(["Country", "Year"])


def get_disease_breakdown(country: str, year: int) -> pd.DataFrame:
    """
    Return all disease death counts for a single country and year.
    Used for the disease breakdown bar chart.
    """
    df = load_data()
    row = df[(df["Country"] == country) & (df["Year"] == year)]
    if row.empty:
        return pd.DataFrame(columns=["Disease", "Deaths"])
    values = row[DISEASES].iloc[0]
    result = pd.DataFrame({"Disease": DISEASES, "Deaths": values.values})
    return result.sort_values("Deaths", ascending=False).reset_index(drop=True)


def get_summary_stats(disease: str, year: int) -> dict:
    """
    Return summary statistics for a disease in a given year.
    """
    df = get_map_data(disease, year)
    return {
        "total": int(df["Deaths"].sum()),
        "mean": int(df["Deaths"].mean()),
        "max_country": df.loc[df["Deaths"].idxmax(), "Country"],
        "max_deaths": int(df["Deaths"].max()),
    }


def get_all_years_data(disease: str) -> pd.DataFrame:
    """
    Return a DataFrame with Country, Code, Year, and death count
    for a given disease across ALL years. Used for the animated choropleth.
    """
    df = load_data()
    filtered = df[["Country", "Code", "Year", disease]].copy()
    filtered = filtered.rename(columns={disease: "Deaths"})
    filtered = filtered.dropna(subset=["Deaths"])
    filtered["Year"] = filtered["Year"].astype(str)
    return filtered.sort_values("Year")


# country to region mapping for sunburst grouping
COUNTRY_REGION = {
    "Afghanistan": "Asia", "Albania": "Europe", "Algeria": "Africa",
    "Angola": "Africa", "Argentina": "Americas", "Armenia": "Asia",
    "Australia": "Oceania", "Austria": "Europe", "Azerbaijan": "Asia",
    "Bahrain": "Asia", "Bangladesh": "Asia", "Belarus": "Europe",
    "Belgium": "Europe", "Benin": "Africa", "Bolivia": "Americas",
    "Bosnia and Herzegovina": "Europe", "Botswana": "Africa", "Brazil": "Americas",
    "Bulgaria": "Europe", "Burkina Faso": "Africa", "Burundi": "Africa",
    "Cambodia": "Asia", "Cameroon": "Africa", "Canada": "Americas",
    "Central African Republic": "Africa", "Chad": "Africa", "Chile": "Americas",
    "China": "Asia", "Colombia": "Americas", "Congo": "Africa",
    "Costa Rica": "Americas", "Croatia": "Europe", "Cuba": "Americas",
    "Cyprus": "Europe", "Czech Republic": "Europe", "Denmark": "Europe",
    "Dominican Republic": "Americas", "Ecuador": "Americas", "Egypt": "Africa",
    "El Salvador": "Americas", "Eritrea": "Africa", "Estonia": "Europe",
    "Ethiopia": "Africa", "Finland": "Europe", "France": "Europe",
    "Gabon": "Africa", "Georgia": "Asia", "Germany": "Europe",
    "Ghana": "Africa", "Greece": "Europe", "Guatemala": "Americas",
    "Guinea": "Africa", "Guinea-Bissau": "Africa", "Haiti": "Americas",
    "Honduras": "Americas", "Hungary": "Europe", "India": "Asia",
    "Indonesia": "Asia", "Iran": "Asia", "Iraq": "Asia",
    "Ireland": "Europe", "Israel": "Asia", "Italy": "Europe",
    "Jamaica": "Americas", "Japan": "Asia", "Jordan": "Asia",
    "Kazakhstan": "Asia", "Kenya": "Africa", "Kuwait": "Asia",
    "Kyrgyzstan": "Asia", "Laos": "Asia", "Latvia": "Europe",
    "Lebanon": "Asia", "Lesotho": "Africa", "Liberia": "Africa",
    "Libya": "Africa", "Lithuania": "Europe", "Luxembourg": "Europe",
    "Madagascar": "Africa", "Malawi": "Africa", "Malaysia": "Asia",
    "Mali": "Africa", "Mauritania": "Africa", "Mauritius": "Africa",
    "Mexico": "Americas", "Moldova": "Europe", "Mongolia": "Asia",
    "Morocco": "Africa", "Mozambique": "Africa", "Myanmar": "Asia",
    "Namibia": "Africa", "Nepal": "Asia", "Netherlands": "Europe",
    "New Zealand": "Oceania", "Nicaragua": "Americas", "Niger": "Africa",
    "Nigeria": "Africa", "North Korea": "Asia", "Norway": "Europe",
    "Oman": "Asia", "Pakistan": "Asia", "Panama": "Americas",
    "Papua New Guinea": "Oceania", "Paraguay": "Americas", "Peru": "Americas",
    "Philippines": "Asia", "Poland": "Europe", "Portugal": "Europe",
    "Qatar": "Asia", "Romania": "Europe", "Russia": "Europe",
    "Rwanda": "Africa", "Saudi Arabia": "Asia", "Senegal": "Africa",
    "Sierra Leone": "Africa", "Singapore": "Asia", "Slovakia": "Europe",
    "Slovenia": "Europe", "Somalia": "Africa", "South Africa": "Africa",
    "South Korea": "Asia", "South Sudan": "Africa", "Spain": "Europe",
    "Sri Lanka": "Asia", "Sudan": "Africa", "Swaziland": "Africa",
    "Sweden": "Europe", "Switzerland": "Europe", "Syria": "Asia",
    "Taiwan": "Asia", "Tajikistan": "Asia", "Tanzania": "Africa",
    "Thailand": "Asia", "Togo": "Africa", "Trinidad and Tobago": "Americas",
    "Tunisia": "Africa", "Turkey": "Asia", "Turkmenistan": "Asia",
    "Uganda": "Africa", "Ukraine": "Europe", "United Arab Emirates": "Asia",
    "United Kingdom": "Europe", "United States": "Americas", "Uruguay": "Americas",
    "Uzbekistan": "Asia", "Venezuela": "Americas", "Vietnam": "Asia",
    "Yemen": "Asia", "Zambia": "Africa", "Zimbabwe": "Africa",
}

def get_sunburst_data(year: int, top_n_countries: int = 5) -> pd.DataFrame:
    """
    Return data structured for a sunburst chart:
    World → Region → Country → Disease
    Shows top_n_countries per region by total deaths.
    """
    df = load_data()
    df = df[df["Year"] == year].copy()

    # add region
    df["Region"] = df["Country"].map(COUNTRY_REGION).fillna("Other")
    df = df[df["Region"] != "Other"]

    # melt diseases into rows
    melted = df.melt(
        id_vars=["Country", "Region"],
        value_vars=DISEASES,
        var_name="Disease",
        value_name="Deaths"
    )
    melted = melted.dropna(subset=["Deaths"])
    melted["Deaths"] = melted["Deaths"].astype(int)

    # keep only top N countries per region by total deaths
    country_totals = melted.groupby(["Region", "Country"])["Deaths"].sum().reset_index()
    top_countries = (
        country_totals.sort_values("Deaths", ascending=False)
        .groupby("Region")
        .head(top_n_countries)["Country"]
        .tolist())
    melted = melted[melted["Country"].isin(top_countries)]

    return melted