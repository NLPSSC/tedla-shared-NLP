import os

from common.worker_mixin import WorkerMixin
from nlp_method.results import RESULTS_TABLE_NAME, TABLE_SCHEMA
from nlp_method.results.FileLock import process_lock
from nlp_method.results.datastore.location import DataStoreLocation
from nlp_method.results.datastore.helpers import results_field_list
from nlp_method.results.result_record import ResultRecord


from loguru import logger


import sqlite3
from pathlib import Path
from typing import Any, Callable, List

dbeaver_query_script_path = os.getenv("DBEAVER_QUERY_SCRIPT_PATH", None)
if dbeaver_query_script_path is not None:
    dbeaver_query_script_path = Path(dbeaver_query_script_path).resolve()


class ResultsDataStore(WorkerMixin):
    results_table_name: str = RESULTS_TABLE_NAME

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._result_data_store_folder: DataStoreLocation = DataStoreLocation(
            *args, **kwargs
        )  # Initialize the path manager to set up the file lock and folder name

        self._table_exists: bool = False
        self._init_table()

    def __del__(self):
        sql_db_path: Path = self.results_path
        results_folder_path: Path = (
            self._result_data_store_folder.get_latest_results_folder_path()
        )
        db_files = list(results_folder_path.glob("*.db"))
        windows_loc = [
            (
                x.stem,
                rf"E:\project_data\tedla-hypertension\results\db\{x.parent.name}\{x.name}",
            )
            for x in db_files
        ]

        if sql_db_path not in db_files:
            logger.warning(
                f"Expected database file {sql_db_path} not found in results folder {results_folder_path}. Found files: {db_files}"
            )

        if dbeaver_query_script_path is not None:
            attach_cmds = [
                f"DETACH DATABASE {result_name};\n\nattach '{windows_path}' as {result_name};\n"
                for result_name, windows_path in windows_loc
            ]
            COLUMNS = [
                "note_id",
                "patient_id",
                "note_date",
                "search_term",
                "window_text",
                "is_negated",
                "is_patient_communication",
                "is_note_within_visit",
                "problem_list_notes_group",
                "outpatient_notes_group",
                "communication_encounter_notes_group",
                "inpatient_notes_group",
                "admission_notes_group",
                "emergency_department_notes_group",
                "ecg_impression_notes_group",
                "discharge_summary_notes_group",
            ]

            SELECT_SUBQUERY = [
                "SELECT "
                + ", ".join(COLUMNS)
                + f" FROM sqlite_scan('{path}', 'results') "
                for name, path in windows_loc
            ]
            unioned_subqueries = "\nUNION ALL\n".join(SELECT_SUBQUERY)
            experimental_cte_check = (
                "with virtual_results as (\n"
                + unioned_subqueries
                + "\n)\nselect * from virtual_results\nlimit 10;"
            )

            CREATE_TABLE_QUERY = """

-- drop table if exists consolidated_results;

CREATE table consolidated_results (
    note_id TEXT,
    patient_id TEXT,
    note_date TEXT,
    search_term TEXT,
    window_text TEXT,
    is_negated INTEGER,
    is_patient_communication INTEGER,
    is_note_within_visit INTEGER,
    problem_list_notes_group INTEGER,
    outpatient_notes_group INTEGER,
    communication_encounter_notes_group INTEGER,
    inpatient_notes_group INTEGER,
    admission_notes_group INTEGER,
    emergency_department_notes_group INTEGER,
    ecg_impression_notes_group INTEGER,
    discharge_summary_notes_group INTEGER
);
"""

            insert_queries = [
                f"insert into consolidated_results {x};" for x in SELECT_SUBQUERY
            ]

            assert dbeaver_query_script_path is not None and isinstance(
                dbeaver_query_script_path, Path
            )
            dbeaver_query_script_path.parent.mkdir(parents=True, exist_ok=True)

            with open(dbeaver_query_script_path, "w") as f:
                test_cte = (
                    experimental_cte_check
                    + "\n)\nselect * from virtual_results\nlimit 10;"
                )

                f.write(
                    f"-- Database file path: {dbeaver_query_script_path}\n"
                    f"-- Results audit log path: {self._result_data_store_folder.results_audit_log_path}\n"
                    f"-- Results folder path: {results_folder_path}\n"
                    f"\n"
                    f"-- Setup\nINSTALL sqlite_scanner; LOAD sqlite_scanner;"
                    f"\n"
                    f"-- SQL command to create consolidated_results schema and results table:\n\n"
                    f"{CREATE_TABLE_QUERY}\n"
                    f"\n\n-- Individual insert statements for each attached database:\n\n"
                    f"{chr(10).join(insert_queries)}"
                )

        self.close_database(sql_db_path)

    @staticmethod
    def close_database(sql_db_path, worker_id=None):
        conn = sqlite3.connect(sql_db_path)
        try:
            if worker_id is not None:
                logger.info("Closing out processing for worker {}...", worker_id)
            else:
                logger.info("Closing database at {}...", sql_db_path)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA wal_checkpoint(FULL);")
            conn.commit()
            conn.close()
        except:
            if worker_id is not None:
                logger.warning(
                    "Error during closing out processing for worker {}. This may indicate uncommitted transactions or issues with the database file.",
                    worker_id,
                )
            else:
                logger.warning(
                    "Error during closing database at {}. This may indicate uncommitted transactions or issues with the database file.",
                    sql_db_path,
                )
        finally:
            del conn

    @property
    def results_path(self) -> Path:
        return self._result_data_store_folder.worker_results_path

    def _exec(self, func: Callable[[sqlite3.Cursor], Any], *args, **kwargs):
        with sqlite3.connect(self.results_path) as conn:
            # Enable WAL mode for concurrent reads/writes
            conn.execute("PRAGMA journal_mode=WAL;")
            # Set synchronous mode to NORMAL for safety without excessive slowdown
            conn.execute("PRAGMA synchronous=NORMAL;")
            try:
                cursor: sqlite3.Cursor = conn.cursor()
                ret_val: Any = func(cursor, *args, **kwargs)
                conn.commit()
                return ret_val
            except Exception as e:
                logger.error(f"Error executing function with lock: {e}")
                conn.rollback()
                raise

    def _does_results_table_exist(self):
        return self._exec(
            lambda cursor: cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                (self.results_table_name,),
            ).fetchone()
            is not None
        )

    @process_lock()
    def get_last_batch(self):
        """
        Return the maximum batch_group value from the results table, or None if no rows exist.
        """

        def query(cursor: sqlite3.Cursor):
            cursor.execute(f"SELECT MAX(batch_group) FROM {self.results_table_name};")
            row = cursor.fetchone()
            val = row[0] if row else None
            next_batch_group: int = int(val) + 1 if val is not None else 1
            return next_batch_group

        return self._exec(query)

    @process_lock()
    def _init_table(self) -> None:
        """
        Initialize the results table in the database if it doesn't already exist.
        This method checks if the table exists in memory cache or in the database.
        If the table doesn't exist, it creates a new table with the schema defined
        in TABLE_SCHEMA, mapping pandas data types to SQL types and adding an
        auto-incrementing primary key.
        The method performs the following steps:
        1. Returns immediately if table is already known to exist (cached check)
        2. Checks if the table exists in the database
        3. If not, builds a CREATE TABLE statement based on TABLE_SCHEMA
        4. Executes the CREATE TABLE statement
        5. Sets the internal flag to mark the table as existing
        Side Effects:
            - Updates self._table_exists flag to True
            - Creates a new 'results' table in the database if it doesn't exist
        Returns:
            None
        """

        self._table_exists = self._table_exists or self._does_results_table_exist()
        if self._table_exists is True:
            logger.info("Results table exists.")
            return

        def build_query() -> str:
            # Map pandas dtypes to SQL types
            dtype_mapping = {
                "int64": "INTEGER",
                "bool": "BOOLEAN",
                "str": "TEXT",
                "date": "DATE",
            }

            columns = ["result_id INTEGER PRIMARY KEY AUTOINCREMENT"]
            for col, dtype in TABLE_SCHEMA.items():
                sql_type = dtype_mapping.get(
                    dtype, "TEXT"
                )  # Default to TEXT for unknown types
                columns.append(f"{col} {sql_type}")

            create_stmt: str = (
                f"CREATE TABLE IF NOT EXISTS {self.results_table_name} ({', '.join(columns)})"
            )
            return create_stmt

        logger.info("Building ")
        self._exec(lambda cursor: cursor.execute(build_query()))
        logger.info("Results table initialized for worker {}.", self.worker_id)

        self._table_exists = True

    @process_lock()
    def record_results(self, records: List[ResultRecord]):
        """
        Insert multiple ResultRecord objects into the persistent 'results' SQLite table.
        This method takes a sequence of ResultRecord instances and writes one row per record
        into the database table named "results". Each record is inserted with a parameterized
        INSERT statement using the following columns:
        - note_id
        - batch_group
        - window_text
        - search_term_to_note_groups_id
        - window_start_char_offset
        - window_end_char_offset
        - entity_start_offset
        - entity_end_offset
        - is_negated
        - note_date
        - visit_start_date
        - visit_end_date
        Behavior:
        - If the provided `records` list is empty or falsy, the method logs a warning and
            returns immediately without performing any database writes.
        - For non-empty input, the method calls self._exec(callback) where `callback` is a
            function that receives a sqlite3.Cursor and performs the individual INSERTs.
        - Inserts are performed with bound parameters (no string interpolation), preventing
            SQL injection from record fields.
        Args:
                records (List[ResultRecord]): Iterable of ResultRecord objects to persist. Each
                        object is expected to provide the attributes referenced above.
        Returns:
                None
        Raises:
                sqlite3.Error: If an error occurs during execution of the SQL statements. The
                        exact propagation and transaction/commit semantics depend on the
                        implementation of self._exec; callers should be prepared to handle
                        sqlite3 exceptions if the underlying operation fails.
        Notes:
        - This method does not perform de-duplication or validation beyond using the record
            attributes as bind parameters; callers should ensure records are valid for the
            intended schema constraints (e.g., uniqueness, foreign keys).
        - Transactional guarantees (atomicity/rollback) are determined by self._exec.
        """

        if not records:
            logger.warning("No records to write.")
            return

        def write_records(cursor: sqlite3.Cursor):
            logger.info("Writing {} records to database for worker {}...", len(records), self.worker_id)
            insert_values = [
                (
                    int(record.note_id),
                    int(record.batch_group),
                    int(record.person_id),
                    record.window_text,
                    (
                        record.note_date.isoformat()
                        if hasattr(record.note_date, "isoformat")
                        else str(record.note_date)
                    ),
                    record.search_term,
                    bool(record.problem_list_notes_group),
                    bool(record.outpatient_notes_group),
                    bool(record.communication_encounter_notes_group),
                    bool(record.inpatient_notes_group),
                    bool(record.admission_notes_group),
                    bool(record.emergency_department_notes_group),
                    bool(record.ecg_impression_notes_group),
                    bool(record.discharge_summary_notes_group),
                    bool(record.is_patient_communication),
                    bool(record.is_note_within_visit),
                    bool(record.is_negated),
                    int(record.window_start_char_offset),
                    int(record.window_end_char_offset),
                    int(record.entity_start_offset),
                    int(record.entity_end_offset),
                )
                for record in records
            ]

            cursor.executemany(
                f"""
                INSERT INTO {self.results_table_name} (
                    {results_field_list()}
                ) VALUES ({', '.join("?" for _ in range(len(TABLE_SCHEMA.keys())))})""",
                insert_values,
            )

        self._exec(write_records)

    def chunk_iter(self, chunk_size: int):
        """
        Iterate over results from the database in chunks.
        This method yields batches of results from the results table, fetching
        them in chunks of the specified size to manage memory efficiently when
        dealing with large datasets.
        Args:
            chunk_size (int): The number of rows to fetch in each chunk.
                Must be at least 1.
        Yields:
            list: A batch of results (rows) from the database, where each batch
                contains up to `chunk_size` rows.
        Raises:
            ValueError: If chunk_size is less than 1.
        Example:
            >>> for batch in data_store.chunk_iter(chunk_size=100):
            ...     process_batch(batch)
        """

        if chunk_size < 1:
            raise ValueError("Chunk size must be at least 1.")

        base_query: str = (
            f"SELECT {results_field_list()} FROM {self.results_table_name}"
        )

        offset = 0
        while True:
            query: str = f"{base_query} LIMIT {chunk_size} OFFSET {offset}"

            def fetch_batch(cursor: sqlite3.Cursor):
                cursor.execute(query)
                results = cursor.fetchall()
                return results

            batch = self._exec(fetch_batch)

            if not batch:
                break

            yield batch
            offset += chunk_size
