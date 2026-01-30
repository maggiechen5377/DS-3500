import matplotlib
matplotlib.use('TkAgg')
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    all_records = []

    for species in species_list:
        print(f"Fetching data for {species}")
        params = {
            'scientificName': species,
            'year': year,
            'decimalLatitude': '38.8,47.5',
            'decimalLongitude': '-77.5,-66.5',
            'hasCoordinate': True,
            'limit': 100}
        try:
            response = requests.get(base_url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                all_records.extend(results)
                print(f"  Retrieved {len(results)} observations for {species}")
            else:
                print(f"  Error {response.status_code} for {species}")
        except Exception as e:
            print(f"  Exception for {species}: {e}")

    if not all_records:
        print("No records retrieved!")
        return pd.DataFrame()

    df = pd.DataFrame(all_records)

    result_df = pd.DataFrame({
        'species_name': df['scientificName'],
        'latitude': df['decimalLatitude'],
        'longitude': df['decimalLongitude'],
        'date': df['eventDate'],
        'state': df['stateProvince'],
        'coordinate_uncertainty': df['coordinateUncertaintyInMeters']
    })
    return result_df


# 2 Data Cleaning & Metrics
def clean_biodiversity_data(raw_df):
    """
    Clean biodiversity data by removing invalid/missing data, duplicates,
    and invalid dates. Extract month from dates.

    Parameters:
    raw_df : pd.DataFrame, raw data from fetch_gbif_data

    Returns:
    tuple: (cleaned_df, metrics_dict)
        - cleaned_df: DataFrame with cleaned data and month column
        - metrics_dict: Dictionary with cleaning metrics
    """
    initial_count = len(raw_df)
    df = raw_df.copy()
    removed_missing = 0
    removed_duplicates = 0
    removed_invalid_dates = 0

    critical_columns = ['species_name', 'latitude', 'longitude', 'date']
    before_missing = len(df)
    df = df.dropna(subset=critical_columns)
    removed_missing = before_missing - len(df)

    before_duplicates = len(df)
    df = df.drop_duplicates()
    removed_duplicates = before_duplicates - len(df)

    before_dates = len(df)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df = df.dropna(subset=['date'])

    df['month'] = df['date'].dt.month

    removed_invalid_dates = before_dates - len(df)

    final_count = len(df)
    percent_retained = (final_count / initial_count) * 100 if initial_count > 0 else 0

    metrics = {
        'raw_count': initial_count,
        'clean_count': final_count,
        'removed_missing': removed_missing,
        'removed_duplicates': removed_duplicates,
        'removed_invalid_dates': removed_invalid_dates,
        'percent_retained': round(percent_retained, 2)}
    return df, metrics

# 3 Data Enrichment
def enrich_with_state_data(cleaned_df, state_ref_df):
    """
    Join bird observations with state reference data.

    Parameters:
    cleaned_df : pd.DataFrame
        - cleaned bird observations data
    state_ref_df : pd.DataFrame
        - state reference data with state names, regions, and land areas

    Returns:
    pd.DataFrame
        -enriched data with region and area_sq_km columns added
    """
    enriched_df = cleaned_df.copy()
    enriched_df['state'] = enriched_df['state'].str.strip().str.title()
    state_ref_df['state_name'] = state_ref_df['state_name'].str.strip().str.title()
    enriched_df = enriched_df.merge(
        state_ref_df[['state_name', 'region', 'area_sq_km']],
        left_on='state',
        right_on='state_name',
        how='left')

    enriched_df = enriched_df.drop(columns=['state_name'])
    unmatched_states = enriched_df[enriched_df['region'].isnull()]['state'].unique()

    if len(unmatched_states) > 0:
        print(f"\nWarning: {len(unmatched_states)} states didn't match:")
        for state in unmatched_states:
            if pd.notna(state):
                print(f"  - {state}")
        print("These observations will have null region and area_sq_km values.")
    else:
        print("\n✓ All states matched successfully!")
    return enriched_df

# 4 Analysis
def calculate_analysis(enriched_df):
    """
    Perform analysis on enriched bird observation data.

    Parameters:
    enriched_df : pd.DataFrame
        - enriched data with region and area_sq_km columns

    Returns:
    None (displays analysis results and plots)
    """
    print("\n" + "=" * 60)
    print("ANALYSIS: Observations per State with Density")
    print("=" * 60)

    state_data = enriched_df[enriched_df['area_sq_km'].notna()].copy()

    obs_per_state = state_data.groupby('state').agg({
        'species_name': 'count',
        'area_sq_km': 'first'
    }).rename(columns={'species_name': 'observations'})

    obs_per_state['density'] = (obs_per_state['observations'] / obs_per_state['area_sq_km']) * 1000

    obs_per_state = obs_per_state.sort_values('density', ascending=False)

    print("\nObservations per State (sorted by density):")
    print(f"{'State':<20} {'Observations':<15} {'Area (sq km)':<15} {'Density*':<15}")
    print("-" * 65)
    for state, row in obs_per_state.iterrows():
        print(f"{state:<20} {row['observations']:<15.0f} {row['area_sq_km']:<15.0f} {row['density']:<15.4f}")

    print("\n*Density = observations per 1000 sq km")
    print(f"\nHighest density: {obs_per_state.index[0]} ({obs_per_state['density'].iloc[0]:.4f})")
    print(f"Lowest density: {obs_per_state.index[-1]} ({obs_per_state['density'].iloc[-1]:.4f})")
    print("\n" + "=" * 60)
    print("ANALYSIS: Species Distribution Across Months")
    print("=" * 60)

    species_month = enriched_df.groupby(['month', 'species_name']).size().reset_index(name='count')

    plt.figure(figsize=(12, 6))

    sns.barplot(data=species_month, x='month', y='count', hue='species_name', palette='Set2')

    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Observations', fontsize=12)
    plt.title('Species Distribution Across Months', fontsize=14, fontweight='bold')
    plt.legend(title='Species', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.tight_layout()
    plt.savefig('species_dist.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot saved as 'species_dist.png'")
    plt.show()

    print("\nObservations by Month:")
    monthly_totals = enriched_df.groupby('month').size().sort_index()
    for month, count in monthly_totals.items():
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        print(f"  {month_names[month - 1]}: {count} observations")

    print("\nObservations by Species:")
    species_totals = enriched_df.groupby('species_name').size()
    for species, count in species_totals.items():
        print(f"  {species}: {count} observations")

    # Analysis
    calculate_analysis(enriched_data)

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    import json

    # Define species and load data
    species_list = [
        'Sturnus vulgaris',
        'Turdus migratorius',
        'Poecile atricapillus']

    # Step 1: Data Acquisition
    print("Step 1: Fetching data from GBIF API...")
    bird_data = fetch_gbif_data(species_list, year=2023)

    # Step 2: Data Cleaning
    print("\nStep 2: Cleaning data...")
    cleaned_data, metrics = clean_biodiversity_data(bird_data)

    # Step 3: Data Enrichment
    print("\nStep 3: Enriching with state data...")
    state_ref = pd.read_csv('state_reference.csv')
    enriched_data = enrich_with_state_data(cleaned_data, state_ref)

    # Step 4: Analysis
    print("\nStep 4: Performing analysis...")
    calculate_analysis(enriched_data)

    # Generate Deliverable Files
    print("\n" + "=" * 60)
    print("GENERATING DELIVERABLE FILES")
    print("=" * 60)

    # 1. analysis_output.json
    analysis_output = {
        "observations_by_state": enriched_data.groupby('state').size().to_dict(),
        "observations_by_region": enriched_data['region'].value_counts().to_dict(),
        "observations_by_month": enriched_data.groupby('month').size().to_dict(),
        "observations_by_species": enriched_data.groupby('species_name').size().to_dict(),
        "total_observations": len(enriched_data),
        "states_covered": enriched_data['state'].nunique(),
        "date_range": {
            "earliest": enriched_data['date'].min().strftime('%Y-%m-%d'),
            "latest": enriched_data['date'].max().strftime('%Y-%m-%d')
        }
    }

    with open('analysis_output.json', 'w') as f:
        json.dump(analysis_output, f, indent=2)
    print("✓ Saved analysis_output.json")

    # 2. quality_metrics.json
    with open('quality_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    print("✓ Saved quality_metrics.json")

    # 3. species_dist.png (saved by calculate_analysis function)
    print("✓ Saved species_dist.png")

    print("\nAll deliverable files generated successfully!")

# ============================================
# VALIDATION TESTS (Requirement 5)
# ============================================

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
