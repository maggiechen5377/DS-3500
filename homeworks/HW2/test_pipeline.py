import pandas as pd
from pipeline import fetch_gbif_data, clean_biodiversity_data, enrich_with_state_data

def test_fetch_gbif_data():
    """Test that fetch_gbif_data returns a DataFrame with required columns"""
    species_list = ['Sturnus vulgaris']
    year = 2023

    result = fetch_gbif_data(species_list, year)

    assert isinstance(result, pd.DataFrame), "Should return a DataFrame"

    required_columns = ['species_name', 'latitude', 'longitude', 'date', 'state', 'coordinate_uncertainty']
    for col in required_columns:
        assert col in result.columns, f"Missing required column: {col}"

    assert len(result) > 0, "Should return at least some observations"

    print("✓ test_fetch_gbif_data passed")


def test_clean_biodiversity_data():
    """Test that clean_biodiversity_data removes invalid data and returns metrics"""
    sample_data = pd.DataFrame({
        'species_name': ['Bird A', 'Bird B', 'Bird A', None, 'Bird C'],
        'latitude': [40.0, 41.0, 40.0, 42.0, 43.0],
        'longitude': [-70.0, -71.0, -70.0, -72.0, -73.0],
        'date': ['2023-01-01', '2023-02-15', '2023-01-01', '2023-03-20', 'invalid-date'],
        'state': ['MA', 'NY', 'MA', 'CT', 'ME'],
        'coordinate_uncertainty': [10, 20, 10, 30, 40]})

    cleaned_df, metrics = clean_biodiversity_data(sample_data)

    assert isinstance(cleaned_df, pd.DataFrame), "Should return DataFrame"
    assert isinstance(metrics, dict), "Should return metrics dictionary"
    assert 'month' in cleaned_df.columns, "Should add month column"
    assert metrics['removed_duplicates'] == 1, "Should remove 1 duplicate"

    print("✓ test_clean_biodiversity_data passed")


def test_enrich_with_state_data():
    """Test that enrich_with_state_data adds region and area columns"""
    cleaned_data = pd.DataFrame({
        'species_name': ['Bird A', 'Bird B'],
        'latitude': [42.0, 41.0],
        'longitude': [-71.0, -73.0],
        'date': pd.to_datetime(['2023-01-15', '2023-02-20']),
        'state': ['Massachusetts', 'New York'],
        'coordinate_uncertainty': [10, 20],
        'month': [1, 2]})

    state_ref = pd.DataFrame({
        'state_name': ['Massachusetts', 'New York'],
        'region': ['Southern New England', 'Northeast'],
        'area_sq_km': [20202, 122057]})

    enriched_df = enrich_with_state_data(cleaned_data, state_ref)

    assert 'region' in enriched_df.columns, "Should add region column"
    assert 'area_sq_km' in enriched_df.columns, "Should add area_sq_km column"
    assert len(enriched_df) == len(cleaned_data), "Should keep all original rows"

    print("✓ test_enrich_with_state_data passed")
