from pydantic import BaseModel, computed_field
import pandas as pd

STATION_LABELS = {
    "place-ogmnl": "Oak Grove",
    "place-mlmnl": "Malden Center",
    "place-welln": "Wellington",
    "place-astao": "Assembly",
    "place-sull": "Sullivan Square",
    "place-ccmnl": "Community College",
    "place-north": "North Station",
    "place-haecl": "Haymarket",
    "place-state": "State",
    "place-dwnxg": "Downtown Crossing",
    "place-chncl": "Chinatown",
    "place-tumnl": "Tufts Medical Center",
    "place-bbsta": "Back Bay",
    "place-masta": "Massachusetts Avenue",
    "place-rugg": "Ruggles",
    "place-rcmnl": "Roxbury Crossing",
    "place-jaksn": "Jackson Square",
    "place-sbmnl": "Stony Brook",
    "place-grnst": "Green Street",
    "place-forhl": "Forest Hills",
}


class SubwayLine(BaseModel):
    route_name: str
    route_id: str
    df: pd.DataFrame
    station_order: list[str]

    model_config = {"arbitrary_types_allowed": True}

    @computed_field
    @property
    def stops(self) -> list[str]:
        """Ordered list of station IDs along the line."""
        return self.station_order

    @computed_field
    @property
    def stop_labels(self) -> list[str]:
        """Human-readable station names in geographic order."""
        return [STATION_LABELS.get(s, s) for s in self.station_order]

    @computed_field
    @property
    def dates(self) -> list[str]:
        """Sorted list of service dates in February as strings."""
        return sorted(self.df["service_date"].dt.strftime("%Y-%m-%d").unique().tolist())

    @computed_field
    @property
    def daily_avg_travel(self) -> dict[str, float]:
        """Date string -> mean actual travel time (seconds) across all trips."""
        result = (
            self.df.groupby(self.df["service_date"].dt.strftime("%Y-%m-%d"))
            ["travel_time_seconds"]
            .mean()
        )
        return result.to_dict()

    @computed_field
    @property
    def daily_avg_scheduled(self) -> dict[str, float]:
        """Date string -> mean scheduled travel time (seconds) across all trips."""
        result = (
            self.df.groupby(self.df["service_date"].dt.strftime("%Y-%m-%d"))
            ["scheduled_travel_time"]
            .mean()
        )
        return result.to_dict()

    @computed_field
    @property
    def travel_by_stop_and_day(self) -> pd.DataFrame:
        """
        Produce a summary table by stop and day where value is mean travel time in seconds.
        This is the 2D array the heatmap animation calls set_array() on.
        """
        pivot = self.df.pivot_table(
            index="parent_station",
            columns=self.df["service_date"].dt.strftime("%Y-%m-%d"),
            values="travel_time_seconds",
            aggfunc="mean"
        )
        ordered = [s for s in self.station_order if s in pivot.index]
        return pivot.reindex(ordered)


if __name__ == "__main__":
    from acquire import load_orange_line, get_station_order

    df = load_orange_line()
    line = SubwayLine(
        route_name="Orange Line",
        route_id="Orange",
        df=df,
        station_order=get_station_order()
    )

    print("Stops:", line.stops)
    print("Stop labels:", line.stop_labels)
    print("Dates:", line.dates[:3])
    print("Daily avg travel (first 3):", dict(list(line.daily_avg_travel.items())[:3]))
    print("Heatmap shape:", line.travel_by_stop_and_day.shape)