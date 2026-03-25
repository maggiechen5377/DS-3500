import pandas as pd
import pytest
from datetime import datetime

from bird_model import BirdObservation
from bird_pipeline import filter_observations, summarize_by_species, clean_data


@pytest.fixture
def raw_dataframe():
    """Raw DataFrame with two rows missing required fields."""
    return pd.DataFrame({
        "decimalLatitude":  [42.3, None, 41.1],
        "decimalLongitude": [-71.0, -70.5, None],
        "species":          ["Puffinus puffinus", "Fratercula arctica", "Morus bassanus"],
        "eventDate":        ["2023-06-01", "2023-07-15", "2023-08-20"],
        "countryCode":      ["US", "CA", "US"],
        "individualCount":  [2, 1, 3],
    })


@pytest.fixture
def single_observation():
    """A single valid BirdObservation in July (Summer)."""
    return BirdObservation(
        species="Puffinus puffinus",
        latitude=42.3,
        longitude=-71.0,
        event_date=datetime(2023, 7, 15),
        country="US",
        count=2,
    )


@pytest.fixture
def mixed_count_observations():
    """Three observations with counts 1, 3, and 2 for filter testing."""
    return [
        BirdObservation(species="A", latitude=10.0, longitude=10.0,
                        event_date=datetime(2023, 6, 1), country="US", count=1),
        BirdObservation(species="B", latitude=10.0, longitude=10.0,
                        event_date=datetime(2023, 6, 1), country="US", count=3),
        BirdObservation(species="C", latitude=10.0, longitude=10.0,
                        event_date=datetime(2023, 6, 1), country="US", count=2),
    ]


@pytest.fixture
def multi_observation_list():
    """Two Puffinus and one Fratercula observations for summarize testing."""
    return [
        BirdObservation(species="Puffinus puffinus", latitude=42.3, longitude=-71.0,
                        event_date=datetime(2023, 5, 1), country="US", count=3),
        BirdObservation(species="Puffinus puffinus", latitude=42.3, longitude=-71.0,
                        event_date=datetime(2023, 6, 1), country="US", count=2),
        BirdObservation(species="Fratercula arctica", latitude=65.0, longitude=-14.0,
                        event_date=datetime(2023, 7, 1), country="IS", count=1),
    ]


def test_clean_data_drops_nulls(raw_dataframe):
    """Rows missing required fields should be dropped after cleaning."""
    cleaned = clean_data(raw_dataframe)
    assert len(cleaned) == 1  # only the first row is fully valid

def test_bird_observation_season(single_observation):
    """Computed season field should return correct meteorological season."""
    assert single_observation.season == "Summer"


def test_filter_by_min_count(mixed_count_observations):
    """Only observations meeting the minimum count should be returned."""
    result = filter_observations(mixed_count_observations, min_count=2)
    assert len(result) == 2


def test_summarize_by_species(multi_observation_list):
    """summarize_by_species should return correct totals per species."""
    result = summarize_by_species(multi_observation_list)
    assert result["Puffinus puffinus"] == 5
    assert result["Fratercula arctica"] == 1
