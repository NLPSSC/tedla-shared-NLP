import pyarrow.parquet as pq

dataset_path = "/home/westerd/_/project_data/tedla-hypertension/source_data/cohort_note_visit_details"
dataset = pq.ParquetDataset(dataset_path)
columns = dataset.schema.names
print(columns)