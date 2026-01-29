import requests
import pandas as pd
import time

#1 Data Acquisition
def fetch_gbif_data(species_list, year):
    """
    Parameters:
    species_list: list of scientific names
    year: int

    Return:
    pd.DataFrame with species name, coordinates, date, state,
    and coordinate uncertainty
    """
    base_url = "https://api.gbif.org/v1/occurrence/search"
    records = []
    for species in species_list:
        print(f"Fetching data for {species}")