"""
TEDLA Hypertension NLP Pipeline - Launcher
===========================================
Everything in ONE file. Double-click run.bat to start.

    1. Install Dependencies
    2. Generate Test Data  (creates synthetic notes to verify pipeline)
    3. Run Pipeline         (processes clinical notes)
"""

import os
import queue
import random
import re
import sqlite3
import subprocess
import sys
import threading
import tkinter as tk
from datetime import date, timedelta
from pathlib import Path
from time import time
from tkinter import filedialog, messagebox

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = str(
    Path(__file__).resolve().parent / "tedla-hypertension-project-databricks"
)
SRC_DIR = str(Path(PROJECT_ROOT) / "src")

SEARCH_TERMS = [
    "angioedema",
    "ascvd score",
    "bradycardia",
    "breast enlargement",
    "breast pain",
    "constipation",
    "dec. libido",
    "decreased heart rate",
    "decreased libido",
    "dizziness",
    "doe",
    "drowsiness",
    "dry cough",
    "dry mouth",
    "dryness of the mouth",
    "dyspnea on exertion",
    "ed",
    "elevated hr",
    "erectile disfunction",
    "excessive facial hair",
    "excessive sleepiness",
    "face swelling",
    "facial erythema",
    "falling out",
    "fatigue",
    "flushing",
    "gingival hypertrophy",
    "gout",
    "gouty flare",
    "gum swelling",
    "gynecomastia",
    "h/a",
    "ha",
    "hallucinations",
    "headache",
    "heart failure with preserved ejection fraction",
    "heart failure with reduced ejection fraction",
    "hepatotoxicity",
    "hfpef",
    "hfref",
    "high ca",
    "high calcium",
    "hirsutism",
    "hyper ca",
    "hyper k",
    "hyper ua",
    "hypercalcemia",
    "hyperkalemia",
    "hyperprolactinemia",
    "hyperuricemia",
    "hypokalemia",
    "hyponatremia",
    "impotence",
    "inc hr",
    "inc. wt.",
    "increase in exercise",
    "increased heart rate",
    "increased lfts",
    "increased liver function tests",
    "increased prolactin",
    "increased weight",
    "insomnia",
    "light headedness",
    "lip swelling",
    "liver toxicity",
    "low alcohol intake",
    "low blood pressure",
    "low bp",
    "low hr",
    "low k",
    "low na",
    "low salt intake",
    "low sodium",
    "lower k",
    "lupus sx",
    "lupus symptom",
    "lupus-like syndrome",
    "mastodynia",
    "medication adherence",
    "n/v",
    "nausea",
    "nightmare",
    "nonproductive cough",
    "orthostatic hypotension",
    "parasomnia",
    "parkinsonian symptoms",
    "parkinsonism",
    "passed out",
    "physical activity",
    "poor sleep",
    "positive ana",
    "positive hgc",
    "pregnancy",
    "pregnant",
    "sexual se",
    "sexual side effect",
    "shortness of breath",
    "sick sinus syndrome",
    "sob",
    "somnolence",
    "symptoms of parkinson",
    "syncope",
    "tachycardia",
    "tired",
    "tongue swelling",
    "ua high",
    "urgency",
    "uric acid elevated",
    "urinary urgency",
    "vivid dreams",
    "vomiting",
    "weight gain",
    "weight loss",
    "weight reduction",
    "hypo k",
    "low sodium",
]

NOTE_TYPE_NAMES = [
    "outpatient",
    "inpatient",
    "admission",
    "discharge_summary",
    "emergency_department",
    "problem_list",
    "ecg_impression",
    "communication_encounter",
]
NOTE_TYPE_WEIGHTS = [0.30, 0.15, 0.10, 0.15, 0.10, 0.10, 0.05, 0.05]
NOTE_TYPE_TO_GROUP_COL = {
    "outpatient": "outpatient_notes_group",
    "inpatient": "inpatient_notes_group",
    "admission": "admission_notes_group",
    "discharge_summary": "discharge_summary_notes_group",
    "emergency_department": "emergency_department_notes_group",
    "problem_list": "problem_list_notes_group",
    "ecg_impression": "ecg_impression_notes_group",
    "communication_encounter": "communication_encounter_notes_group",
}
ALL_GROUP_COLS = [
    "problem_list_notes_group",
    "outpatient_notes_group",
    "communication_encounter_notes_group",
    "inpatient_notes_group",
    "admission_notes_group",
    "emergency_department_notes_group",
    "ecg_impression_notes_group",
    "discharge_summary_notes_group",
]

ERROR_HINTS = {
    "en_core_web_sm": "SpaCy model not installed. Click 'Install' first.",
    "NOTE_DATA_LOCATION": "Input path not found. Check your input folder.",
    "ModuleNotFoundError": "Missing package. Click 'Install' first.",
    "ImportError": "Missing package. Click 'Install' first.",
    "No .parquet": "No data files found. Generate test data or check path.",
}

# ---------------------------------------------------------------------------
# Color theme
# ---------------------------------------------------------------------------
C = {
    "bg": "#0f172a",
    "surface": "#1e293b",
    "surface2": "#334155",
    "border": "#475569",
    "text": "#f1f5f9",
    "text2": "#94a3b8",
    "accent": "#3b82f6",
    "accent_h": "#60a5fa",
    "green": "#22c55e",
    "green_bg": "#052e16",
    "red": "#ef4444",
    "red_bg": "#450a0a",
    "yellow": "#eab308",
    "log_bg": "#020617",
    "log_fg": "#cbd5e1",
}


# ===================================================================
#  SECTION 1: SYNTHETIC NOTE GENERATOR
# ===================================================================


def _embed(term, ctx):
    if ctx == "positive":
        t = [
            f"Patient reports {term}.",
            f"Noted {term} on examination.",
            f"Assessment: {term}.",
            f"Patient presents with {term}.",
        ]
    elif ctx == "negated":
        t = [
            f"Patient denies {term}.",
            f"No evidence of {term}.",
            f"Negative for {term}.",
            f"No {term} reported.",
        ]
    else:
        t = [
            f"Family history significant for {term}.",
            f"Mother had {term}.",
            f"Father diagnosed with {term}.",
        ]
    return random.choice(t)


def _ctx():
    r = random.random()
    return "positive" if r < 0.60 else ("negated" if r < 0.85 else "family")


def _bp():
    return f"{random.randint(110,180)}/{random.randint(60,110)}"


def _hr():
    return random.randint(55, 110)


def _note_outpatient(terms):
    tl = [_embed(t, _ctx()) for t in terms]
    age, sex = random.randint(40, 85), random.choice(["male", "female"])
    return f"""OUTPATIENT PROGRESS NOTE
CHIEF COMPLAINT: Follow-up for blood pressure management.
HISTORY OF PRESENT ILLNESS:
{age}-year-old {sex} presents for routine follow-up. Patient reports compliance
with current antihypertensive regimen. {tl[0]}
{tl[1] if len(tl) > 1 else ""}
Reports taking medications as prescribed. No recent hospitalizations.
REVIEW OF SYSTEMS:
Cardiovascular: {tl[0]}
{"Respiratory: " + tl[1] if len(tl) > 1 else "Respiratory: No dyspnea."}
{"General: " + tl[2] if len(tl) > 2 else "General: No acute concerns."}
Neurological: Alert and oriented. No focal deficits.
PHYSICAL EXAMINATION:
BP: {_bp()} mmHg  HR: {_hr()} bpm  RR: {random.randint(14,20)}
General: Alert, well-appearing {sex} in no acute distress.
Cardiovascular: Regular rate and rhythm. No murmurs.
Lungs: Clear to auscultation bilaterally. Extremities: No edema.
ASSESSMENT AND PLAN:
1. Hypertension - {"well controlled" if random.random() > 0.5 else "borderline controlled"}.
2. Medication adherence counseled. Follow-up in 3 months.
"""


def _note_inpatient(terms):
    tl = [_embed(t, _ctx()) for t in terms]
    return f"""INPATIENT DAILY PROGRESS NOTE - Hospital Day #{random.randint(1,7)}
SUBJECTIVE: Patient reports feeling {"better" if random.random() > 0.4 else "about the same"}.
{tl[0]} {tl[1] if len(tl) > 1 else ""}
OBJECTIVE:
Vitals: BP {_bp()} mmHg, HR {_hr()} bpm, T 98.{random.randint(0,9)}F, SpO2 {random.randint(94,99)}%
Labs: Na {random.randint(133,145)}, K {round(random.uniform(3.3,5.2),1)}, Cr {round(random.uniform(0.7,1.5),1)}
ASSESSMENT/PLAN:
1. Hypertension - continue IV to PO transition.
2. {tl[-1] if len(tl) > 1 else "Monitoring daily."}
3. Anticipate discharge in {random.randint(1,3)} days.
"""


def _note_admission(terms):
    tl = [_embed(t, _ctx()) for t in terms]
    age, sex = random.randint(45, 80), random.choice(["male", "female"])
    return f"""ADMISSION NOTE
ADMITTING DIAGNOSIS: Hypertensive urgency
HISTORY OF PRESENT ILLNESS:
{age}-year-old {sex} with history of hypertension, presenting with
BP of {random.randint(170,220)}/{random.randint(100,130)} mmHg.
{tl[0]} {"Additionally, " + tl[1].lower() if len(tl) > 1 else ""}
PAST MEDICAL HISTORY:
- Hypertension (diagnosed {random.randint(2,20)} years ago)
- {"Type 2 Diabetes" if random.random() > 0.5 else "Hyperlipidemia"}
MEDICATIONS:
- Lisinopril {random.choice(["10mg","20mg","40mg"])} daily
- Amlodipine {random.choice(["5mg","10mg"])} daily
PHYSICAL EXAMINATION:
BP: {_bp()} mmHg  HR: {_hr()} bpm
CV: Regular rate and rhythm. {"S4 gallop." if random.random() > 0.7 else "No murmurs."}
PLAN: Admit to telemetry. Start IV nicardipine drip. Labs: CBC, BMP, troponin.
"""


def _note_discharge(terms):
    tl = [_embed(t, _ctx()) for t in terms]
    los = random.randint(2, 8)
    return f"""DISCHARGE SUMMARY
LENGTH OF STAY: {los} days
DISCHARGE DIAGNOSIS: Hypertensive emergency
HOSPITAL COURSE:
Admitted for hypertensive emergency with BP {random.randint(180,230)}/{random.randint(110,130)}.
{tl[0]} Transitioned to oral medications. {tl[1] if len(tl) > 1 else ""}
BP stabilized on discharge regimen.
DISCHARGE MEDICATIONS:
- Amlodipine 10mg daily - Lisinopril 40mg daily
- {"Chlorthalidone 25mg daily" if random.random() > 0.5 else "Metoprolol 100mg daily"}
FOLLOW-UP: PCP in 1 week, Cardiology in 2 weeks.
"""


def _note_ed(terms):
    tl = [_embed(t, _ctx()) for t in terms]
    age, sex = random.randint(35, 85), random.choice(["male", "female"])
    return f"""EMERGENCY DEPARTMENT NOTE
CHIEF COMPLAINT: {"Elevated blood pressure" if random.random() > 0.5 else "Headache and dizziness"}
HPI: {age}-year-old {sex} with BP {random.randint(160,210)}/{random.randint(95,125)} on triage.
{tl[0]} {tl[1] if len(tl) > 1 else ""}
ED COURSE:
EKG: {"normal sinus rhythm" if random.random() > 0.5 else "LVH by voltage criteria"}.
CXR: {"No acute process" if random.random() > 0.6 else "Mild cardiomegaly"}.
Administered {"labetalol 20mg IV" if random.random() > 0.5 else "hydralazine 10mg IV"} with improvement.
DISPOSITION: {"Admitted" if random.random() > 0.5 else "Discharged with follow-up in 48hrs"}
"""


def _note_problem_list(terms):
    tl = [_embed(t, "positive") for t in terms]
    probs = ["Essential hypertension, uncontrolled", "Hyperlipidemia"]
    for t in tl[:3]:
        probs.append(t.rstrip("."))
    probs.extend(
        random.sample(
            ["Type 2 diabetes", "Obesity BMI 32", "CKD stage 2", "OSA", "GERD"],
            k=random.randint(1, 3),
        )
    )
    return (
        "PROBLEM LIST (Active)\n"
        + "\n".join(f"  {i+1}. {p}" for i, p in enumerate(probs))
        + "\n"
    )


def _note_ecg(terms):
    rate = random.randint(50, 120)
    rhythm = random.choice(
        ["Normal sinus rhythm", "Sinus tachycardia", "Sinus bradycardia"]
    )
    return f"""ECG IMPRESSION
Rate: {rate} bpm | Rhythm: {rhythm}
PR {random.randint(140,220)}ms, QRS {random.randint(80,120)}ms, QTc {random.randint(380,480)}ms
Findings: {rhythm} at {rate} bpm. {"LVH by voltage." if random.random() > 0.5 else "No ST changes."}
{_embed(terms[0], _ctx())}
"""


def _note_comm(terms):
    tl = [_embed(t, _ctx()) for t in terms]
    return f"""COMMUNICATION NOTE
TYPE: {"Telephone encounter" if random.random() > 0.5 else "Patient message"}
Patient contacted regarding BP concerns. {tl[0]} {tl[1] if len(tl) > 1 else ""}
Advised to {"continue current medications" if random.random() > 0.5 else "schedule appointment"}.
"""


NOTE_GEN = {
    "outpatient": _note_outpatient,
    "inpatient": _note_inpatient,
    "admission": _note_admission,
    "discharge_summary": _note_discharge,
    "emergency_department": _note_ed,
    "problem_list": _note_problem_list,
    "ecg_impression": _note_ecg,
    "communication_encounter": _note_comm,
}


def generate_test_data(output_folder, num_notes, log_fn=print):
    import pandas as pd

    base = Path(output_folder)
    inp, out = base / "test_input", base / "test_output"
    dirs = {
        k: inp / k
        for k in [
            "note_data",
            "data_to_process",
            "note_to_groups_map",
            "note_to_visit_date",
            "note_group_to_term",
        ]
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    log_fn(f"Generating {num_notes} synthetic clinical notes...")
    npat = max(1, num_notes // 5)
    pids = list(range(500000, 500000 + npat))
    bd = date(2019, 1, 1)
    notes, meta, groups, visits = [], [], [], []
    for i in range(num_notes):
        nid, pid, vid = 1000000 + i, pids[i % npat], 300000 + i
        nt = random.choices(NOTE_TYPE_NAMES, weights=NOTE_TYPE_WEIGHTS, k=1)[0]
        st = random.sample(SEARCH_TERMS, min(random.randint(1, 3), len(SEARCH_TERMS)))
        nd = bd + timedelta(days=random.randint(0, 4 * 365))
        notes.append({"note_id": nid, "note_text": NOTE_GEN[nt](st)})
        meta.append(
            {
                "note_id": nid,
                "person_id": pid,
                "x_part_num": 1,
                "x_uniq": str(900000 + i),
                "note_date": nd,
                "visit_occurrence_id": vid,
                "is_patient_communication": nt == "communication_encounter",
                "note_within_visit": nt
                in (
                    "inpatient",
                    "admission",
                    "discharge_summary",
                    "emergency_department",
                ),
            }
        )
        gr = {"note_id": nid}
        for c in ALL_GROUP_COLS:
            gr[c] = c == NOTE_TYPE_TO_GROUP_COL[nt]
        groups.append(gr)
        visits.append(
            {
                "note_id": nid,
                "visit_occurrence_id": vid,
                "visit_start_date": nd,
                "visit_end_date": nd + timedelta(days=random.randint(0, 3)),
            }
        )
    log_fn("Writing parquet files...")
    df = pd.DataFrame(notes)
    df["note_id"] = df["note_id"].astype("int64")
    df.to_parquet(dirs["note_data"] / "synthetic_notes.parquet", index=False)
    df = pd.DataFrame(meta)
    df["note_id"] = df["note_id"].astype("int64")
    df["person_id"] = df["person_id"].astype("int64")
    df["x_part_num"] = df["x_part_num"].astype("int32")
    df["visit_occurrence_id"] = df["visit_occurrence_id"].astype("int64")
    df["note_date"] = pd.to_datetime(df["note_date"])
    df.to_parquet(dirs["data_to_process"] / "data_to_process.parquet", index=False)
    df = pd.DataFrame(groups)
    df["note_id"] = df["note_id"].astype("int64")
    for c in ALL_GROUP_COLS:
        df[c] = df[c].astype(bool)
    df.to_parquet(
        dirs["note_to_groups_map"] / "note_to_groups_map.parquet", index=False
    )
    df = pd.DataFrame(visits)
    df["note_id"] = df["note_id"].astype("int64")
    df["visit_occurrence_id"] = df["visit_occurrence_id"].astype("int64")
    df["visit_start_date"] = pd.to_datetime(df["visit_start_date"])
    df["visit_end_date"] = pd.to_datetime(df["visit_end_date"])
    df.to_parquet(
        dirs["note_to_visit_date"] / "note_to_visit_date.parquet", index=False
    )
    csv_p = (
        Path(PROJECT_ROOT)
        / "src"
        / "nlp_method"
        / "data"
        / "map_search_term_to_note_group.csv"
    )
    if csv_p.exists():
        pd.read_csv(csv_p).to_parquet(
            dirs["note_group_to_term"] / "note_group_to_term.parquet", index=False
        )
    else:
        recs = [
            {
                "search_term_to_note_groups_id": i + 1,
                "search_term": t,
                "notes_admissions": 1,
                "notes_communication_encounter": 1 if random.random() > 0.3 else 0,
                "notes_discharge_summary": 1,
                "notes_ecg_impression": 1 if t in ["bradycardia", "tachycardia"] else 0,
                "notes_emergency_department": 1,
                "notes_inpatient": 1,
                "notes_outpatient": 1,
                "notes_problem_lists": 1,
            }
            for i, t in enumerate(sorted(set(SEARCH_TERMS)))
        ]
        pd.DataFrame(recs).to_parquet(
            dirs["note_group_to_term"] / "note_group_to_term.parquet", index=False
        )
    log_fn(f"Done! {num_notes} notes for {npat} patients.")
    return str(inp), str(out)


# ===================================================================
#  SECTION 2: .ENV GENERATOR
# ===================================================================


def make_env_file(input_path, output_path, num_workers):
    inp, out = Path(input_path), Path(output_path)
    nd = str(inp / "note_data") if (inp / "note_data").exists() else str(inp)
    dp = (
        str(inp / "data_to_process") if (inp / "data_to_process").exists() else str(inp)
    )
    gm = (
        str(inp / "note_to_groups_map") if (inp / "note_to_groups_map").exists() else ""
    )
    vd = (
        str(inp / "note_to_visit_date") if (inp / "note_to_visit_date").exists() else ""
    )
    gt = (
        str(inp / "note_group_to_term") if (inp / "note_group_to_term").exists() else ""
    )
    cs = (
        Path(PROJECT_ROOT)
        / "src"
        / "nlp_method"
        / "data"
        / "map_search_term_to_note_group.csv"
    )
    for d in (out / "results", out / "logs", out / "metrics"):
        d.mkdir(parents=True, exist_ok=True)
    content = f"""PYTHONPATH=src
SPACY_MODEL=en_core_web_sm
NOTE_DATA_LOCATION={nd}
DATA_TO_PROCESS_DATASET={dp}
MAP_SEARCH_TERM_TO_NOTE_GROUP={cs if cs.exists() else ""}
NOTE_TO_GROUPS_MAP_PATH={gm}
NOTE_TO_VISIT_DATE_PATH={vd}
NOTE_GROUP_TO_TERM_PATH={gt}
SQLITE_DB_PATH={out/"results"}
LOG_PATH={out/"logs"}
METRICS_PATH={out/"metrics"}
RESULTS_TABLE_NAME=results
NUM_WORKER_PROCESSES={num_workers}
MAX_WORKER_QUEUE_SIZE={max(num_workers*3,8)}
NOTE_ITERATOR_BATCH_SIZE=5000
MAX_LOADER_WORKERS=4
WORKER_READY_TIMEOUT_SECONDS=300
WORKER_JOIN_TIMEOUT_SECONDS=3600
"""
    ep = Path(PROJECT_ROOT) / "src" / "nlp_method" / ".env"
    ep.write_text(content, encoding="utf-8")
    return str(ep)


# ===================================================================
#  SECTION 2b: CSV / EXCEL IMPORT
# ===================================================================

SUPPORTED_IMPORT_EXT = {".csv", ".xlsx", ".xls", ".tsv"}


def import_notes_file(file_path, output_folder, log_fn=print):
    """Convert a CSV/Excel file of clinical notes into the parquet structure the pipeline expects.

    Required columns: note_id, note_text
    Optional columns: person_id, note_date, note_type
    """
    import pandas as pd

    fp = Path(file_path)
    ext = fp.suffix.lower()
    log_fn(f"Reading {fp.name} ...")
    if ext == ".csv":
        df = pd.read_csv(fp, encoding="utf-8-sig")
    elif ext == ".tsv":
        df = pd.read_csv(fp, sep="\t", encoding="utf-8-sig")
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(fp)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    if "note_text" not in df.columns:
        raise ValueError(
            "File must have a 'note_text' column containing the clinical note text."
        )
    if "note_id" not in df.columns:
        df.insert(0, "note_id", range(1_000_000, 1_000_000 + len(df)))
        log_fn("No 'note_id' column found - auto-generated IDs.")
    if "person_id" not in df.columns:
        df["person_id"] = range(500_000, 500_000 + len(df))
        log_fn("No 'person_id' column found - auto-generated IDs.")
    if "note_date" not in df.columns:
        df["note_date"] = pd.Timestamp.now().normalize()
    else:
        df["note_date"] = pd.to_datetime(df["note_date"], errors="coerce").fillna(
            pd.Timestamp.now().normalize()
        )

    n = len(df)
    base = Path(output_folder)
    inp = base / "imported_input"
    out = base / "imported_output"
    dirs = {
        k: inp / k
        for k in [
            "note_data",
            "data_to_process",
            "note_to_groups_map",
            "note_to_visit_date",
            "note_group_to_term",
        ]
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)

    # Determine note type column
    note_type_col = None
    for candidate in ("note_type", "type", "category", "note_category"):
        if candidate in df.columns:
            note_type_col = candidate
            break

    log_fn(f"Converting {n} notes to pipeline format...")

    # 1. note_data
    nd = df[["note_id", "note_text"]].copy()
    nd["note_id"] = nd["note_id"].astype("int64")
    nd.to_parquet(dirs["note_data"] / "notes.parquet", index=False)

    # 2. data_to_process (metadata)
    meta = df[["note_id", "person_id", "note_date"]].copy()
    meta["note_id"] = meta["note_id"].astype("int64")
    meta["person_id"] = meta["person_id"].astype("int64")
    meta["x_part_num"] = 1
    meta["x_uniq"] = [str(900_000 + i) for i in range(n)]
    meta["visit_occurrence_id"] = [300_000 + i for i in range(n)]
    meta["is_patient_communication"] = False
    meta["note_within_visit"] = True
    meta["note_date"] = pd.to_datetime(meta["note_date"])
    meta["visit_occurrence_id"] = meta["visit_occurrence_id"].astype("int64")
    meta.to_parquet(dirs["data_to_process"] / "data_to_process.parquet", index=False)

    # 3. note_to_groups_map
    groups = df[["note_id"]].copy()
    groups["note_id"] = groups["note_id"].astype("int64")
    for c in ALL_GROUP_COLS:
        if note_type_col:
            mapped_type = df[note_type_col].str.lower().str.strip()
            groups[c] = mapped_type.apply(
                lambda v, col=c: col.replace("_notes_group", "") in str(v)
            )
        else:
            groups[c] = c == "outpatient_notes_group"  # default all to outpatient
    groups.to_parquet(
        dirs["note_to_groups_map"] / "note_to_groups_map.parquet", index=False
    )

    # 4. note_to_visit_date
    visits = pd.DataFrame(
        {
            "note_id": df["note_id"].astype("int64"),
            "visit_occurrence_id": meta["visit_occurrence_id"],
            "visit_start_date": pd.to_datetime(df["note_date"]),
            "visit_end_date": pd.to_datetime(df["note_date"]),
        }
    )
    visits.to_parquet(
        dirs["note_to_visit_date"] / "note_to_visit_date.parquet", index=False
    )

    # 5. note_group_to_term
    csv_p = (
        Path(PROJECT_ROOT)
        / "src"
        / "nlp_method"
        / "data"
        / "map_search_term_to_note_group.csv"
    )
    if csv_p.exists():
        pd.read_csv(csv_p).to_parquet(
            dirs["note_group_to_term"] / "note_group_to_term.parquet", index=False
        )
    else:
        recs = [
            {
                "search_term_to_note_groups_id": i + 1,
                "search_term": t,
                "notes_admissions": 1,
                "notes_communication_encounter": 1,
                "notes_discharge_summary": 1,
                "notes_ecg_impression": 0,
                "notes_emergency_department": 1,
                "notes_inpatient": 1,
                "notes_outpatient": 1,
                "notes_problem_lists": 1,
            }
            for i, t in enumerate(sorted(set(SEARCH_TERMS)))
        ]
        pd.DataFrame(recs).to_parquet(
            dirs["note_group_to_term"] / "note_group_to_term.parquet", index=False
        )

    log_fn(f"Done! Imported {n} notes from {fp.name}.")
    return str(inp), str(out)


# ===================================================================
#  SECTION 2c: RESULTS EXPORT (CSV / EXCEL)
# ===================================================================

RESULT_COLUMNS = [
    "note_id",
    "batch_group",
    "patient_id",
    "window_text",
    "note_date",
    "search_term",
    "problem_list_notes_group",
    "outpatient_notes_group",
    "communication_encounter_notes_group",
    "inpatient_notes_group",
    "admission_notes_group",
    "emergency_department_notes_group",
    "ecg_impression_notes_group",
    "discharge_summary_notes_group",
    "is_patient_communication",
    "is_note_within_visit",
    "is_negated",
    "window_start_char_offset",
    "window_end_char_offset",
    "entity_start_offset",
    "entity_end_offset",
]


def export_results(results_folder, output_file, log_fn=print):
    """Read all SQLite result databases and export to CSV or Excel."""
    import pandas as pd

    rdir = Path(results_folder)
    db_files = list(rdir.glob("**/*.db"))
    if not db_files:
        raise FileNotFoundError(f"No .db result files found in {rdir}")
    all_rows = []
    for dbf in db_files:
        try:
            conn = sqlite3.connect(str(dbf))
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cursor.fetchall()]
            for tbl in tables:
                if tbl.startswith("sqlite_"):
                    continue
                rows = pd.read_sql_query(f"SELECT * FROM {tbl}", conn)
                all_rows.append(rows)
            conn.close()
        except Exception as e:
            log_fn(f"Warning: could not read {dbf.name}: {e}")
    if not all_rows:
        raise ValueError("No result data found in database files.")
    combined = pd.concat(all_rows, ignore_index=True)
    # Drop internal columns
    if "result_id" in combined.columns:
        combined.drop(columns=["result_id"], inplace=True)
    out_path = Path(output_file)
    ext = out_path.suffix.lower()
    if ext == ".csv":
        combined.to_csv(out_path, index=False, encoding="utf-8-sig")
    elif ext == ".xlsx":
        combined.to_excel(out_path, index=False, engine="openpyxl")
    elif ext == ".tsv":
        combined.to_csv(out_path, index=False, sep="\t", encoding="utf-8-sig")
    else:
        combined.to_csv(out_path.with_suffix(".csv"), index=False, encoding="utf-8-sig")
        out_path = out_path.with_suffix(".csv")
    log_fn(f"Exported {len(combined)} results to {out_path.name}")
    return str(out_path), len(combined)


# ===================================================================
#  SECTION 3: INSTALLER
# ===================================================================


def install_deps(log_fn, done_fn):
    def _work():
        try:
            py = sys.executable
            req = Path(PROJECT_ROOT) / "requirements.txt"
            log_fn("[1/2] Installing Python packages...")
            if req.exists():
                _runcmd([py, "-m", "pip", "install", "-r", str(req)], log_fn)
            else:
                _runcmd(
                    [
                        py,
                        "-m",
                        "pip",
                        "install",
                        "spacy>=3.7",
                        "medspacy>=1.3",
                        "pandas",
                        "pyarrow",
                        "polars",
                        "python-dotenv",
                        "loguru",
                    ],
                    log_fn,
                )
            log_fn("[2/2] Downloading spaCy model...")
            _runcmd([py, "-m", "spacy", "download", "en_core_web_sm"], log_fn)
            log_fn("Verifying...")
            _runcmd(
                [
                    py,
                    "-c",
                    "import spacy; import medspacy; import pandas; import pyarrow; import polars; import loguru; print('All OK')",
                ],
                log_fn,
            )
            done_fn(True, "All dependencies installed and verified!")
        except Exception as e:
            done_fn(False, str(e))

    threading.Thread(target=_work, daemon=True).start()


def _runcmd(cmd, log_fn):
    p = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
    )
    for line in p.stdout:  # type: ignore
        log_fn(line.rstrip("\n"))
    p.wait()
    if p.returncode != 0:
        raise RuntimeError(f"Command failed (exit {p.returncode})")


# ===================================================================
#  SECTION 4: PIPELINE RUNNER
# ===================================================================


class PipelineRunner:
    def __init__(self, env_path):
        self.env_path = env_path
        self._proc = None
        self._q = queue.Queue()
        self._running = False
        self.notes_sent = 0

    @property
    def running(self):
        return self._running

    def count_notes(self, input_path):
        try:
            import pyarrow.parquet as pq

            d = Path(input_path)
            if (d / "note_data").exists():
                d = d / "note_data"
            return sum(
                pq.read_metadata(str(f)).num_rows for f in d.glob("**/*.parquet")
            )
        except:
            return 0

    def start(self):
        self.notes_sent = 0
        self._running = True
        env = os.environ.copy()
        env["PYTHONPATH"] = SRC_DIR
        try:
            with open(self.env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        env[k.strip()] = v.strip()
        except FileNotFoundError:
            pass
        self._proc = subprocess.Popen(
            [sys.executable, "-m", "nlp_method"],
            cwd=PROJECT_ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        threading.Thread(target=self._reader, daemon=True).start()

    def stop(self):
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=10)
            except:
                self._proc.kill()
        self._running = False

    def poll(self):
        items = []
        while True:
            try:
                items.append(self._q.get_nowait())
            except queue.Empty:
                break
        return items

    def returncode(self):
        return self._proc.poll() if self._proc else None

    def _reader(self):
        try:
            for line in self._proc.stdout:  # type: ignore
                line = line.rstrip("\n")
                m = re.search(r"with\s+(\d+)\s+sent", line)
                if m:
                    self.notes_sent = int(m.group(1))
                self._q.put(
                    (
                        line,
                        any(
                            k in line.lower()
                            for k in ["error", "exception", "traceback", "failed"]
                        ),
                    )
                )
        except:
            pass
        finally:
            self._proc.wait()  # type: ignore
            self._running = False
            self._q.put((None, False))


# ===================================================================
#  SECTION 5: MODERN GUI
# ===================================================================


class RoundedButton(tk.Canvas):
    """A modern rounded button using canvas drawing."""

    def __init__(
        self, parent, text="", command=None, color=None, width=160, height=38, **kw
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=C["surface"],
            highlightthickness=0,
            cursor="hand2",
            **kw,
        )
        self._cmd = command
        self._color = color or C["accent"]
        self._hover_color = C["accent_h"]
        self._text = text
        self._bw, self._bh = width, height
        self._enabled = True
        self._draw(self._color)
        self.bind(
            "<Enter>",
            lambda e: self._draw(self._hover_color) if self._enabled else None,
        )
        self.bind(
            "<Leave>", lambda e: self._draw(self._color) if self._enabled else None
        )
        self.bind(
            "<Button-1>", lambda e: self._cmd() if self._cmd and self._enabled else None
        )

    def _draw(self, fill):
        self.delete("all")
        r = 8
        w, h = self._bw, self._bh
        self.create_round_rect(2, 2, w - 2, h - 2, r, fill=fill, outline="")
        fg = C["text"] if self._enabled else C["text2"]
        self.create_text(
            w // 2, h // 2, text=self._text, fill=fg, font=("Segoe UI", 10, "bold")
        )

    def create_round_rect(self, x1, y1, x2, y2, r, **kw):
        self.create_arc(
            x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, style="pieslice", **kw
        )
        self.create_arc(
            x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, style="pieslice", **kw
        )
        self.create_arc(
            x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, style="pieslice", **kw
        )
        self.create_arc(
            x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, style="pieslice", **kw
        )
        self.create_rectangle(x1 + r, y1, x2 - r, y2, **kw)
        self.create_rectangle(x1, y1 + r, x2, y2 - r, **kw)

    def set_enabled(self, enabled):
        self._enabled = enabled
        self.config(cursor="hand2" if enabled else "arrow")
        self._draw(self._color if enabled else C["surface2"])

    def set_text(self, text):
        self._text = text
        self._draw(self._color if self._enabled else C["surface2"])


class App:
    def __init__(self, root):
        self.root = root
        self.runner = None
        self._t0 = None
        self._total = 0
        self._all_log = ""

        root.title("TEDLA Hypertension NLP Pipeline")
        root.geometry("860x780")
        root.minsize(800, 700)
        root.configure(bg=C["bg"])

        # Main container
        main = tk.Frame(root, bg=C["bg"], padx=24, pady=16)
        main.pack(fill="both", expand=True)

        # ---- Header ----
        hdr = tk.Frame(main, bg=C["bg"])
        hdr.pack(fill="x", pady=(0, 12))
        tk.Label(
            hdr, text="TEDLA", font=("Segoe UI", 22, "bold"), fg=C["accent"], bg=C["bg"]
        ).pack(side="left")
        tk.Label(
            hdr,
            text="  Hypertension NLP Pipeline",
            font=("Segoe UI", 22),
            fg=C["text"],
            bg=C["bg"],
        ).pack(side="left")
        tk.Label(
            hdr,
            text="Clinical note processing for research",
            font=("Segoe UI", 10),
            fg=C["text2"],
            bg=C["bg"],
        ).pack(side="right", pady=8)

        # ---- Card: Install ----
        self._card_install = self._card(
            main,
            "Install Dependencies",
            "Download all required packages and language models",
        )
        ci = self._card_install
        row = tk.Frame(ci, bg=C["surface"])
        row.pack(fill="x", pady=(8, 0))
        self.btn_install = RoundedButton(
            row, "Install", self._install, width=130, height=36
        )
        self.btn_install.pack(side="left")
        self.lbl_install = tk.Label(
            row,
            text="  Not installed yet",
            font=("Segoe UI", 9),
            fg=C["text2"],
            bg=C["surface"],
        )
        self.lbl_install.pack(side="left", padx=10)

        # ---- Card: Run Pipeline ----
        self._card_run = self._card(
            main,
            "Run Pipeline",
            "Process clinical notes through the NLP extraction pipeline",
        )
        cp = self._card_run
        # Input row with Import button
        r1 = tk.Frame(cp, bg=C["surface"])
        r1.pack(fill="x", pady=(8, 4))
        tk.Label(
            r1,
            text="Input",
            font=("Segoe UI", 9),
            fg=C["text2"],
            bg=C["surface"],
            width=8,
            anchor="w",
        ).pack(side="left")
        self.inp_var = tk.StringVar()
        tk.Entry(
            r1,
            textvariable=self.inp_var,
            font=("Segoe UI", 10),
            bg=C["surface2"],
            fg=C["text"],
            insertbackground=C["text"],
            relief="flat",
            bd=0,
        ).pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        self._browse_btn(r1, self.inp_var)
        self.btn_import = RoundedButton(
            r1,
            "Import CSV/Excel",
            self._import_file,
            color="#7c3aed",
            width=145,
            height=36,
        )
        self.btn_import.pack(side="right", padx=(6, 0))
        # Output
        r2 = tk.Frame(cp, bg=C["surface"])
        r2.pack(fill="x", pady=(0, 4))
        tk.Label(
            r2,
            text="Output",
            font=("Segoe UI", 9),
            fg=C["text2"],
            bg=C["surface"],
            width=8,
            anchor="w",
        ).pack(side="left")
        self.out_var = tk.StringVar()
        tk.Entry(
            r2,
            textvariable=self.out_var,
            font=("Segoe UI", 10),
            bg=C["surface2"],
            fg=C["text"],
            insertbackground=C["text"],
            relief="flat",
            bd=0,
        ).pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        self._browse_btn(r2, self.out_var)
        # Workers + buttons
        r3 = tk.Frame(cp, bg=C["surface"])
        r3.pack(fill="x", pady=(0, 4))
        tk.Label(
            r3,
            text="Workers",
            font=("Segoe UI", 9),
            fg=C["text2"],
            bg=C["surface"],
            width=8,
            anchor="w",
        ).pack(side="left")
        self.wk_var = tk.StringVar(value=str(min(4, os.cpu_count() or 2)))
        tk.Entry(
            r3,
            textvariable=self.wk_var,
            font=("Segoe UI", 10),
            width=5,
            bg=C["surface2"],
            fg=C["text"],
            insertbackground=C["text"],
            relief="flat",
            bd=0,
        ).pack(side="left", ipady=6, padx=(0, 6))
        tk.Label(
            r3,
            text=f"of {os.cpu_count() or '?'} cores",
            font=("Segoe UI", 9),
            fg=C["text2"],
            bg=C["surface"],
        ).pack(side="left", padx=(0, 16))
        self.btn_run = RoundedButton(
            r3, "Run Pipeline", self._run, color="#16a34a", width=150, height=36
        )
        self.btn_run.pack(side="left", padx=(0, 8))
        self.btn_stop = RoundedButton(
            r3, "Stop", self._stop, color=C["red"], width=80, height=36
        )
        self.btn_stop.pack(side="left", padx=(0, 8))
        self.btn_stop.set_enabled(False)
        self.btn_export = RoundedButton(
            r3,
            "Export CSV",
            self._export_results,
            color="#0891b2",
            width=110,
            height=36,
        )
        self.btn_export.pack(side="left", padx=(0, 8))
        self.btn_export.set_enabled(False)
        self.btn_open = RoundedButton(
            r3, "Open Output", self._open_out, color=C["surface2"], width=120, height=36
        )
        self.btn_open.pack(side="left")
        self.btn_open.set_enabled(False)
        # Progress
        r4 = tk.Frame(cp, bg=C["surface"])
        r4.pack(fill="x", pady=(6, 0))
        self.prog_var = tk.StringVar(value="")
        tk.Label(
            r4,
            textvariable=self.prog_var,
            font=("Segoe UI", 9),
            fg=C["accent_h"],
            bg=C["surface"],
        ).pack(side="left")
        # Progress bar canvas
        self.prog_canvas = tk.Canvas(
            cp, height=6, bg=C["surface2"], highlightthickness=0
        )
        self.prog_canvas.pack(fill="x", pady=(6, 0))
        self._prog_pct = 0

        # ---- Log panel ----
        log_frame = tk.Frame(main, bg=C["log_bg"], bd=0)
        log_frame.pack(fill="both", expand=True, pady=(12, 0))

        log_hdr = tk.Frame(log_frame, bg=C["surface"])
        log_hdr.pack(fill="x")
        tk.Label(
            log_hdr,
            text="  Log Output",
            font=("Segoe UI", 9, "bold"),
            fg=C["text2"],
            bg=C["surface"],
            pady=4,
        ).pack(side="left")
        clr_btn = tk.Label(
            log_hdr,
            text=" Clear ",
            font=("Segoe UI", 8),
            fg=C["text2"],
            bg=C["surface2"],
            cursor="hand2",
            padx=8,
            pady=2,
        )
        clr_btn.pack(side="right", padx=6, pady=3)
        clr_btn.bind("<Button-1>", lambda e: self._clear_log())

        self.log = tk.Text(
            log_frame,
            wrap="word",
            font=("Cascadia Code", 9),
            bg=C["log_bg"],
            fg=C["log_fg"],
            insertbackground=C["text"],
            state="disabled",
            bd=0,
            padx=10,
            pady=6,
            relief="flat",
        )
        sb = tk.Scrollbar(
            log_frame, command=self.log.yview, bg=C["surface"], troughcolor=C["log_bg"]
        )
        self.log.config(yscrollcommand=sb.set)
        self.log.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.log.tag_configure("err", foreground=C["red"])
        self.log.tag_configure("ok", foreground=C["green"])
        self.log.tag_configure("dim", foreground=C["text2"])

        # ---- Status bar ----
        self.stat_var = tk.StringVar(value="Ready")
        tk.Label(
            main,
            textvariable=self.stat_var,
            font=("Segoe UI", 9),
            fg=C["text2"],
            bg=C["bg"],
            anchor="w",
            pady=4,
        ).pack(fill="x")

    # ---- Helpers ----

    def _card(self, parent, title, subtitle):
        """Create a card-style panel."""
        outer = tk.Frame(parent, bg=C["border"], bd=0)
        outer.pack(fill="x", pady=(0, 8))
        inner = tk.Frame(outer, bg=C["surface"], padx=16, pady=12)
        inner.pack(fill="x", padx=1, pady=1)
        tk.Label(
            inner,
            text=title,
            font=("Segoe UI", 11, "bold"),
            fg=C["text"],
            bg=C["surface"],
        ).pack(anchor="w")
        tk.Label(
            inner, text=subtitle, font=("Segoe UI", 9), fg=C["text2"], bg=C["surface"]
        ).pack(anchor="w")
        return inner

    def _browse_btn(self, parent, var):
        b = tk.Label(
            parent,
            text=" ... ",
            font=("Segoe UI", 9, "bold"),
            fg=C["text"],
            bg=C["surface2"],
            cursor="hand2",
            padx=8,
            pady=4,
        )
        b.pack(side="right")
        b.bind("<Button-1>", lambda e: var.set(filedialog.askdirectory() or var.get()))

    def _w(self, txt, tag=""):
        self.log.config(state="normal")
        self.log.insert("end", txt, tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _clear_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    def _set_progress(self, pct):
        self._prog_pct = pct
        self.prog_canvas.delete("all")
        w = self.prog_canvas.winfo_width()
        if w > 1:
            fill_w = int(w * pct / 100)
            self.prog_canvas.create_rectangle(
                0, 0, fill_w, 6, fill=C["accent"], outline=""
            )

    # ---- Install ----

    def _install(self):
        self.btn_install.set_enabled(False)
        self.lbl_install.config(text="  Installing...", fg=C["yellow"])
        self._w("--- Installing Dependencies ---\n", "dim")

        def log_cb(line):
            self.root.after(0, self._w, line + "\n")

        def done_cb(ok, msg):
            def _u():
                self.btn_install.set_enabled(True)
                if ok:
                    self.lbl_install.config(text="  Installed", fg=C["green"])
                    self._w(msg + "\n", "ok")
                else:
                    self.lbl_install.config(text="  FAILED - see log", fg=C["red"])
                    self._w("FAILED: " + msg + "\n", "err")

            self.root.after(0, _u)

        install_deps(log_cb, done_cb)

    # ---- Import CSV/Excel ----

    def _import_file(self):
        fp = filedialog.askopenfilename(
            title="Select CSV or Excel file with clinical notes",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx *.xls"),
                ("TSV files", "*.tsv"),
                ("All files", "*.*"),
            ],
        )
        if not fp:
            return
        folder = filedialog.askdirectory(title="Select folder for converted data")
        if not folder:
            return
        self.btn_import.set_enabled(False)
        self._w(f"--- Importing {Path(fp).name} ---\n", "dim")

        def _work():
            try:
                inp, out = import_notes_file(
                    fp,
                    folder,
                    log_fn=lambda msg: self.root.after(0, self._w, msg + "\n"),
                )

                def _done():
                    self.btn_import.set_enabled(True)
                    self.inp_var.set(inp)
                    self.out_var.set(out)
                    self._w("Import complete. Paths auto-filled.\n", "ok")

                self.root.after(0, _done)
            except Exception as ex:

                def _fail(_ex):
                    self.btn_import.set_enabled(True)
                    self._w(f"Import ERROR: {_ex}\n", "err")

                self.root.after(0, _fail(ex))

        threading.Thread(target=_work, daemon=True).start()

    # ---- Export Results ----

    def _export_results(self):
        out = self.out_var.get().strip()
        if not out:
            messagebox.showwarning("Missing", "No output folder set.")
            return
        results_dir = Path(out) / "results"
        if not results_dir.exists():
            results_dir = Path(out)
        fp = filedialog.asksaveasfilename(
            title="Export results as",
            defaultextension=".csv",
            initialfile="pipeline_results.csv",
            filetypes=[
                ("CSV file", "*.csv"),
                ("Excel file", "*.xlsx"),
                ("TSV file", "*.tsv"),
            ],
        )
        if not fp:
            return
        self._w("--- Exporting results ---\n", "dim")

        def _work():
            try:
                path, count = export_results(  # type: ignore
                    str(results_dir),
                    fp,
                    log_fn=lambda msg: self.root.after(0, self._w, msg + "\n"),
                )
                self.root.after(0, self._w, f"Exported {count} rows to {path}\n", "ok")
            except Exception as e:
                self.root.after(0, self._w, f"Export ERROR: {e}\n", "err")

        threading.Thread(target=_work, daemon=True).start()

    # ---- Run ----

    def _run(self):
        inp = self.inp_var.get().strip()
        out = self.out_var.get().strip()
        if not inp:
            messagebox.showwarning("Missing", "Select an Input folder.")
            return
        if not out:
            messagebox.showwarning("Missing", "Select an Output folder.")
            return
        if not Path(inp).exists():
            messagebox.showerror("Error", f"Input not found:\n{inp}")
            return
        try:
            wk = int(self.wk_var.get())
        except ValueError:
            messagebox.showwarning("Invalid", "Workers must be a number.")
            return

        try:
            env_path = make_env_file(inp, out, wk)
            self._w(f"Config: {env_path}\n", "dim")
        except Exception as e:
            messagebox.showerror("Error", f"Config failed:\n{e}")
            return

        self.runner = PipelineRunner(env_path)
        self._total = self.runner.count_notes(inp)
        if self._total > 0:
            est = self._total / (750 * wk)
            es = (
                f"~{max(1,int(est*60))}s"
                if est < 1
                else (f"~{int(est)}m" if est < 60 else f"~{est/60:.1f}h")
            )
            self._w(f"Found {self._total} notes. Estimated: {es} with {wk} workers.\n")
            self.prog_var.set(f"Estimated: {es} for {self._total:,} notes")
        else:
            self.prog_var.set("Running...")

        self.btn_run.set_enabled(False)
        self.btn_stop.set_enabled(True)
        self.btn_open.set_enabled(False)
        self._set_progress(0)
        self.stat_var.set("Pipeline running...")
        self._t0 = time()
        self._all_log = ""
        try:
            self.runner.start()
        except Exception as e:
            self._w(f"Failed to start: {e}\n", "err")
            self._reset()
            return
        self._poll()

    def _stop(self):
        if self.runner and self.runner.running:
            self.runner.stop()
            self._w("\nStopped by user.\n", "err")
            self.stat_var.set("Stopped.")
            self._reset()

    def _open_out(self):
        p = self.out_var.get().strip()
        if p and Path(p).exists():
            if sys.platform == "win32":
                os.startfile(p)
            else:
                subprocess.run(["xdg-open", p])

    def _poll(self):
        if not self.runner:
            return
        for line, is_err in self.runner.poll():
            if line is None:
                elapsed = time() - self._t0 if self._t0 else 0
                rc = self.runner.returncode()
                m, s = int(elapsed // 60), int(elapsed % 60)
                if rc == 0:
                    self._w(f"\nCompleted in {m}m {s}s.\n", "ok")
                    self.stat_var.set(f"Completed in {m}m {s}s")
                    self._set_progress(100)
                else:
                    self._w(f"\nFailed (exit {rc}).\n", "err")
                    for pat, msg in ERROR_HINTS.items():
                        if pat.lower() in self._all_log.lower():
                            self._w(f"\n{msg}\n", "err")
                            break
                    self.stat_var.set(f"Failed (exit {rc})")
                self.btn_open.set_enabled(True)
                self.btn_export.set_enabled(True)
                self._reset()
                return
            self._w(line + "\n", "err" if is_err else "")
            self._all_log += line + "\n"
        if self._total > 0 and self.runner:
            sent = self.runner.notes_sent
            pct = min(100, int(sent / self._total * 100))
            self._set_progress(pct)
            elapsed = time() - self._t0 if self._t0 else 0
            if sent > 0 and elapsed > 0:
                rem = (self._total - sent) / (sent / elapsed)
                rs = (
                    f"{int(rem)}s left"
                    if rem < 60
                    else f"{int(rem//60)}m {int(rem%60)}s left"
                )
                self.prog_var.set(f"{pct}%  |  {sent:,}/{self._total:,} notes  |  {rs}")
            else:
                self.prog_var.set(f"{pct}%  |  {sent:,}/{self._total:,} notes")
        self.root.after(100, self._poll)

    def _reset(self):
        self.btn_run.set_enabled(True)
        self.btn_stop.set_enabled(False)


# ===================================================================
#  ENTRY POINT
# ===================================================================


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
