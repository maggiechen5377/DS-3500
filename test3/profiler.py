import cProfile
import pstats
import time
import pandas as pd
from bird_pipeline import clean_data, build_observations, filter_observations

def run_pipeline():
    df = pd.read_csv("gbif_occurrences.csv", sep="\t", nrows=1000)
    df = clean_data(df)
    obs = build_observations(df)
    filter_observations(obs, min_count=1)

start = time.time()
run_pipeline()
end = time.time()
print(f"Main runtime: {end - start:.3f} seconds")

cProfile.run("run_pipeline()", "output.prof")

p = pstats.Stats("output.prof")
p.sort_stats("cumulative")
p.print_stats(10)