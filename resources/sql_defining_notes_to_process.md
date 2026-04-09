# SQL to Build CSV File

## Overview

The SQL contained within this document targets Microsoft SQL Server with
table names from the OMOP common data model.  The source tables used in
this document correspond to the following:

Table names in your local database may differ slightly, requiring an update
to the scripts.

## Workflow

This document describes SQL to perform the following workflow within your
SQL environment:

- Ensure the patient cohort exists as a table in the database, such that each
  patient is identified with the unique id for patients present in other tables
  (i.e., person_id),
- Identify the notes associated with the patient cohort,
- Identify Visits associated with the identified notes,
- Define each note group,
- Create list of note ids for the NLP pipeline,
- Create final table with inputs for NLP pipeline, and
- Export to CSV files for use with NLP tool.

## SQL Scripts

### Source Tables

#### Patient Cohort Table

This code assumes that you already have a patient cohort with at minimum a
unique id for each patient as used by other tables in the system.  This SQL
assumes the name of this table to be `cohort`.

The cohort table should contain eligible individuals identified from the structured
data that has already been shared with VUMC, and the cohort table should include
both MRN and person_id. The person_id should be the same ID used when sharing the
structured data so that we can merge the NLP data with the structured dataset.

```sql
-- The list of patients in the cohort
select  person_id
        , mrn -- link to eligible participants in local dataset
from cohort with (nolock)
```

#### NLP Export Data

Create the table, `nlp_data_export`, containing the data to export for
NLP processing using patient cohort notes and supporting features for
note dates from `1/1/2010` to `12/31/2024`.

The following queries combines all the logic to create this table into
one query for simplicity.  It is recommended, however, that if possible
each of these CTEs (Common Table Expression) used within the query be
created as individual tables, such that your local database administrator
can build appropriate indexes to facilitate efficient querying.

##### SQL to create NLP Export

```sql
-- Patient Cohort
with cte_cohort as (
    select  person_id
            , mrn -- link to eligible participants in local dataset
    from cohort with (nolock)
)
-- Notes linked to Patients
, cte_notes as (
    SELECT  n.note_id
            , n.person_id
            , LOWER(n.note_title) AS note_title
            -- id referencing a specific note type; may not be present
            -- or may be actual text in your system
            , n.note_type_concept_id 
            , n.provider_id
            , n.note_date
            , n.visit_occurrence_id
            -- text describing note origin; may have different meaning
            -- in your system and thus optional
            , LOWER(n.note_source_value) AS note_source_value
    FROM note n with (nolock)
        INNER JOIN cohort c with (nolock)
            ON n.person_id = c.person_id
    WHERE n.note_date BETWEEN '2010-01-01' AND '2024-12-31'
)
-- Visits linked to Notes
, cte_visits as (
    SELECT  v.visit_occurrence_id
            , v.visit_concept_id
            , v.person_id
            , v.discharge_to_concept_id
            , v.provider_id
            , v.visit_start_date
            , v.visit_end_date
            , v.visit_source_value
    FROM cte_notes n
        INNER JOIN visit_occurrence v with (nolock)
            ON n.visit_occurrence_id = v.visit_occurrence_id
    WHERE notes.visit_occurrence_id IS NOT NULL
)
-- Features used to define Note Groups
, cte_note_features as (
    SELECT  n.note_id
            , n.person_id
            , n.note_type_concept_id
            , n.note_title
            , n.note_source_value
            , v.visit_concept_id
    FROM cte_notes n
        LEFT JOIN cte_visits v
            ON n.visit_occurrence_id = v.visit_occurrence_id
)
-- Admission Note Group
, cte_admission_note_group as (
    SELECT note_id
    FROM cte_note_features
    WHERE (
        CHARINDEX('admission', note_source_value) > 0
        OR CHARINDEX('admission', note_title) > 0
    )
)
-- Communication Encounter Notes Group
, cte_communication_encounter_notes_group AS (
    SELECT note_id
    FROM cte_note_features
    WHERE CHARINDEX('communication', note_title) > 0
)
-- Discharge Summary Notes Group
, cte_discharge_summary_notes_group AS (
    SELECT note_id
    FROM cte_note_features
    WHERE (
        note_source_value IN ('discharge summary')
        OR CHARINDEX('discharge summary', note_title) > 0
    )
)
-- ECG Impression Notes Group
, cte_ecg_impression_notes_group AS (
    SELECT note_id
    FROM cte_note_features
    WHERE note_title LIKE '%ecg%impression%'
)
-- ED Notes Group
, cte_emergency_department_notes_group AS (
    SELECT note_id
    FROM cte_note_features
    WHERE (
        CHARINDEX('emergency', note_source_value) > 0
        OR CHARINDEX('emergency', note_title) > 0
    )
)
-- Inpatient Notes Group
, cte_inpatient_notes_group AS (
    SELECT note_id
    FROM cte_note_features
    WHERE CHARINDEX('inpatient', note_title) > 0
)
-- Outpatient Notes Group
, cte_outpatient_notes_group AS (
    SELECT note_id
    FROM cte_note_features
    WHERE CHARINDEX('outpatient', note_title) > 0
)
-- Problem Lists Notes Group
, cte_problem_list_notes_group AS (
    SELECT note_id
    FROM cte_note_features
    -- This is an OMOP-specific definition; you will need
    -- to adjust this to match your local definition for
    -- for problem lists
    WHERE note_type_concept_id IN (2002404173, 2002603124)
)
, cte_note_ids_to_process_with_nlp AS (
    SELECT note_id, note_group_id
    FROM (
        SELECT note_id, note_group_id FROM (
            SELECT note_id, CAST (1 AS TINYINT) as note_group_id FROM cte_admission_note_group
            UNION ALL
            SELECT note_id, CAST (2 AS TINYINT) as note_group_id FROM cte_communication_encounter_notes_group
            UNION ALL
            SELECT note_id, CAST (3 AS TINYINT) as note_group_id FROM cte_discharge_summary_notes_group
            UNION ALL
            SELECT note_id, CAST (4 AS TINYINT) as note_group_id FROM cte_ecg_impression_notes_group
            UNION ALL
            SELECT note_id, CAST (5 AS TINYINT) as note_group_id FROM cte_emergency_department_notes_group
            UNION ALL
            SELECT note_id, CAST (6 AS TINYINT) as note_group_id FROM cte_inpatient_notes_group
            UNION ALL
            SELECT note_id, CAST (7 AS TINYINT) as note_group_id FROM cte_outpatient_notes_group
            UNION ALL
            SELECT note_id, CAST (8 AS TINYINT) as note_group_id FROM cte_problem_list_notes_group
        )
    )
    GROUP BY note_id , note_group_id;
)
, cte_patient_communications as (
    SELECT note_id
    FROM cte_note_features N
    WHERE (
        CHARINDEX('message', note_class_source_value) > 0
        OR CHARINDEX('letter', note_class_source_value) > 0
        OR CHARINDEX('portal', note_class_source_value) > 0
    )
    UNION ALL
    SELECT note_id
    FROM cte_visits
    WHERE (
        CHARINDEX('phone', visit_source_value) > 0
        OR CHARINDEX('portal', visit_source_value) > 0
    )
)
, cte_nlp_data as (
    SELECT  n.note_id
            , n.person_id
            , n.note_text
            , n.note_date
            , v.visit_occurrence_id
            , v.visit_start_date
            , v.visit_end_date
            , pc.is_patient_communication
            , CASE
                WHEN n.note_date BETWEEN (v.visit_start_date, v.visit_end_date) THEN 
                    CAST(1 AS BIT)
                ELSE
                    CAST(0 AS BIT) 
                END
                AS note_within_visit
            -- VUMC-specific use; NLP expect value, setting to default
            , 1 as x_part_num
            -- VUMC-specific use; NLP expect value, setting to default
            , '' as x_uniq
    FROM cte_note_features n
        LEFT JOIN cte_visits V
            ON n.visit_occurrence_id = v.visit_occurrence_id
        LEFT JOIN cte_patient_communications pc
            on n.note_id = pc.note_id
)
SELECT  IDENTITY(INT, 1, 1) AS data_id
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
INTO nlp_data_export
FROM cte_nlp_data
```

##### Export NLP Data to CSV

Given that a user must have permission to run the stored procedure `xp_cmdshell` as well
as know how to use the `bcp` utility, we have provided a PowerShell script to perform
the export.  Powershell is avaialble by default on Windows machines.  The following
Instructions provide details on how run the PowerShell script, `nlp_export.ps1`.

This will create a series of CSV files with prefixed by a number (e.g., `1_nlp_data_export.csv`, 
`2_nlp_data_export.csv`, etc.) in the folder to specify in the script.

**Note**: A copy of this PowerShell script has been provided at 
`resources\nlp_export.ps1`.  


**Instructions**

1. Copy the following to a PowerShell script named `nlp_export.ps1` on the computer
where you will be exporting the data to CSVs.
2. Open a powershell console (Windows Key + R, type powershell.exe, and hit <enter>)
3. Make sure the `SqlServer` PowerShell module is installed
```powershell
Install-Module -Name SqlServer -Scope CurrentUser -Force
```
4. Within the PowerShell console, change directory into the folder containing
   the script and type `./nlp_export.ps1` to start the export.

**Note:**  You will need to edit the file, setting the values for your SQL
Server database, export folder, and batch size.

> ```
> $server      = "YOUR_SERVER_NAME"
> $database    = "YOUR_DATABASE_NAME"
> $exportPath  = "C:\path\to\export\folder"
> $batchSize   = 10000
> ```


**`nlp_export.ps1`** PowerShell Export Script

```powershell
# ---------------------------------------------------------------------------
# Configuration — update these values for your environment
# ---------------------------------------------------------------------------
$server      = "YOUR_SERVER_NAME"
$database    = "YOUR_DATABASE_NAME"
$exportPath  = "C:\path\to\export\folder"
$batchSize   = 10000

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
```






