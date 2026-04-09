# ---------------------------------------------------------------------------
# Configuration — update these values for your environment
#
# Note: Please ensure that the value of $batchSize is set appropriately for
# your system's memory and performance capabilities. A larger batch size may
# reduce the number of files generated but could increase memory usage, 
# processing time, and affect the responsiveness of the SQL Server (impacting
# other users). Conversely, a smaller batch size may generate more files but
# will typically use less memory and allow for quicker processing of each batch.
# ---------------------------------------------------------------------------
$server      = "YOUR_SERVER_NAME"
$database    = "YOUR_DATABASE_NAME"
$exportPath  = "C:\path\to\export\folder"
$batchSize   = 100000
$batchIndex  = 1

# Use Windows integrated auth. For SQL auth, add:
#   -Username "sa" -Password "your_password" -TrustServerCertificate
$connParams = @{
    ServerInstance = $server
    Database       = $database
}

# ---------------------------------------------------------------------------
# Export loop
# ---------------------------------------------------------------------------
while ($true) {

    $offset = ($batchIndex - 1) * $batchSize

    $query = @"
SELECT  data_id
      , note_id
      , person_id
      , note_text
      , note_date
      , visit_occurrence_id
      , visit_start_date
      , visit_end_date
      , is_patient_communication
      , note_within_visit
      , x_part_num
      , x_uniq
FROM nlp_data_export
ORDER BY data_id
OFFSET $offset ROWS
FETCH NEXT $batchSize ROWS ONLY;
"@

    try {
        $rows = Invoke-Sqlcmd @connParams -Query $query -ErrorAction Stop
    }
    catch {
        Write-Error "Query failed on batch $batchIndex`: $_"
        exit 1
    }

    # If no rows returned, export is complete.
    if (-not $rows -or $rows.Count -eq 0) {
        Write-Host "Export complete. $(($batchIndex - 1)) batch(es) exported."
        break
    }

    $csvPath = Join-Path $exportPath "${batchIndex}_nlp_data_export.csv"

    try {
        $rows | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8 -ErrorAction Stop
        Write-Host "Batch $batchIndex`: $($rows.Count) rows -> $csvPath"
    }
    catch {
        Write-Error "Failed to write CSV for batch $batchIndex`: $_"
        exit 1
    }

    $batchIndex++
}