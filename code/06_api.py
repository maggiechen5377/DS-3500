"""
REST APIs & Basic Requests
Rush's Notebook

Topics:
- JSON structure and parsing
- Making GET requests with the requests library
- Extracting data from API responses
"""

import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

# THIS IS RUSH's API KEY.
# YOU WILL BE RATE-LIMITED PAST A CERTAIN POINT
# IF YOU'D LIKE TO PRACTICE, USE YOUR OWN API KEY
API_KEY = "96681b9ba7abb77834eb76e7e45c7e75fdd0f5a81a8bb6d90b0dab8c4d1bee9c"

# ============================================================================
# JSON REVIEW
# ============================================================================

def explore_json_structure(json_data):
    """
    Review JSON structure and navigation
    """
    # Parse the JSON string
    # data = json.loads(json_data)
    data = json_data

    print("Data type:", type(data))
    print("Top-level keys:", data.keys())
    print("\nFirst result:")
    print(json.dumps(data['results'][0], indent=2))

    # Extract specific values
    # first_value = data['results'][0]['value']
    # all_values = [result['value'] for result in data['results']]

# ============================================================================
# FIRST API CALL
# ============================================================================

def simple_api_request():
    """
    Make a simple API countries request to Open AQ.
    Returns the JSON data.
    """
    endpoint = "https://api.openaq.org/v3/countries/155"
    headers = {
        "X-API-Key" : API_KEY
    }
    response = requests.request("GET", endpoint, headers = headers)
    return response.json()



def api_request_with_parameters():
    """
    Make API request with query parameters. Use the Open AQ
    API to get locations near Boston via coordinates.
    Returns: the JSON data.
    """
    endpoint = "https://api.openaq.org/v3/locations"
    headers = {
        "X-API-Key": API_KEY
    }
    parameters = {
        "coordinates": "42.3611,-71.0570",
        "radius": 1000
    }
    response = requests.request("GET", endpoint,
                                headers=headers,
                                params=parameters)
    return response.json()

def convert_to_dataframe(data):
    """
    Convert API response to pandas DataFrame
    Args:
        data (dict): JSON response from OpenAQ API

    Returns:
        pd.DataFrame: DataFrame with measurement data
    """
    # TODO: Extract relevant fields
    records = []
    for measurement in data['results']:
        records.append({
        # extract relevant data!
        })

    df = pd.DataFrame(records)
    return df

# ============================================================================
# PRACTICE EXERCISES (10 min)
# ============================================================================

def exercise_1():
    """
    Exercise 1: Get air quality data for a city
    - What's the average PM2.5 value?
    - create a visualization for the PM2.5 values
    """
    pass


def exercise_2():
    """
    Exercise 2: Try a different parameter
    - Look at the OpenAQ docs for other parameter IDs
    - Try ozone (o3) or PM10
    """
    pass


def exercise_3():
    """
    Exercise 3: Extract specific fields
    - Create a list of all location names
    - Hint: Use list comprehensions!
    """
    pass


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to run all demonstrations
    """
    # JSON Review
    # explore_json_structure()

    # Simple request
    json_data = simple_api_request()
    # explore_json_structure(json_data)

    # Request with parameters
    data = api_request_with_parameters()
    explore_json_structure(data)

    # Extract and analyze
    # df = convert_to_dataframe(data)


    # Exercises
    # exercise_1()
    # exercise_2()
    # exercise_3()



if __name__ == "__main__":
    main()
