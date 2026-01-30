"""
Pytest
Rush's Notebook
"""
import numpy as np
import pandas as pd
import pytest
import dotenv
import requests
import os
from unittest.mock import patch

# OpenAQ API Key from Lecture 6/7
dotenv.load_dotenv()
AIR_QUALITY_PATH = "data/air_quality.csv"

# From Day 7
def get_air_quality_data():
    """
    Get air quality data from the OpenAQ API-
     we are going to get PM2.5 data by day
     from a sensor in Boston (sensor ID 521)

    Returns:
        dataframe with only
    """
    api_key = os.environ.get("OPENAQ_KEY")
    headers = {'X-API-Key': api_key} if api_key else None
    url = "https://api.openaq.org/v3/sensors/688/measurements/daily"
    hardcoded_fields = {"neighborhood": "Roxbury",
                        "sensor": "pm25",
                        "units": "cubic microns"}
    #make the request
    response = requests.get(url, params={}, headers=headers)

    # if error, send out an empty dataframe
    if response.status_code != 200:
        return pd.DataFrame()

    ### data in dictionary
    data_dct = response.json()

    df = convert_to_dataframe(data_dct, hardcoded_fields)
    return df

def convert_to_dataframe(data, hardcoded_fields):
    """
    Convert API response to pandas DataFrame
    Args:
        data (dict): JSON response from OpenAQ API

    Returns:
        pd.DataFrame: DataFrame with measurement data
    """
    records = []
    for measurement in data['results']:
        entry = {
        # extract relevant data!
            "date":  measurement["date"]["utc"],
            "neighborhood": "Roxbury",
             "value": measurement["value"],
        }
        entry.update(hardcoded_fields)
        records.append(entry)

    df = pd.DataFrame(records)
    return df

###############################################################################
# BASIC PYTEST
###############################################################################
def test_data_loads():
    """Test that CSV data loads correctly.
    Data should have rows.
    Data should have columns for neighborhood and sensor"""
    data = pd.read_csv(AIR_QUALITY_PATH)

    assert len(data) > 0
    assert "neighborhood" in data.columns
    assert "sensor" in data.columns


def test_pm25_values_valid():
    """Test with helpful error messages
    PM2.5 values should be non-negative and cannot be more than 500"""
    data = pd.read_csv(AIR_QUALITY_PATH)

    pm25 = data[data["sensor"] == "pm25"]

    assert (pm25["value"] >= 0).all(), "PM2.5 data has negative values"
    assert (pm25["value"] <= 500).all(), "PM2.5 data has unreasonably high values"


###############################################################################
# FIXTURES
###############################################################################

@pytest.fixture
def sample_air_quality():
    """Clean air quality data for testing"""
    return pd.DataFrame({
        'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03']),
        'neighborhood': ['Roxbury', 'Roxbury', 'Kenmore Sq'],
        'sensor': ['pm25', 'pm25', 'pm25'],
        'value': [3.43, 4.80, 5.69]
    })

@pytest.fixture
def dirty_air_quality():
    """Messy air quality data for testing"""
    return pd.DataFrame({
        'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03']),
        'neighborhood': ['roxbury', 'Roxbury', 'Kenmore Sq'],
        'sensor': ['pm25', 'pm25', 'pm25'],
        'value': [3.43, -4.80, None]
    })

# Example tests using fixtures
def test_calculate_average(sample_air_quality):
    """Using fixture in a test and approximating values"""

    avg = sample_air_quality["value"].mean()

    assert avg == pytest.approx(sum([3.43, 4.80, 5.69])/3)


# def test_remove_negative_values(dirty_air_quality, sample_air_quality):
#     """Test cleaning with dirty fixture"""
#     # Assume we have a clean_air_quality function
#     cleaned = clean_air_quality(dirty_air_quality)
#     # assert (cleaned['value'] >= 0).all()
#     assert cleaned == sample_air_quality
#     pass

###############################################################################
# MOCKING API CALLS
###############################################################################

@pytest.fixture
def mock_openaq_response():
    """Sample OpenAQ API response"""
    return {
        'results': [
            {
                'location': 'Boston-Roxbury',
                'parameter': 'pm25',
                'value': 3.43,
                'date': {'utc': '2026-01-01T00:00:00Z'}
            },
            {
                'location': 'Boston-Roxbury',
                'parameter': 'pm25',
                'value': 4.80,
                'date': {'utc': '2026-01-02T00:00:00Z'}
            }
        ]
    }


# Test with mocking
@patch('requests.get')
def test_fetch_openaq_data(fake_get_request, mock_openaq_response):
    """Test API fetch WITHOUT calling real API"""
    # Setup the mock
    # set up get().status_code
    fake_get_request.return_value.status_code = 200
    # set up get().json()
    fake_get_request.return_value.json.return_value = mock_openaq_response

    # Call function (uses mock instead of real API)
    data = get_air_quality_data()

    # Verify it processed correctly
    assert len(data) == 2
    assert data.at[0, "value"] == 3.43

    # Verify API was called
    fake_get_request.assert_called_once()

@patch('requests.get')
def test_fetch_handles_error(mock_get):
    """Test error handling"""
    # Simulate API error
    # set up get().status_code
    mock_get.return_value.status_code = 404

    # Verify if the API was called
    data = get_air_quality_data()

    assert len(data) == 0

if __name__ == '__main__':
    # We don't call test functions here!
    # Pytest does it on its own.
    pass