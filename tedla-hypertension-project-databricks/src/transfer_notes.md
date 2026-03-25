
databricks fs --profile dev cp -r dbfs:/dbfs/tmp/note_data_2012_to_2013_parquet /mnt/z/_/data/project_data/tedla/note_data_2012_to_2013_parquet &&

scp -r /mnt/z/_/data/project_data/tedla/note_data_2012_to_2013_parquet lambda-server:/var/nfs_share/workspaces/ciphi/westerd/tedla/tedla/note_data_2012_to_2013_parquet

