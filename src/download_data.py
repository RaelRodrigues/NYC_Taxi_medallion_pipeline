"""
download_data.py

Downloads the NYC Yellow Taxi trip data (Jan-Jun 2023 and Jan-Jun 2024) plus
the taxi zone lookup table from the NYC TLC's public website, and saves
everything into data/raw/.

Usage:
    python src/download_data.py
"""

from pathlib import Path

import requests

# This file lives in <project_root>/src/download_data.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
ZONE_LOOKUP_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

YEARS = [2023, 2024]
MONTHS = range(1, 7)  # January through June


def download_file(url: str, file_name: str) -> None:
    """Download one file from `url` and save it as `file_name` in data/raw/."""
    destination = RAW_DATA_DIR / file_name

    if destination.exists():
        print(f"Already downloaded: {file_name}")
        return

    print(f"Downloading {file_name} ...")
    response = requests.get(url)
    response.raise_for_status()

    with open(destination, "wb") as f:
        f.write(response.content)

    print(f"Saved {file_name}")


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Download each month of trip data for each year
    for year in YEARS:
        for month in MONTHS:
            file_name = f"yellow_tripdata_{year}-{month:02d}.parquet"
            url = f"{BASE_URL}/{file_name}"
            download_file(url, file_name)

    # Download the zone lookup table
    download_file(ZONE_LOOKUP_URL, "taxi_zone_lookup.csv")

    print("\nAll files downloaded to data/raw/")


if __name__ == "__main__":
    main()