import pyarrow.parquet as pq

dataset_path = "cohort_note_visit_details"
dataset = pq.ParquetDataset(dataset_path)
columns = dataset.schema.names
print(columns)