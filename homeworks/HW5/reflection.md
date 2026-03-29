# Reflection — Animating the T (Orange Line, February 2026)

## 1. Storm Impact

Both animations tell a clear story about service disruption in February 2026.
In Animation A, there is a noticeable spike in actual travel time around
February 8-9, where the orange line jumps to nearly 95 seconds, well above
the relatively stable scheduled travel time of around 110 seconds.
Interestingly, the actual travel time is consistently *below* the scheduled
time for most of the month, which suggests the Orange Line generally runs
faster than planned under normal conditions. The blizzard disrupted this
pattern visibly.

In Animation B, the heatmap reveals white (missing) cells around February
13-16 concentrated at the southern end of the line, particularly Stony Brook,
Green Street, and Forest Hills. This suggests those stops experienced the most
severe service gaps, possibly due to above-ground track exposure to snow and
ice. Service appears to have largely recovered by February 17, with color
returning consistently across all stops.

## 2. Data Limitations

The `scheduled_travel_time` field is null for any trip that the MBTA ran as
non-standard or unplanned service, which happens frequently during storms when
the agency deviates from its published schedule. In my cleaning step, I dropped
all rows with null `scheduled_travel_time` before computing scheduled
aggregates. This means Animation A's scheduled line is based on a smaller
subset of trips on storm days, making it appear artificially stable. A more
complete picture would require imputing or separately tracking unmatched trips.

## 3. Layered Architecture

The layer separation proved most useful when I needed to fix the station
ordering in the heatmap. The `travel_by_stop_and_day` pivot table was producing
zero rows because the station IDs in `ORANGE_LINE_STOPS` didn't match the
`parent_station` values in the data. Because the model layer was isolated in
`models.py`, I could test and fix the computed field independently by running
`models.py` directly without touching `animate.py` at all. This made the
debugging loop much faster and kept the problem contained to one file.

## 4. AI Usage Statement

I used Claude (Anthropic) as an AI assistant for this assignment. I used it
to help formulate the overall structure and steps of the project, including
how to organize the three-layer architecture across `data.py`, `models.py`,
and `animate.py`. I also relied on it heavily for debugging, including fixing
a 403 error when fetching the MBTA parquet files, resolving a URL format
issue, correcting a station ID mismatch that caused the heatmap to return
zero rows, and troubleshooting a nested Git repository conflict. In most
cases I had to step in to verify the output looked correct, identify when
something was still wrong, and provide the actual error messages so the AI
could diagnose the issue accurately.