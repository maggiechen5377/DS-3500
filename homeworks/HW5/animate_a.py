import matplotlib.pyplot as plt
import matplotlib.animation as animation
from model import SubwayLine
from acquire import load_orange_line, get_station_order


def animate_line_chart(line: SubwayLine, save_path: str = "mbta_orange_animation_a.mp4"):
    """Animation A: Actual vs Scheduled Travel Time, building day by day."""
    dates = line.dates
    actual = [line.daily_avg_travel[d] for d in dates]
    scheduled = [line.daily_avg_scheduled[d] for d in dates]
    x = list(range(len(dates)))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, len(dates) - 1)
    ax.set_ylim(0, max(max(actual), max(scheduled)) * 1.2)
    ax.set_xticks(x[::3])
    ax.set_xticklabels([dates[i][5:] for i in x[::3]], rotation=45)
    ax.set_xlabel("Date (February 2026)")
    ax.set_ylabel("Mean Travel Time (seconds)")
    ax.set_title("Orange Line: Actual vs Scheduled Travel Time — February 2026")

    actual_line, = ax.plot([], [], color="tomato", label="Actual", linewidth=2)
    sched_line, = ax.plot([], [], color="steelblue", label="Scheduled",
                          linewidth=2, linestyle="--")

    ax.axvspan(11, 13, alpha=0.15, color="gray", label="Blizzard")
    ax.legend()

    def update(i):
        actual_line.set_data(x[:i+1], actual[:i+1])
        sched_line.set_data(x[:i+1], scheduled[:i+1])
        return actual_line, sched_line

    anim = animation.FuncAnimation(
        fig, update, frames=len(dates), interval=200, blit=True
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
    animate_line_chart(line)