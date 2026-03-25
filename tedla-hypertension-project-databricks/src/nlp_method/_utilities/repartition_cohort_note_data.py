import os
import pyarrow as pa
import pyarrow.dataset as ds

cohort_note_data_path = "/home/westerd/_/project_data/tedla-hypertension/source_data/cohort_note_data"
cohort_note_data_batched_path = f"{cohort_note_data_path}_batched"
note_id_to_note_groups_path = "/home/westerd/_/project_data/tedla-hypertension/source_data/note_id_to_note_groups"

# Load your existing dataset (replace with your actual path)
input_dataset = ds.dataset(cohort_note_data_path, format="parquet")

# Define the output path for the repartitioned dataset
output_path = cohort_note_data_batched_path
os.makedirs(output_path, exist_ok=True)

# Repartition by 'batch_group' (this creates subdirectories like batch_group=1, batch_group=2, etc.)
ds.write_dataset(
    input_dataset,
    output_path,
    format="parquet",
    partitioning=["batch_group"],  # Partition on this column
    use_threads=True,  # Enable multi-threading for speed
    # max_rows_per_file=100000,  # Optional: Control file size for better performance
)

print("Repartitioning complete.")