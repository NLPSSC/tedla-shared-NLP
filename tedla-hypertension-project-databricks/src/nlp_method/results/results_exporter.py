import csv
import os
from pathlib import Path
from typing import Literal
from nlp_method.results.datastore.results_data_store import ResultsDataStore


class ResultsExporter:

    def __init__(self) -> None:
        self._results_data_store: ResultsDataStore = ResultsDataStore()

    def export_as(self, file_name: str, export_type: Literal["csv", "parquet"]):
        if export_type == "csv":
            self._export_as_csv(file_name)
        elif export_type == "parquet":
            self._export_as_parquet(file_name)
        else:
            raise ValueError(f"Unsupported export type: {export_type}")

    def _export_as_csv(self, file_name: str):
        if len(file_name) < 5:
            raise ValueError("File name must be at least 5 characters long.")

        export_folder = os.getenv("EXPORT_DIR", None)
        if export_folder is None:
            raise ValueError("EXPORT_DIR environment variable is not defined.")

        export_folder = Path(export_folder)
        export_folder.mkdir(parents=True, exist_ok=True)

        export_path: Path = export_folder / f"{file_name}.csv"
        if export_path.exists():
            raise FileExistsError(f"File already exists: {export_path}")

        writer = None
        with export_path.open(mode="w") as fh:
            for chunk in self._results_data_store.chunk_iter(10000):
                if writer is None:
                    writer = csv.DictWriter(fh, fieldnames=chunk[0].keys())
                if fh.tell() == 0:  # Write header only once
                    writer.writeheader()
                writer.writerows(chunk)

    def _export_as_parquet(self, file_name: str):
        raise NotImplementedError("Parquet export is not implemented yet.")


if __name__ == "__main__":

    exporter = ResultsExporter()

    exporter.export_as("sample_results", "csv")
