"""
Schema mapping documentation for OurAirports dataset to Airport model.

This module documents the field mapping and normalization rules used when
importing data from the OurAirports CSV dataset into our Airport model.

Dataset: OurAirports (https://davidmegginson.github.io/ourairports-data/)
License: Public Domain
"""

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from apps.base.models import City, Country


class OurAirportsCSVRow(TypedDict, total=False):
    """Type definition for OurAirports CSV row structure."""

    # From OurAirports airports.csv schema
    id: str  # Integer ID (not used in our model)
    ident: str  # ICAO or local code (our primary key)
    type: str  # Airport type (e.g., large_airport, small_airport)
    name: str  # Airport name
    latitude_deg: str  # Latitude in decimal degrees (string in CSV)
    longitude_deg: str  # Longitude in decimal degrees (string in CSV)
    elevation_ft: str  # Elevation in feet (string in CSV, may be empty)
    continent: str  # Continent code (not used in our model)
    iso_country: str  # ISO 3166-1 alpha-2 country code
    iso_region: str  # ISO 3166-2 region code
    municipality: str  # City/town name
    scheduled_service: str  # yes/no (not used in our model)
    gps_code: str  # GPS code (not used in our model)
    iata_code: str  # IATA 3-letter code (may be empty)
    local_code: str  # Local airport code (not used in our model)
    home_link: str  # Website URL (not used in our model)
    wikipedia_link: str  # Wikipedia URL (not used in our model)
    keywords: str  # Keywords (not used in our model)


class AirportModelFields(TypedDict, total=False):
    """Type definition for Airport model fields."""

    ident: str
    iata_code: str
    name: str
    airport_type: str
    latitude_deg: float
    longitude_deg: float
    elevation_ft: int | None
    iso_country: str
    iso_region: str
    municipality: str
    country: "Country | None"
    city: "City | None"
    active: bool


# Field mapping from OurAirports CSV to Airport model
FIELD_MAPPING: dict[str, dict[str, str | bool | list[str]]] = {
    "ident": {
        "csv_field": "ident",
        "required": True,
        "description": "ICAO or local airport code, used as unique identifier",
        "example": "KDEN",
    },
    "iata_code": {
        "csv_field": "iata_code",
        "required": False,
        "description": "IATA 3-letter code, preferred for display",
        "example": "DEN",
        "validation": "3 uppercase letters or empty",
    },
    "name": {
        "csv_field": "name",
        "required": True,
        "description": "Airport name",
        "example": "Denver International Airport",
    },
    "airport_type": {
        "csv_field": "type",
        "required": False,
        "description": "Airport type category",
        "example": "large_airport",
        "values": ["large_airport", "medium_airport", "small_airport", "heliport", "closed", "seaplane_base", "balloonport"],
    },
    "latitude_deg": {
        "csv_field": "latitude_deg",
        "required": True,
        "description": "Latitude in decimal degrees",
        "example": "39.8561",
        "type": "float",
        "validation": "-90.0 to 90.0",
    },
    "longitude_deg": {
        "csv_field": "longitude_deg",
        "required": True,
        "description": "Longitude in decimal degrees",
        "example": "-104.6737",
        "type": "float",
        "validation": "-180.0 to 180.0",
    },
    "elevation_ft": {
        "csv_field": "elevation_ft",
        "required": False,
        "description": "Elevation in feet",
        "example": "5434",
        "type": "int",
        "nullable": True,
    },
    "iso_country": {
        "csv_field": "iso_country",
        "required": True,
        "description": "ISO 3166-1 alpha-2 country code",
        "example": "US",
        "validation": "2 uppercase letters",
    },
    "iso_region": {
        "csv_field": "iso_region",
        "required": False,
        "description": "ISO 3166-2 region code",
        "example": "US-CO",
    },
    "municipality": {
        "csv_field": "municipality",
        "required": False,
        "description": "City or town name",
        "example": "Denver",
    },
    "country": {
        "csv_field": "iso_country",
        "required": False,
        "description": "Normalized Country FK (apps.base.Country) derived from iso_country",
        "notes": "Created via AirportLocationIntegrator",
    },
    "city": {
        "csv_field": "municipality",
        "required": False,
        "description": "Normalized City FK (apps.base.City) derived from municipality + iso_country",
        "notes": "Created via AirportLocationIntegrator",
    },
    "active": {
        "csv_field": "type",
        "required": False,
        "description": "Boolean flag derived from airport type (closed airports become inactive)",
        "example": "True",
        "values": ["True", "False"],
    },
}


def normalize_csv_row(row: dict[str, str]) -> AirportModelFields:
    """
    Normalize a CSV row from OurAirports to Airport model fields.

    Transformations:
    - String coordinates → float with validation
    - String elevation → int or None
    - Empty strings → appropriate default values
    - Field name mapping (e.g., 'type' → 'airport_type')

    Args:
        row: Dictionary from CSV DictReader

    Returns:
        Dictionary ready for Airport.objects.update_or_create()

    Raises:
        ValueError: If required fields missing or invalid data types
    """
    # Parse numeric fields
    latitude = float(row["latitude_deg"])
    longitude = float(row["longitude_deg"])

    # Validate coordinate ranges
    if not (-90 <= latitude <= 90):
        raise ValueError(f"Invalid latitude: {latitude}")
    if not (-180 <= longitude <= 180):
        raise ValueError(f"Invalid longitude: {longitude}")

    # Parse optional elevation
    elevation: int | None = None
    if row.get("elevation_ft"):
        try:
            elevation = int(float(row["elevation_ft"]))
        except (ValueError, TypeError):
            pass  # Leave as None if invalid

    # Build normalized data
    normalized: AirportModelFields = {
        "ident": row["ident"],
        "name": row["name"],
        "airport_type": row.get("type", ""),
        "latitude_deg": latitude,
        "longitude_deg": longitude,
        "elevation_ft": elevation,
        "iata_code": row.get("iata_code", ""),
        "iso_country": row["iso_country"],
        "iso_region": row.get("iso_region", ""),
        "municipality": row.get("municipality", ""),
        "country": None,
        "city": None,
        "active": row.get("type", "").lower() != "closed",
    }

    return normalized


# Unmapped fields from OurAirports CSV (intentionally excluded)
UNMAPPED_FIELDS = [
    "id",  # OurAirports internal ID, not needed
    "continent",  # Can be derived from iso_country if needed
    "scheduled_service",  # Not relevant for MVP
    "gps_code",  # Redundant with ident/iata_code
    "local_code",  # Redundant with ident
    "home_link",  # URLs not in scope for MVP
    "wikipedia_link",  # URLs not in scope for MVP
    "keywords",  # Not needed for core functionality
]


# Sample mapping example for documentation
MAPPING_EXAMPLE: dict[str, dict[str, str | int | float]] = {
    "csv_input": {
        "id": "3462",
        "ident": "KDEN",
        "type": "large_airport",
        "name": "Denver International Airport",
        "latitude_deg": "39.861698150635",
        "longitude_deg": "-104.672996521",
        "elevation_ft": "5434",
        "continent": "NA",
        "iso_country": "US",
        "iso_region": "US-CO",
        "municipality": "Denver",
        "scheduled_service": "yes",
        "gps_code": "KDEN",
        "iata_code": "DEN",
        "local_code": "DEN",
        "home_link": "http://www.flydenver.com/",
        "wikipedia_link": "https://en.wikipedia.org/wiki/Denver_International_Airport",
        "keywords": "Denver",
    },
    "model_output": {
        "ident": "KDEN",
        "iata_code": "DEN",
        "name": "Denver International Airport",
        "airport_type": "large_airport",
        "latitude_deg": 39.861698150635,
        "longitude_deg": -104.672996521,
        "elevation_ft": 5434,
        "iso_country": "US",
        "iso_region": "US-CO",
        "municipality": "Denver",
    },
}
