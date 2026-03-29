import pandas as pd
import requests
import io
from pathlib import Path

CACHE_FILE = Path("orange_line_feb2026.parquet")
TRUNK_ROUTE_ID = "Orange"

ORANGE_LINE_STOPS = [
    "place-ogmnl",  # Oak Grove
    "place-mlmnl",  # Malden Center
    "place-welln",  # Wellington
    "place-astao",  # Assembly
    "place-sull",   # Sullivan Square
    "place-ccmnl",  # Community College
    "place-north",  # North Station
    "place-haecl",  # Haymarket
    "place-state",  # State
    "place-dwnxg",  # Downtown Crossing
    "place-chncl",  # Chinatown
    "place-tumnl",  # Tufts Medical Center
    "place-bbsta",  # Back Bay
    "place-masta",  # Massachusetts Avenue
    "place-rugg",   # Ruggles
    "place-rcmnl",  # Roxbury Crossing
    "place-jaksn",  # Jackson Square
    "place-sbmnl",  # Stony Brook
    "place-grnst",  # Green Street
    "place-forhl",  # Forest Hills
]


def fetch_data(trunk_route_id: str = TRUNK_ROUTE_ID) -> pd.DataFrame:
    if CACHE_FILE.exists():
        print("Loading from cache...")
        return pd.read_parquet(CACHE_FILE)

    base_url = "https://performancedata.mbta.com/lamp/subway-on-time-performance-v1/2026-02-{day:02d}-subway-on-time-performance-v1.parquet"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    frames = []
    for day in range(1, 29):
        url = base_url.format(day=day)
        print(f"Fetching day {day}...")
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            df = pd.read_parquet(io.BytesIO(response.content))
            df = df[df["trunk_route_id"] == trunk_route_id]
            frames.append(df)
        except Exception as e:
            print(f"  Skipped day {day}: {e}")

    combined = pd.concat(frames, ignore_index=True)
    combined.to_parquet(CACHE_FILE)
    print(f"Cached to {CACHE_FILE}")
    return combined

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and deduplicate the raw LAMP dataframe."""

    df = df.sort_values("stop_timestamp")
    df = df.drop_duplicates(subset=["trip_id", "stop_id", "service_date"], keep="first")

    df = df.dropna(subset=["travel_time_seconds", "stop_timestamp", "parent_station"])

    df = df.dropna(subset=["scheduled_travel_time"])

    df["service_date"] = pd.to_datetime(df["service_date"].astype(str), format="%Y%m%d")

    return df.reset_index(drop=True)


def get_trip_durations(df: pd.DataFrame) -> pd.DataFrame:
    """Compute end-to-end trip duration by summing segment travel times."""
    trip_durations = (
        df.groupby(["trip_id", "service_date"])["travel_time_seconds"]
        .sum()
        .reset_index()
        .rename(columns={"travel_time_seconds": "total_travel_time_seconds"})
    )
    return trip_durations


def get_station_order() -> list[str]:
    """Return the ordered list of Orange Line stations (geographic order)."""
    return ORANGE_LINE_STOPS


def load_orange_line() -> pd.DataFrame:
    """Main entry point: fetch, cache, and clean Orange Line data."""
    raw = fetch_data()
    return clean_data(raw)


if __name__ == "__main__":
    df = load_orange_line()
    print(df.shape)
    print(df.dtypes)
    print(df["parent_station"].unique())