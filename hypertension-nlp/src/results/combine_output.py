import sqlite3
from pathlib import Path
import argparse


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


if __name__ == "__main__":
    """
    Output is produced in a series of SQLite databases, one per worker process.
    This script combines the output into a single database and produces some summary statistics.
    """

    # parser = argparse.ArgumentParser(description="Combine SQLite result databases into one.")
    # parser.add_argument("--input", required=True, help="Path to the folder containing result .db files")
    # parser.add_argument("--output", required=True, help="Path to the combined output .db file")
    # args = parser.parse_args()

    # results_folder = Path(args.input)
    # combined_db_path = Path(args.output)

    results_folder = Path(
        r"Z:\_\active\nlpssc\Tedla - VUMC\nlp_Tdla\tedla-shared-NLP\output\imported_output\results\results_20260325_103310"
    )
    combined_db_path = Path(
        r"Z:\_\active\nlpssc\Tedla - VUMC\nlp_Tdla\tedla-shared-NLP\output\imported_output\results\combined"
    ) / f"combined_{results_folder.name}.db"


    results_dbs = list(results_folder.glob("*.db"))

    results_table_name = "results"

    # iterate over results_dbs and combine into a single database

    expected_table_columns = []
    results_counts = {}

    # Create the combined database and the results table if it doesn't exist
    with sqlite3.connect(combined_db_path) as combined_conn:
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
        print(f"Row count mismatch! Total rows from results: {total_rows_from_results}, total rows in combined: {total_rows_in_combined}")
    else:
        print(f"Row count matches! Total rows: {total_rows_in_combined}")
