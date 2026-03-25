"""
pipeline.py
Data pipeline and simulation for bird occurrence observations.
DS3500 Practical Exam 3
"""
import pandas as pd
from collections import defaultdict
from pydantic import ValidationError
from bird_model import BirdObservation

# ── Data Layer ────────────────────────────────────────────────────────────────

def load_data(path: str) -> pd.DataFrame:
    """Load bird occurrence CSV into a DataFrame."""
    df = pd.read_csv(path, sep="\t")
    cleaned = clean_data(df)
    return cleaned

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize the raw DataFrame."""
    df = df.rename(columns={
        "occurrenceID":    "occurrenceID",
        "species":         "species",
        "decimalLatitude": "latitude",
        "decimalLongitude":"longitude",
        "eventDate":       "event_date",
        "countryCode":     "country",
        "individualCount": "count",
    })
    keep = ["occurrenceID", "species", "latitude", "longitude", "event_date", "country", "count"]
    df = df[[c for c in keep if c in df.columns]].copy()
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    df = df.dropna(subset=["species", "latitude", "longitude", "event_date"])
    return df.reset_index(drop=True)

def build_observations(df: pd.DataFrame) -> list:
    """Convert cleaned DataFrame rows into validated BirdObservation objects."""
    observations = []
    validation_errors = 0
    for _, row in df.iterrows():
        try:
            obs = BirdObservation(**row)
            observations.append(obs)
        except ValidationError:
            validation_errors += 1
            continue
    if validation_errors:
        print(f"Skipped {validation_errors} observations due to Validation Errors.")
    return observations

# ── Analysis Layer ────────────────────────────────────────────────────────────
def filter_observations(observations, min_count=1, seasons=None, countries=None):
    """Filter observations by count, season, and/or country."""
    if not isinstance(min_count, int):
        raise TypeError("min_count must be an integer")
    if min_count < 0:
        raise ValueError("min_count must be non-negative")
    if seasons is not None and not isinstance(seasons, list):
        raise TypeError("seasons must be a list")
    if countries is not None and not isinstance(countries, list):
        raise TypeError("countries must be a list")

    return [
        obs for obs in observations
        if obs.count >= min_count
           and (seasons is None or obs.season in seasons)
           and (countries is None or obs.country in countries)
    ]

def summarize_by_species(observations: list) -> dict:
    """Return total count per species across all observations."""
    totals = defaultdict(int)
    for obs in observations:
        totals[obs.species] += obs.count
    return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))

# ── Simulation Layer ──────────────────────────────────────────────────────────
######## YOU MAY IGNORE CODE IN THIS LAYER FOR THE EXAM ########
def run_simulation(observations: list, top_n: int = 5) -> None:
    """
    Simulate bird sightings arriving in chronological order.
    Prints a running tally of the top N species after each month.
    """
    sorted_obs = sorted(observations, key=lambda o: o.event_date)
    running_totals = defaultdict(int)
    current_month = None

    for obs in sorted_obs:
        month_key = (obs.year, obs.event_date.month)

        if current_month is None:
            current_month = month_key

        if month_key != current_month:
            # print tally at end of each month
            top = sorted(running_totals.items(), key=lambda x: x[1], reverse=True)[:top_n]
            print(f"\n── {current_month[0]}-{current_month[1]:02d} ──")
            for species, count in top:
                print(f"  {species:<40} {count:>5}")
            current_month = month_key

        running_totals[obs.species] += obs.count

    # print final month
    top = sorted(running_totals.items(), key=lambda x: x[1], reverse=True)[:top_n]
    print(f"\n── {current_month[0]}-{current_month[1]:02d} (final) ──")
    for species, count in top:
        print(f"  {species:<40} {count:>5}")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    CSV_PATH = "gbif_occurrences.csv"

    raw = load_data(CSV_PATH)
    df = clean_data(raw)
    observations = build_observations(df)

    print(f"\nLoaded {len(observations)} valid observations.")

    filtered = filter_observations(observations, min_count=1)
    run_simulation(filtered, top_n=5)

if __name__ == "__main__":
    main()
