import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from model import SubwayLine
from acquire import load_orange_line, get_station_order


def animate_heatmap(line: SubwayLine, save_path: str = "mbta_orange_animation_b.mp4"):
    """Animation B: Stop x Day heatmap, revealing one column per frame."""
    heatmap_df = line.travel_by_stop_and_day
    data = heatmap_df.values.astype(float)
    n_stops, n_days = data.shape

    vmin = np.nanmin(data)
    vmax = np.nanmax(data)

    display = np.full_like(data, np.nan)

    fig, ax = plt.subplots(figsize=(12, 7))
    im = ax.imshow(
        display, aspect="auto", cmap="plasma",
        vmin=vmin, vmax=vmax,
        interpolation="nearest"
    )

    ax.set_yticks(range(n_stops))
    ax.set_yticklabels(line.stop_labels, fontsize=8)
    ax.set_xticks(range(n_days))
    ax.set_xticklabels([d[5:] for d in line.dates], rotation=90, fontsize=7)
    ax.set_xlabel("Date (February 2026)")
    ax.set_title("Orange Line: Mean Travel Time by Stop & Day — February 2026")
    plt.colorbar(im, ax=ax, label="Mean Travel Time (seconds)")
    plt.tight_layout()

    def update(i):
        display[:, i] = data[:, i]
        im.set_array(display)
        return [im]

    anim = animation.FuncAnimation(
        fig, update, frames=n_days, interval=200, blit=True
    )
    anim.save(save_path, writer="ffmpeg", fps=5)
    print(f"Saved {save_path}")
    plt.close()


if __name__ == "__main__":
    df = load_orange_line()
    line = SubwayLine(
        route_name="Orange Line",
        route_id="Orange",
        df=df,
        station_order=get_station_order()
    )
    animate_heatmap(line)