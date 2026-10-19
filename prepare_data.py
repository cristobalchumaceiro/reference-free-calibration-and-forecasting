#!/usr/bin/env python3
"""
Script 1: Data Acquisition & Filtering (prepare_data.py)

Clones the raw QMUL Air Quality Monitoring System (AQMS) repository, pulls the
required subset of low-cost node and reference station CSVs via Git LFS, applies
temporal and column filtering (2025-04-16 to 2026-06-10 inclusive), and exports
the filtered files into `data/01_raw/`.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import pandas as pd

REPO_URL = "https://github.com/AndresMercad0/qm-airquality-network-data.git"
RELEASE_TAG = "v1.0.1"

NODES = ["node_1", "node_2", "node_3", "node_4", "node_6", "node_7"]
REF_STATIONS = ["node_TH2_MER"]

START_TIMESTAMP = "2025-04-16T00:00:00Z"
END_TIMESTAMP = "2026-06-10T23:59:59Z"

NODE_COLUMNS = [
    "timestamp_utc",
    "node_id",
    "site",
    "subsite",
    "exposure",
    "environment",
    "latitude",
    "longitude",
    "temperature_low_sht45_celsius",
    "humidity_low_sht45_percentage",
    "pm2_5_low_sps30_ug_m3",
    "pm10_low_sps30_ug_m3",
]

REF_COLUMNS = [
    "timestamp_utc",
    "node_id",
    "site",
    "subsite",
    "exposure",
    "environment",
    "latitude",
    "longitude",
    "pm2_5_high_met_one_ug_m3",
]


def check_prerequisites():
    """Verify that git and git-lfs are installed and available on PATH."""
    if shutil.which("git") is None:
        sys.exit("Error: 'git' is not installed or not found on PATH.")
    try:
        subprocess.run(
            ["git", "lfs", "version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        sys.exit(
            "Error: 'git-lfs' is required to download the raw datasets. "
            "Please install Git LFS (https://git-lfs.com/) and run 'git lfs install'."
        )


def filter_and_save_csv(src_path, dest_path, columns):
    """Read raw CSV, restrict to study date window and target columns, and save."""
    df = pd.read_csv(src_path, usecols=columns)[columns]
    mask = (df["timestamp_utc"] >= START_TIMESTAMP) & (
        df["timestamp_utc"] <= END_TIMESTAMP
    )
    df_filtered = df.loc[mask]
    df_filtered.to_csv(dest_path, index=False)
    return len(df_filtered)


def main():
    check_prerequisites()

    root_dir = os.path.dirname(os.path.abspath(__file__))
    node_out_dir = os.path.join(root_dir, "data", "01_raw", "node_data")
    ref_out_dir = os.path.join(root_dir, "data", "01_raw", "reference_data")

    os.makedirs(node_out_dir, exist_ok=True)
    os.makedirs(ref_out_dir, exist_ok=True)

    lfs_paths = [f"data/{node}.csv" for node in NODES] + [
        f"data/reference/{ref}.csv" for ref in REF_STATIONS
    ]
    lfs_include_arg = f"--include={','.join(lfs_paths)}"

    with tempfile.TemporaryDirectory(prefix="qmul_aqms_") as tmp_dir:
        print(f"1. Cloning {REPO_URL} at release {RELEASE_TAG} (skipping initial LFS smudge)...")
        env = os.environ.copy()
        env["GIT_LFS_SKIP_SMUDGE"] = "1"
        subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", RELEASE_TAG, REPO_URL, tmp_dir],
            check=True,
            env=env,
        )

        print("2. Pulling required dataset files via Git LFS...")
        subprocess.run(
            ["git", "-C", tmp_dir, "lfs", "pull", lfs_include_arg],
            check=True,
        )

        print("3. Filtering and exporting low-cost node datasets...")
        for node in NODES:
            src_csv = os.path.join(tmp_dir, "data", f"{node}.csv")
            dest_csv = os.path.join(node_out_dir, f"{node}_filtered.csv")
            row_count = filter_and_save_csv(src_csv, dest_csv, NODE_COLUMNS)
            print(f"   Saved {node}_filtered.csv ({row_count:,} rows)")

        print("4. Filtering and exporting reference station dataset...")
        for ref in REF_STATIONS:
            src_csv = os.path.join(tmp_dir, "data", "reference", f"{ref}.csv")
            dest_csv = os.path.join(ref_out_dir, f"{ref}_filtered.csv")
            row_count = filter_and_save_csv(src_csv, dest_csv, REF_COLUMNS)
            print(f"   Saved {ref}_filtered.csv ({row_count:,} rows)")

    print("\nData preparation complete. All raw files are ready in data/01_raw/.")


if __name__ == "__main__":
    main()
