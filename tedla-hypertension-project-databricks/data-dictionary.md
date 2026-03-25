<style>
    body {
        font-family: 'Segoe UI', 'Arial', 'Helvetica Neue', Helvetica, sans-serif;
    }
    table td,th {
        font-size: .75em;
        padding-left: 5px;
        padding-bottom: 5px;
        padding-top: 5px;
        padding-right: 5px;
    }
    table th {
        text-align: center;
    }
    table td:last-child, th:last-child {
        vertical-align: top;
    }
    
    table tr:nth-child(even) td {
        background-color: #f5f5f5;
    }
    table tr:nth-child(odd) td {
        background-color: transparent;
    }
    table, th, td {
        border: solid 1px black;
        border-collapse: collapse;
    }
    div.footnote_container {
        margin-top: 10px
    }
    div.footnote {
        font-size: .8em;
        margin: 10px 0 0 0
    }
</style>

# Data Dictionary

The following describes the columns within the dataset, the data types, and a description for each column.

| Feature | Valid Values | Data Type | Description |
|---|:---:|:---:|---|
| note_id |  | integer | The unique id for the note in the RD |
| patient_id |  | integer | The unique id for the patient in the RD (not MRN) |
| search_term |  | string | The search term found |
| is_negated | 0/1 | boolean | If True, indicates negative assertion (i.e., "doa" string was found, but the window text contains "was not doa") |
| window_text |  | string | The text surrounding the search term (+/- 20 tokens) |
| note_date | ISO format<sup>2</sup> | date | The note date as asserted in the source |
| is_patient_communication<sup>1</sup> | 0/1 | boolean | The note is related to patient communications (e.g., messaging, phone communication, etc.) |
| is_note_within_visit | 0/1 | boolean | Given visit, $V$, with start and end date,<br/> $V_s$ and $V_e$, then<br/>1 if $V_s \leq$ note\_date $\leq V_e$, 0 otherwise |
| problem_list_notes_group | 0/1 | boolean | Note is part of "Problem List" Group |
| outpatient_notes_group | 0/1 | boolean | Note is part of "Outpatient Notes" Group |
| communication_encounter_notes_group | 0/1 | boolean | Note is part of "Communication Encounter Notes" Group |
| inpatient_notes_group | 0/1 | boolean | Note is part of "Inpatient Notes" Group |
| admission_notes_group | 0/1 | boolean | Note is part of "Admission Notes" Group |
| emergency_department_notes_group | 0/1 | boolean | Note is part of "Emergency Department Notes" Group |
| ecg_impression_notes_group | 0/1 | boolean | Note is part of "ECG Impression Notes" Group |
| discharge_summary_notes_group | 0/1 | boolean | Note is part of "Discharge Summary Notes" Group |

<div class="footnote_container">
<div class="footnote"><sup>1</sup> <strong>is_patient_communication</strong> indicates communication with the patient, which may also coincide with<br/>&nbsp;&nbsp;&nbsp;other assertions (e.g., discharge_summary_notes_group == 1 for this record.)</div>
<div class="footnote"><sup>2</sup> Example: 2010-04-26T00:00:00</div>
</div>
