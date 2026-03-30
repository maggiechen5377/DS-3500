# Reflection — Animating the T (Orange Line, February 2026)

## 1. Storm Impact

Both animations tell a clear story about service disruption in February 2026.
In Animation A, there is a noticeable spike in actual travel time around
February 8-9, where the orange line jumps to nearly 95 seconds, well above
the relatively stable scheduled travel time of around 110 seconds.
Interestingly, the actual travel time is consistently below the scheduled
time for most of the month, suggesting the Orange Line generally runs faster
than planned under normal conditions.

In Animation B, the heatmap reveals white (missing) cells around February
13-16 concentrated at the southern end of the line, particularly Stony Brook,
Green Street, and Forest Hills. This suggests those stops experienced the most
severe service gaps, possibly due to above-ground track exposure to snow and
ice. Service appears to have largely recovered by February 17.

## 2. Data Limitations

The `scheduled_travel_time` field is null for any trip the MBTA ran as
non-standard service, which happens frequently during storms when the agency
deviates from its published schedule. In my cleaning step, I dropped all rows
with null `scheduled_travel_time` before computing scheduled aggregates. This
means Animation A's scheduled line is based on a smaller subset of trips on
storm days, making it appear artificially stable.

## 3. Layered Architecture

The layer separation proved most useful when I needed to fix the station
ordering in the heatmap. The `travel_by_stop_and_day` pivot table was
producing zero rows because the station IDs in `ORANGE_LINE_STOPS` did not
match the `parent_station` values in the data. Because the model layer was
isolated in `model.py`, I could test and fix the computed field independently
by running `model.py` directly without touching either animation file.

## 4. AI Usage Statement

I used Claude (Anthropic) for this assignment to help structure the three-layer
architecture and debug several issues, including a 403 error fetching MBTA
parquet files, a URL format issue, a station ID mismatch causing zero heatmap
rows, and a nested Git repository conflict. In most cases I had to step in to
verify output, identify when something was still wrong, and provide error
messages so the AI could diagnose the issue accurately.