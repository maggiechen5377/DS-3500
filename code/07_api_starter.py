"""
Authentication & Error Handling
Rush's Notebook
"""
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import dotenv
import os
from time import sleep
#TODO: add more imports here (dotenv, os, time)


# TODO: Load environment variables from .env file
# You can use Rush's API key from lecture 6 if you like.
dotenv.load_dotenv()
# ============================================================================
# ENVIRONMENT VARIABLES
# ============================================================================

def demo_environment_variables():
    """
    Using environment variables to load API keys securely
    """
    api_key = os.environ.get("OPENAQ_KEY")
    print(api_key)
    return api_key

# ============================================================================
# ERROR HANDLING
# ============================================================================

def demo_basic_error_handling(url, params=None, headers=None):
    """
    Basic error handling for API requests

    Args:
        url (str): API endpoint
        params (dict): Query parameters
        headers (dict): Request headers

    Returns:
        dict: JSON response or None if error
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            print("success")
        elif response.status_code == 429:
            print('rate limit exceeded')
    except requests.exceptions.ConnextionError:
        print("Connection Error")


def demo_retry_logic(url, params=None, headers=None, max_retries=3):
    """
    Retry logic with exponential backoff

    Args:
        url (str): API endpoint
        params (dict): Query parameters
        headers (dict): Request headers
        max_retries (int): Maximum number of retry attempts

    Returns:
        dict: JSON response or None if all retries fail
    """
    wait = 2
    for i in range(65):
        demo_basic_error_handling(url, params, headers)
        sleep(wait)
        wait = wait * 2


# ============================================================================
# PAGINATION
# ============================================================================

def demo_pagination(url, params=None, headers=None, num_pages=3):
    """
    Retry logic with exponential backoff

    Args:
        url (str): API endpoint
        params (dict): Query parameters
        headers (dict): Request headers
        num_pages (int): Number of pages to retrieve

    Returns:
        dict: JSON response or None if all retries fail
    """
    dataset = []
    for page in range(1, 4):
        params["page"] = page
        response = requests.get(url, params=params, headers=headers)
        print(f"Status code is {response.status_code}")
        if response.status_code == 200:
            new_data = response.json()['results']
            print(f"new data size is {len(new_data)}")
            dataset = dataset + new_data
    print(f"final data size is{len(dataset)}")
    return dataset

# ============================================================================
# OPENAQ AUTHENTICATED PIPELINE
# ============================================================================

def get_air_quality_data(url, params, headers):
    """
    Get air quality data from the OpenAQ API-
     we are going to get PM2.5 data by day
     from a sensor in Boston (sensor ID 521)

    Returns:
        dict: JSON response or None if error
    """
    # make the request
    response = requests.get(url, params=params, headers=headers)
    # data in dictionary
    data_dct = response.json()['results']
    print(json.dumps(data_dct), indent=2)



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

def visualize_air_quality(df, city):
    """
    Create visualization of air quality data

    Args:
        df (pd.DataFrame): Air quality data
        city (str): City name for title
    """

# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

def exercise_1():
    """
    Exercise 1: Get data for your hometown
    """
    pass


def exercise_2():
    """
    Exercise 2: Try retrieving data until you hit
    a certain amount of data using pagination
    """


def exercise_3():
    """
    Exercise 3: Try a different parameter (ozone, PM10)
    """


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to run all demonstrations
    """
    # Part 1: Environment Variables
    # api_key = demo_environment_variables()
    # headers = {'X-API-Key': api_key} if api_key else None

    # demo_basic_error_handling(
    #     "https://api.openaq.org/v3/locations",
    #     params={'limit': 5},
    #     headers=headers
    # )
    #
    # demo_retry_logic(
    #     "https://api.openaq.org/v3/locations",
    #     params={'limit': 5},
    #     headers=headers
    # )
    # demo_pagination(
    #     "https://api.openaq.org/v3/locations",
    #     params={'limit': 5},
    #     headers=headers
    # )

    # add function calls below for demoing air quality pipeline

    # Exercises
    # exercise_1()
    # exercise_2()
    # exercise_3()

    pass


if __name__ == "__main__":
    main()