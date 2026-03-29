# HW5 — Animating the T

**Line:** Orange Line
**Course:** DS3500

## How to Run

### Setup
Install dependencies:
```bash
pip install pandas pyarrow requests pydantic matplotlib pillow
conda install -c conda-forge ffmpeg
```

### Step 1 — Fetch and clean data
```bash
python acquire.py
```
This downloads all 28 days of February 2026 Orange Line data from the MBTA
LAMP endpoint and caches it locally as `orange_line_feb2026.parquet`.
Only needs to run once.

### Step 2 — Run Animation A (Actual vs Scheduled Travel Time)
```bash
python animate_a.py
```
Saves `mbta_orange_animation_a.mp4`

### Step 3 — Run Animation B (Stop x Day Heatmap)
```bash
python animate_b.py
```
Saves `mbta_orange_animation_b.mp4`

## File Structure

- `acquire.py` — data acquisition and cleaning layer
- `model.py` — Pydantic SubwayLine model with computed fields
- `animate_a.py` — Animation A, actual vs scheduled travel time line chart
- `animate_b.py` — Animation B, stop x day travel time heatmap
- `reflection.md` — written reflection
- `README.md` — this file