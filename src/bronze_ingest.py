## Bronze_ingest.py

from pathlib import Path                            # a way to work with file paths
import pandas as pd
from deltalake import write_deltalake, DeltaTable   # to write and read Delta Lake tables

# build paths starting from this script's own location (not from wherever the terminal happens to be),
# so the script works correctly no matter where you run it from
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# folder where the raw parquet files live
data_dir = PROJECT_ROOT / "data" / "raw"

# where the Bronze layer Delta table will be created
delta_path = PROJECT_ROOT / "data" / "delta" / "bronze_trips"

# enumerate() gives us both the loop position (i) and the file path,
# so we know whether this is the first file (i == 0) or a later one
for i, path in enumerate(data_dir.glob("yellow_tripdata_*.parquet")):

    # split the file name by "_" to isolate the date part
    # e.g. "yellow_tripdata_2023-01.parquet" -> ["yellow", "tripdata", "2023-01.parquet"]
    piece = path.name.split("_")

    # take the last piece, which contains the date + file extension
    data_ = piece[-1]

    # remove ".parquet" from the end, leaving just "2023-01"
    year_month = data_.replace(".parquet", "")

    # load the actual trip data from this file into a DataFrame
    df = pd.read_parquet(path)

    # standardize all column names to lowercase
    df.columns = df.columns.str.lower()

    # add a new column showing which year/month this file represents
    df["year-month"] = year_month

    # on the first file (i == 0), create the Delta table from scratch
    # on every file after that, append rows to the table that already exists
    # this avoids loading all 12 months into memory at once, each file is written and then discarded before moving to the next one
    if i == 0:
        write_deltalake(delta_path, df, mode="overwrite")
    else:
        write_deltalake(delta_path, df, mode="append")

    print(f"[{i}] {path.name} escrito na tabela Delta")