#!/usr/bin/bash

start_year=$1

if [[ -z "$start_year" ]]; then
    echo "Error: start_year argument is required."
    exit 1
fi

if ! [[ "$start_year" =~ ^[0-9]+$ ]]; then
    echo "Error: start_year must be a number."
    exit 1
fi

if (( start_year < 2015 || start_year > 2024 )); then
    echo "Error: start_year must be between 2015 and 2024."
    exit 1
fi

end_year=$((start_year + 1))

data_source=note_data_${start_year}_to_${end_year}_parquet
local_target=/mnt/z/_/data/project_data/tedla
remote_target=/var/nfs_share/workspaces/ciphi/westerd/tedla/tedla

databricks fs \
    --profile dev \
    cp \
    -r dbfs:/dbfs/tmp/$data_source $local_target/$data_source && \
scp -r \
    $local_target/$data_source \
    lambda-server:$remote_target/$data_source