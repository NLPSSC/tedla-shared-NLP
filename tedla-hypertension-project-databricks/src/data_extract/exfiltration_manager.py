# import os
# from typing import Literal, TypeAlias, cast

# import pandas as pd
# from loguru import logger

# from nlp_method.fs import get_dbutils
# from nlp_method.fs.ExportMixin import ExportMixin
# from nlp_method.fs.TableDef import TableDef

# ExfiltrationState: TypeAlias = Literal[
#     "dbfs_created",
#     "dbfs_removed",
#     "output_created",
#     "output_removed",
#     "tar_created",
#     "tar_removed",
#     "split_created",
# ]

# SCHEMA = {
#     "table": "str",
#     "dbfs_created": "bool",
#     "dbfs_removed": "bool",
#     "output_created": "bool",
#     "output_removed": "bool",
#     "tar_created": "bool",
#     "tar_removed": "bool",
#     "split_created": "bool",
# }

# SPLIT_SIZE_IN_MB = 5
# EXFILTRATION_BATCH_SIZE = 50


# class ExfiltrationManager(ExportMixin):
#     """
#     Manage a per-table exfiltration status log persisted as a CSV file.
#     This class provides utilities to record and query boolean "exfiltration"
#     states for a specific TableDef. The log is stored in a CSV file whose path
#     is provided via the EXFILTRATION_LOG environment variable. The CSV is
#     expected to contain the columns described by the module-level SCHEMA
#     (mapping column name -> dtype) and a "table" column that holds the
#     table name (name_without_schema).
#     Behavior and responsibilities
#     - On initialization:
#         - Accepts either a TableDef instance or a string (table name) and
#             normalizes it into a TableDef.
#         - Reads EXFILTRATION_LOG from the environment. Raises ValueError if the
#             variable is not set or does not point to a ".csv" file.
#         - Ensures the CSV file exists and is initialized with the SCHEMA
#             columns if it is missing or empty.
#         - Ensures there is an entry (row) for the current table; if not, adds
#             one with all action columns set to False.
#     - Persistent read/write:
#         - Internal helpers read the CSV into a pandas.DataFrame and cast
#             column types according to SCHEMA. If reading fails, an empty typed
#             DataFrame is returned.
#         - Writes always cast the DataFrame to SCHEMA before persisting.
#     Public methods
#     - set_state(action):
#         - Mark the given action column as True for the current table.
#         - If the table does not already have a row in the CSV, a new row is
#             appended with that action set to True and other action columns False.
#         - `action` is expected to be a valid column name (often an enum member
#             like ExfiltrationState); invalid names will raise a KeyError when
#             used to index the DataFrame.
#     - get_state(action: ExfiltrationState | None = None):
#         - If action is provided: return the boolean value of that action for
#             the current table, or False if no row exists.
#         - If action is None: return a dict representation of the row for the
#             current table (column -> value) or False if no row exists.
#     Notes and exceptions
#     - Depends on externally defined identifiers:
#         - SCHEMA: mapping of column names to pandas dtypes used for casting.
#         - TableDef: an object with at least a name_without_schema attribute.
#         - ExfiltrationState: optional enum/type used to represent action names.
#     - Raises ValueError during initialization if EXFILTRATION_LOG is missing
#         or not a CSV path. Reading/writing the CSV may raise IO-related
#         exceptions or pandas errors which are not swallowed by the public API
#         (except where internal attempts to read are guarded).
#     - The implementation uses simple CSV persistence and is not safe for
#         concurrent writers. If multiple processes may update the same log,
#         coordinate access externally (file locks, a central service, or a DB).
#     Example usage (informal)
#     - Construct with a TableDef or table name string.
#     - Call set_state(SomeAction) to mark an action as done.
#     - Call get_state(SomeAction) to inspect a specific action, or call
#         get_state() to retrieve the full row mapping for the table.
#     """

#     def __init__(self, table: TableDef | str):
#         """
#         Initialize the exfiltration log helper.
#         Parameters
#         ----------
#         table : TableDef | str
#             A TableDef instance or a table name. If a string is provided, it is
#             wrapped as TableDef(table) and stored on the instance as self._table.
#         Behavior / side effects
#         -----------------------
#         - Reads the environment variable EXFILTRATION_LOG to obtain the filesystem path
#           of the CSV log file and stores it on the instance as self._exfiltration_log.
#         - Validates that EXFILTRATION_LOG is defined and that the filename ends with
#           '.csv'; raises ValueError otherwise.
#         - Checks the filesystem for the log file and its size. If the file does not
#           exist or has size 0, a new CSV file is created at that path using
#           pandas.DataFrame with column names taken from SCHEMA.keys() (no rows,
#           index=False).
#         - After preparing the log file, delegates further setup to self._init_table().
#         Raises
#         ------
#         ValueError
#             If the EXFILTRATION_LOG environment variable is not set or does not point
#             to a .csv file.
#         OSError
#             If filesystem operations (for example os.path.getsize or writing the CSV)
#             fail due to the path being inaccessible or other I/O problems.
#         """
#         if isinstance(table, str):
#             table = TableDef(table)
#         self._table: TableDef = table
#         self._exfiltration_log = os.getenv("EXFILTRATION_LOG", None)

#         if self._exfiltration_log is None:
#             raise ValueError("EXFILTRATION_LOG is not defined")
#         if self._exfiltration_log.endswith(".csv") is False:
#             raise ValueError("EXFILTRATION_LOG must be a csv file")
#         log_exists = os.path.exists(self._exfiltration_log)
#         file_size = os.path.getsize(self._exfiltration_log)

#         # Initialize the log file if it does not exist or is empty
#         if not log_exists or file_size == 0:
#             self._write_log(pd.DataFrame(columns=list(SCHEMA.keys())))

#         self._dbutils = get_dbutils()

#         self._init_table()

#     @property
#     def source_table(self) -> TableDef:
#         return self._table

#     def exfiltrate(self):
#         # build dbfs data, if needed
#         self._export_data()

#         # Archive exported data to tar file in dbfs
#         self._archive_exported_data()

#         # Make splits, if needed
#         self._split_archive()

#         # Move splits to workspace
#         self._move_split_archive_to_workspace_for_download()

#         # Emit instructions for later use on the local machine
#         self._emit_instructions()

#     def _export_data(self):
#         if self.get("dbfs_created"):
#             if not self.source_table.export_path.exists:
#                 raise ValueError(
#                     "Export data marked as created, but the data does not exist at {}",
#                     self.source_table.export_path.get_table_data_path(),
#                 )
#             return

#         self._export_data()

#     def _archive_exported_data(self):

#         table_def: TableDef = self.source_table

#         if not self.get("tar_created") and all(
#             [
#                 self.get(cast(ExfiltrationState, x))
#                 for x in ["dbfs_created", "output_created"]
#             ]
#         ):
#             try:
#                 tar_archive_path: str = table_def.tar_archive_path.get_table_data_path()
#                 if "/tmp" not in tar_archive_path:
#                     raise ValueError("Tar archive path must be in /tmp")
#                 export_data_path: str = table_def.export_path.get_table_data_path()
#                 if "/tmp" not in export_data_path:
#                     raise ValueError("Export data path must be in /tmp")

#                 arguments = [
#                     "tar",
#                     "-cf",
#                     tar_archive_path,
#                     export_data_path,
#                 ]

#                 start_log_message = f"Creating tar archive: {tar_archive_path}; calling {' '.join(arguments)}..."
#                 end_log_message = f"Created tar archive: {tar_archive_path}."

#                 self._execute_process(start_log_message, end_log_message, arguments)
#                 self.set("tar_created")

#             except Exception as ex:
#                 logger.error(ex)
#                 raise

#         if self.get("tar_created") and all(
#             [
#                 self.get(cast(ExfiltrationState, x))
#                 for x in ["dbfs_created", "output_created"]
#             ]
#         ):

#             try:
#                 table_def.workspace_path.clean()
#                 self.set("output_removed")
#             except Exception as ex:
#                 logger.error(ex)
#                 raise

#     def _emit_instructions(self):
#         download_instructions = f"databricks workspace export-dir {self.source_table.split_archive_path.get_table_data_path()} ./{self.source_table.schema_dot_table}"
#         logger.info(
#             "To download the table data, run the following command in your terminal:"
#         )
#         logger.info(download_instructions)

#     def _split_archive(self):

#         table_def: TableDef = self.source_table

#         if not self.get("split_created") and all(
#             [
#                 self.get(cast(ExfiltrationState, x))
#                 for x in ["dbfs_created", "output_created", "tar_created"]
#             ]
#         ):
#             try:
#                 tar_path = table_def.tar_archive_path.get_table_data_path()
#                 splits_path = table_def.split_archive_path.get_table_data_path()
#                 start_log_message = f"Splitting tar archive {tar_path} into {SPLIT_SIZE_IN_MB}MB parts..."
#                 end_log_message = f"Split tar archive into {SPLIT_SIZE_IN_MB}MB parts with suffix '.part'"

#                 cmd_arguments = [
#                     "split",
#                     "-b",
#                     f"{SPLIT_SIZE_IN_MB}m",
#                     tar_path,
#                     splits_path,
#                 ]

#                 self._execute_process(start_log_message, end_log_message, cmd_arguments)

#                 self.set("split_created")
#                 table_def.tar_archive_path.clean()
#                 self.set("tar_removed")
#             except Exception as ex:
#                 logger.error(ex)
#                 raise

#     def _move_split_archive_to_workspace_for_download(self):
#         table_def = self.source_table

#         if not self.get("output_created") and self.get("dbfs_created"):

#             _export_path = table_def.export_path.get_table_data_path()
#             _workspace_download_folder = table_def.workspace_path.get_table_data_path()
#             logger.info(f"Moving {_export_path} to {_workspace_download_folder}...")
#             try:

#                 self._dbutils.fs.mkdirs(_workspace_download_folder)
#                 self._dbutils.fs.mv(_export_path, _workspace_download_folder, recurse=True)
#                 logger.info(f"Moved {_export_path} to {_workspace_download_folder}")

#                 self.set("output_created")

#             except Exception as ex:
#                 logger.error(ex)
#                 raise

#         if self.get("output_created") and self.get("dbfs_created"):
#             try:
#                 table_def.export_path.clean()
#                 self.set("dbfs_removed")
#             except Exception as ex:
#                 logger.error(ex)
#                 raise

#     def _execute_process(self, start_log_message, end_log_message, cmd_arguments):
#         logger.info(start_log_message)
#         import subprocess

#         subprocess.run(cmd_arguments, check=True)

#         logger.info(end_log_message)

#     def _open_log(self):
#         """
#         Open and prepare the exfiltration log for the current table.
#         This method attempts to read a CSV log file whose path is stored in
#         self._exfiltration_log and returns a tuple (df, table_mask):
#         - df (pandas.DataFrame):
#             - If the file exists and has non-zero size, it is read with pandas.read_csv(index_col=False).
#               If the loaded DataFrame has any rows, its columns are cast to the expected SCHEMA.
#             - If the file does not exist, has zero size, or an error occurs while reading/parsing,
#               an empty DataFrame with columns from SCHEMA is returned.
#             - The method guarantees that a DataFrame is returned (never None) or raises AssertionError
#               if self._exfiltration_log is None.
#         - table_mask (pandas.Series of bool):
#             - A boolean mask selecting rows in df that belong to the current table,
#               computed as df["table"] == self._table.name_without_schema.
#             - The mask is aligned with df (same index and length).
#         Notes and side effects:
#         - Uses filesystem checks (os.path.exists and os.path.getsize) to determine whether to attempt reading.
#         - Any exception raised while reading or casting the existing file is swallowed and causes the method
#           to fall back to an empty DataFrame with the expected schema.
#         - This method does not modify the file system or write to the log file.
#         - Preconditions:
#             - self._exfiltration_log must not be None (AssertionError otherwise).
#             - SCHEMA must be defined and appropriate for astype casting of the DataFrame columns.
#         Returns:
#             tuple[pd.DataFrame, pd.Series]: (df, table_mask)
#         """
#         assert self._exfiltration_log is not None
#         file_exists = (
#             os.path.exists(self._exfiltration_log)
#             and os.path.getsize(self._exfiltration_log) > 0
#         )
#         df: pd.DataFrame | None = None
#         if file_exists:
#             try:
#                 df = pd.read_csv(self._exfiltration_log, index_col=False)
#                 if len(df) > 0:
#                     df = df.astype(SCHEMA)  # type: ignore
#             except Exception as ex:
#                 file_exists = False
#         else:
#             df = pd.DataFrame(columns=SCHEMA.keys()).astype(SCHEMA)  # type: ignore

#         assert df is not None, "DataFrame should not be None"
#         table_mask = df["table"] == self._table.table_name_only
#         return df, table_mask

#     def _write_log(self, df: pd.DataFrame):
#         """
#         Write the provided DataFrame to the instance's exfiltration log as a CSV file.

#         The DataFrame is first cast to the expected SCHEMA to normalize column types and order,
#         then written to the path stored in self._exfiltration_log with the DataFrame index omitted.

#         Args:
#             df (pandas.DataFrame): DataFrame containing the records to be logged. It will be
#                 converted with df.astype(SCHEMA) prior to writing.

#         Raises:
#             TypeError, ValueError: If casting the DataFrame to SCHEMA fails (e.g., due to
#                 incompatible dtypes or missing columns).
#             OSError: If writing the CSV fails due to filesystem or permission errors.

#         Notes:
#             - The output CSV will not include the DataFrame index (to_csv is called with index=False).
#             - SCHEMA and _exfiltration_log are expected to be defined on the module or the instance.
#             - Pandas-specific exceptions from astype or to_csv may also propagate to the caller.
#         """
#         df.astype(SCHEMA).to_csv(self._exfiltration_log, index=False)  # type: ignore

#     def _init_table(self):
#         """
#         Initialize an entry for the current table in the exfiltration log.

#         This private helper:
#         - Calls self._open_log() to obtain (df, table_mask).
#         - If table_mask indicates an existing row for the current table, does nothing.
#         - Otherwise, constructs a new row where every column except "table" is False,
#             sets "table" to self._table.name_without_schema, appends the row to the DataFrame,
#             and writes the updated DataFrame back to the CSV at self._exfiltration_log.

#         Behavior and side effects:
#         - Mutates persistent state by creating or updating the CSV file at self._exfiltration_log.
#         - Assumes the DataFrame returned by self._open_log() has a "table" column and
#             other boolean-like columns.
#         - Uses pandas for DataFrame concatenation and CSV output.

#         Returns:
#         - None

#         Raises:
#         - Propagates I/O and pandas-related exceptions that may occur when reading or
#             writing the CSV or manipulating the DataFrame (e.g. FileNotFoundError, OSError,
#             pandas errors).
#         """
#         df, table_mask = self._open_log()
#         if table_mask.any():
#             return
#         # Add a new row if table not found
#         new_row: dict[str, bool | str] = {
#             col: False for col in df.columns if col != "table"
#         }
#         new_row["table"] = self._table.table_name_only
#         df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
#         self._write_log(df)

#     def set(self, action):
#         """
#         Set the state of an action flag for the current table in the exfiltration log.
#         This method opens the exfiltration log (via self._open_log()) which returns a
#         pandas.DataFrame and a boolean mask that identifies rows for the current
#         table. If a matching row exists, the column named by `action` is set to True
#         for those rows. If no matching row is found, a new row is appended for the
#         current table: all existing boolean/action columns (except "table") are set to
#         False, the "table" column is set to self._table.name_without_schema, and the
#         given `action` column is set to True (creating the column if it did not
#         previously exist). The updated DataFrame is then written back to CSV at
#         self._exfiltration_log.
#         Args:
#             action (str): The name of the action/flag column to set to True for the
#                 current table. If the column does not exist in the DataFrame it will
#                 be created.
#         Returns:
#             None
#         Side effects:
#             - Reads and writes the CSV file located at self._exfiltration_log.
#             - May add a new column to the DataFrame/CSV when `action` is not already a
#               column name.
#             - Persists changes by calling DataFrame.to_csv(..., index=False).
#         Raises:
#             - Any exceptions raised by self._open_log(), pandas operations (e.g.,
#               KeyError, ValueError), or file I/O (e.g., PermissionError, OSError)
#               may propagate to the caller.
#         Notes:
#             - The method relies on self._open_log() to return (df, table_mask) where
#               table_mask is a boolean pandas Series/array aligned to df.
#             - This implementation is not synchronized for concurrent access: concurrent
#               calls may lead to race conditions or lost updates when multiple processes
#               or threads modify the same CSV file.
#         """
#         df, table_mask = self._open_log()

#         # Instead of: if mask:
#         if table_mask.any():
#             # Update the action column for matching rows
#             df.loc[table_mask, action] = True
#         else:
#             # Add a new row if table not found
#             new_row: dict[str, bool | str] = {
#                 col: False for col in df.columns if col != "table"
#             }
#             new_row["table"] = self._table.table_name_only
#             new_row[action] = True
#             df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
#         self._write_log(df)

#     def get(
#         self, action: ExfiltrationState | None = None
#     ) -> bool | dict[ExfiltrationState | str, bool | str]:
#         """
#         Return the current exfiltration log state or a specific field from the latest matching record.
#         This method opens the underlying log (via self._open_log()), filters rows using the
#         returned table_mask, and considers only the first matching record (if any).
#         Parameters
#         ----------
#         action : ExfiltrationState | None, optional
#             If provided, the value for this key is returned from the first matching record.
#             If None, the entire record (as a dict) is returned.
#         Returns
#         -------
#         dict | Any | bool
#             - If no matching record is found, returns False.
#             - If a matching record is found and action is None, returns the record as a dict
#               (keys correspond to DataFrame columns).
#             - If a matching record is found and action is provided, returns the value for that
#               action key from the record.
#         Raises
#         ------
#         KeyError
#             If action is provided but does not exist as a key in the record dict.
#         Notes
#         -----
#         - Only the first record matching the table_mask is used; any additional matches are ignored.
#         - The method relies on self._open_log() to return a (DataFrame, boolean_mask) tuple.
#         """

#         df, table_mask = self._open_log()
#         records = df.loc[table_mask, :].to_dict(orient="records")
#         if len(records) > 0:
#             record = records[0]
#         else:
#             record = None
#         if record is None:
#             return False
#         if action is not None:
#             return cast(bool, record[action])
#         return cast(dict[ExfiltrationState | str, bool | str], record)


# # exfil_mgr: ExfiltrationManager = ExfiltrationManager(table_def)

# # # build dbfs data, if needed
# # exfil_mgr.export_data()

# # # Archive exported data to tar file in dbfs
# # exfil_mgr.archive_exported_data()

# # # Make splits, if needed
# # exfil_mgr.split_archive()

# # # Emit instructions for later use on the local machine
# # exfil_mgr.emit_instructions()

# # exfil_mgr.move_split_archive_to_workspace_for_download()
