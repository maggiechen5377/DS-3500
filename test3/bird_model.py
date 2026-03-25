"""
Pydantic model for bird occurrence observations.
DS3500 Practical Exam 3
"""
from pydantic import BaseModel, field_validator, computed_field
from datetime import datetime


class BirdObservation(BaseModel):
    """A single bird occurrence record from GBIF."""
    occurrenceID: str | None = None
    species: str
    latitude: float
    longitude: float
    event_date: datetime
    country: str
    count: int

    @field_validator("latitude")
    @staticmethod
    def latitude_in_range(v):
        if not (-90 <= v <= 90):
            raise ValueError(f"Latitude must be between -90 and 90, got {v}")
        return v

    @field_validator("longitude")
    @staticmethod
    def longitude_in_range(v):
        if v is None:
            return v
        if not (-180 <= v <= 180):
            raise ValueError(f"Longitude must be between -180 and 180, got {v}")
        return v

    @field_validator("count")
    @staticmethod
    def count_must_be_positive(v):
        if v < 1:
            raise ValueError(f"Count must be at least 1, got {v}")
        return v

    @computed_field
    @property
    def season(self) -> str:
        """Return the meteorological season for the observation."""
        month = self.event_date.month
        if month in (12, 1, 2):
            return "Winter"
        elif month in (3, 4, 5):
            return "Spring"
        elif month in (6, 7, 8):
            return "Summer"
        else:
            return "Fall"

    @computed_field
    @property
    def year(self) -> int:
        """Return the year of the observation."""
        return self.event_date.year

    @computed_field
    @property
    def hemisphere(self) -> str:
        """Return 'Northern' or 'Southern' based on latitude."""
        return "Northern" if self.latitude >= 0 else "Southern"

    def is_rare(self, threshold: int = 2) -> bool:
        """Return True if the observation count is below the rarity threshold."""
        return self.count < threshold

    def summary(self) -> str:
        """Return a short human-readable summary of the observation."""
        return (
            f"{self.species} | {self.country} | "
            f"{self.event_date.strftime('%Y-%m-%d')} | "
            f"Season: {self.season} | Count: {self.count}"
        )

    def __hash__(self):
        """Bird observations are uniquely identified by their occurrenceID."""
        return hash(self.occurrenceID)