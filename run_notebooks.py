#!/usr/bin/env python3
"""
Script 2: Sequential Notebook Runner (run_notebooks.py)

Executes all six Jupyter notebooks in sequential order to reproduce the
data cleaning, reference-free hygroscopic calibration, and indoor PM2.5
forecasting pipeline.
"""

import os
import sys
import time
import nbformat
from nbclient import NotebookClient

NOTEBOOKS = [
    "phase_0_data_preparation.ipynb",
    "phase_1.1_data_exploration_and_training_pool.ipynb",
    "phase_1.2_calibration_modelling_and_tuning.ipynb",
    "phase_1.3_calibration_production.ipynb",
    "phase_2.1_forecasting_exploration.ipynb",
    "phase_2.2_production.ipynb",
]


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    notebooks_dir = os.path.join(root_dir, "notebooks")

    node_raw_dir = os.path.join(root_dir, "data", "01_raw", "node_data")
    expected_first_file = os.path.join(node_raw_dir, "node_1_filtered.csv")
    if not os.path.exists(expected_first_file):
        sys.exit(
            "Error: Filtered raw data not found in data/01_raw/node_data/.\n"
            "Please run 'python prepare_data.py' first."
        )

    total_start = time.time()
    print(f"Starting sequential execution of {len(NOTEBOOKS)} notebooks...\n")

    for idx, nb_name in enumerate(NOTEBOOKS, start=1):
        nb_path = os.path.join(notebooks_dir, nb_name)
        if not os.path.exists(nb_path):
            sys.exit(f"Error: Notebook not found at {nb_path}")

        print(f"[{idx}/{len(NOTEBOOKS)}] Executing {nb_name}...")
        step_start = time.time()

        with open(nb_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        client = NotebookClient(
            nb,
            timeout=-1,
            kernel_name="python3",
            resources={"metadata": {"path": notebooks_dir}},
        )
        client.execute()

        with open(nb_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)

        elapsed = time.time() - step_start
        print(f"    Completed {nb_name} in {elapsed:.1f}s.\n")

    total_elapsed = time.time() - total_start
    print(f"All notebooks executed successfully in {total_elapsed / 60:.1f} minutes.")


if __name__ == "__main__":
    main()
