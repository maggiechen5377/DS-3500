"""
Pytest
Rush's Notebook
"""

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
    pass

def test_pm25_values_valid():
    """Test with helpful error messages
    PM2.5 values should be non-negative and cannot be more than 500"""
    pass

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

# Example tests using fixtures
def test_calculate_average(sample_air_quality):
    """Using fixture in a test and approximating values"""

# def test_remove_negative_values(dirty_air_quality):
#     """Test cleaning with dirty fixture"""
#     # Assume we have a clean_air_quality function
#     # cleaned = clean_air_quality(dirty_air_quality)
#     # assert (cleaned['value'] >= 0).all()
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
def test_fetch_openaq_data(mock_get, mock_openaq_response):
    """Test API fetch WITHOUT calling real API"""
    # Setup the mock

    # Call function (uses mock instead of real API)

    # Verify it processed correctly

    # Verify API was called


@patch('requests.get')
def test_fetch_handles_error(mock_get):
    """Test error handling"""
    # Simulate API error

    # Function should handle the error gracefully

    # Verify if the API was called


if __name__ == '__main__':
    # We don't call test functions here!
    # Pytest does it on its own.
    pass