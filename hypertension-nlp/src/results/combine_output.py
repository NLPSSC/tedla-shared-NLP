import sqlite3
from pathlib import Path
import argparse

COMBINED_OUTPUT_FOLDER = "combined_output"


def create_destination_table(
    results_table_name,
    expected_table_columns,
    combined_conn,
    combined_cursor,
    results_cursor,
):
    if not expected_table_columns:
        results_cursor.execute(f"PRAGMA table_info({results_table_name})")
        columns_info = results_cursor.fetchall()
        expected_table_columns = [col[1] for col in columns_info]
        columns_def = ", ".join([f"{col[1]} {col[2]}" for col in columns_info])
        table_create_cmd = (
            f"CREATE TABLE IF NOT EXISTS {results_table_name} ({columns_def})"
        )
        combined_cursor.execute(table_create_cmd)
        combined_conn.commit()
    return expected_table_columns


def combine_databases(
    create_destination_table, individual_results_folder, combined_output_path
):
    results_folder = Path(individual_results_folder)
    combined_db_path = Path(combined_output_path)

    combined_db_path.mkdir(parents=True, exist_ok=True)

    combined_db_path = combined_db_path / f"combined_{results_folder.name}.db"

    results_dbs = list(results_folder.glob("*.db"))

    results_table_name = "results"

    # iterate over results_dbs and combine into a single database

    expected_table_columns = []
    results_counts = {}

    # Create the combined database and the results table if it doesn't exist

    try:
        combined_conn = sqlite3.connect(combined_db_path)
    except sqlite3.OperationalError as e:
        print(f"Error creating combined database at {combined_db_path}: {e}")
        exit(1)

    with combined_conn:
        combined_cursor = combined_conn.cursor()
        # Get the schema from the first results db
        with sqlite3.connect(results_dbs[0]) as first_conn:
            for results_idx, results_db in enumerate(results_dbs):
                results_counts[results_idx] = 0
                with sqlite3.connect(results_db) as results_conn:
                    results_cursor = results_conn.cursor()

                    expected_table_columns = create_destination_table(
                        results_table_name,
                        expected_table_columns,
                        combined_conn,
                        combined_cursor,
                        results_cursor,
                    )

                    results_cursor.execute(
                        f"SELECT {', '.join(expected_table_columns)} FROM {results_table_name}"
                    )

                    while True:
                        rows = results_cursor.fetchmany(1000)
                        results_counts[results_idx] += len(rows)
                        if not rows:
                            break

                        combined_cursor.executemany(
                            f"INSERT INTO {results_table_name} ({', '.join(expected_table_columns)}) VALUES ({', '.join(['?'] * len(expected_table_columns))})",
                            rows,
                        )
                        combined_conn.commit()

    total_rows_from_results = sum(results_counts.values())
    with sqlite3.connect(combined_db_path) as combined_conn:
        combined_cursor = combined_conn.cursor()
        combined_cursor.execute(f"SELECT COUNT(*) FROM {results_table_name}")
        total_rows_in_combined = combined_cursor.fetchone()[0]

    if total_rows_from_results != total_rows_in_combined:
        print(
            f"Row count mismatch! Total rows from results: {total_rows_from_results}, total rows in combined: {total_rows_in_combined}"
        )
    else:
        print(f"Row count matches! Total rows: {total_rows_in_combined}")


if __name__ == "__main__":
    """
    Output is produced in a series of SQLite databases, one per worker process.
    This script combines the output into a single database and produces some summary statistics.
    """

    parser = argparse.ArgumentParser(
        description="Combine SQLite result databases into one."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the folder containing result .db files"
    )
    parser.add_argument(
        "--output",
        required=False,
        help=(
            f"Path to the folder for the combined output .db file. If not provided, "
            f'a "{COMBINED_OUTPUT_FOLDER}" folder will be created in the input folder.'
        ),
    )
    args = parser.parse_args()

    if not args.input:
        print("Error: --input argument is required.")
        parser.print_help()
        exit(1)

    individual_results_folder = Path(args.input)
    if individual_results_folder.exists() and individual_results_folder.is_dir():
        print(f"Found input folder: {individual_results_folder}")
    else:
        print(
            f"Input folder {individual_results_folder} does not exist or is not a directory."
        )
        exit(1)

    if args.output:
        combined_output_path = Path(args.output)
        if not combined_output_path.exists():
            print(
                f"Output path {combined_output_path} does not exist. It will be created."
            )
        elif not combined_output_path.is_dir():
            print(f"Output path {combined_output_path} exists but is not a directory.")
            exit(1)
    else:

        combined_output_path = individual_results_folder / COMBINED_OUTPUT_FOLDER
        combined_output_path.mkdir(parents=True, exist_ok=True)
        print(f"No output path provided. Using default: {combined_output_path}")

    combine_databases(
        create_destination_table, individual_results_folder, combined_output_path
    )
