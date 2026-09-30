#!/usr/bin/env python3

"""
Generate a list of filenames and paths in a collection.
This script reads a CSV file containing file inventory data, filters it for a specified collection, and outputs a CSV file with the filenames and their paths.

The user can specify the collection abbreviation with the --collection argument. The output CSV file will be named based on the collection abbreviation.

Requires:
- argparse
- csv
- pandas
- Pathlib

Author: Samuel J Huskey
Date: 2026-09-29
"""

import argparse
import csv
import pandas as pd
from pathlib import Path

# Define default values
DEFAULT_INVENTORY_FILE = "file_inventory.csv"

DEFAULT_FILE_TYPES = [
    ".wav",
    ".pdf",
    ".eaf",
    ".xml",
    ".docx",
    ".mov",
    ".mp4",
    ".txt",
    ".pptx",
    ".fwbackup",
    ".tar",
]


def make_collection_frame(collection_name, df):
    # Filter the DataFrame for the specified collection
    collection_df = df[df["collection_abbr"] == collection_name]
    collection_df = collection_df[["filename", "full_path"]]

    return collection_df


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Generate a list of filenames and paths in a collection."
    )
    parser.add_argument(
        "--collection",
        type=str,
        required=True,
        help="Collection abbreviation (e.g., CAR, LAR, etc.)",
    )
    parser.add_argument(
        "--inventory_file",
        type=str,
        default=DEFAULT_INVENTORY_FILE,
        help="Path to the file inventory CSV file",
    )

    args = parser.parse_args()

    # Read the inventory CSV file
    df = pd.read_csv(args.inventory_file)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(DEFAULT_INVENTORY_FILE)

    # Extract the collection name from the full_path and create a new column 'collection'
    df["collection"] = df["full_path"].apply(
        lambda x: Path(x).parts[6] if len(Path(x).parts) > 6 else None
    )

    # Create a new column 'collection_abbr' that contains the first three characters of the collection name
    df["collection_abbr"] = df["collection"].apply(
        lambda x: x[:3] if pd.notnull(x) else None
    )

    # Create a new column 'file_type' that contains the file extension
    df["file_type"] = df["filename"].apply(
        lambda x: Path(x).suffix if pd.notnull(x) else None
    )

    # Drop rows where 'file_type' is not in the list of DEFAULT_FILE_TYPES
    df = df[df["file_type"].isin(DEFAULT_FILE_TYPES)]

    # Drop rows where 'filename' begings with a dot (hidden files)
    df = df[~df["filename"].str.startswith(".")]

    # Keep only the relevant columns
    df = df[["collection", "collection_abbr", "filename", "file_type", "full_path"]]

    # Filter the DataFrame for the specified collection
    collection_df = make_collection_frame(args.collection, df)

    # Create output filename based on collection abbreviation
    output_filename = f"{args.collection}_file_list.csv"

    # Save the filtered DataFrame to a new CSV file
    collection_df.to_csv(output_filename, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8")
    print(f"File list for collection '{args.collection}' saved to '{output_filename}'.")


if __name__ == "__main__":
    main()
