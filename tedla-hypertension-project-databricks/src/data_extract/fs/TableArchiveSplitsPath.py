# import glob
# import os

# from loguru import logger

# from nlp_method.fs.DBFSTablePath import TableExportPath
# from nlp_method.fs.TableDefBase import TableDefBase


# class TableArchiveSplitsPath(TableExportPath):
#     """
#     SplitsTablePath(table_def: TableDefBase)
#     Path helper for split archive parts stored in a configured "splits" folder.
#     This class is a thin specialization of DBFSTablePath that constructs and
#     manages filenames for archive parts produced by table-splitting workflows.
#     Archive parts produced/expected by this class use the suffix ".tar.zst.part".
#     Behavior
#     - The constructor obtains the folder root from the environment variable
#         ARCHIVE_SPLIT_PATH and delegates to the DBFSTablePath base class.
#     - get_path(with_prefix: bool = False) builds the path to the archive part for
#         the provided table definition. If with_prefix is True, the path is returned
#         prefixed with the instance prefix (e.g. "<prefix>:/<path>"); otherwise the
#         plain filesystem/DBFS path is returned. The returned filename always ends
#         with ".tar.zst.part".
#     - clean() finds all files whose names begin with the base archive path for the
#         table (i.e. "<folder_root>/<table_filename>*") and removes them from the
#         filesystem, logging each removal. This is a destructive operation.
#     Parameters
#     - table_def (TableDefBase): Table definition object. Must provide at least the
#         attribute "table_filename" (str), which is used to construct filenames.
#     Environment
#     - Reads ARCHIVE_SPLIT_PATH from the environment to determine the folder root. If
#         ARCHIVE_SPLIT_PATH is not set, None is passed to the base class (behavior then
#         depends on DBFSTablePath).
#     Methods
#     - get_path(with_prefix: bool = False) -> str
#             Returns the constructed path for the table's archive part, including the
#             ".tar.zst.part" suffix. If with_prefix is True the DBFS/prefix is prepended.
#     - clean() -> None
#             Removes all archive part files that match the base archive name (prefixing
#             allowed). Logs removals. May raise exceptions if file removal fails (e.g.
#             OSError, PermissionError) — callers should handle or allow these to propagate.
#     Examples
#     - Create an instance and obtain a path:
#             st = SplitsTablePath(table_def)
#             st.get_path()                  # "/<splits_folder>/<table_filename>.tar.zst.part"
#             st.get_path(with_prefix=True)  # "<prefix>:/<splits_folder>/<table_filename>.tar.zst.part"
#     - Clean up all parts for the table:
#             st.clean()
#     Notes
#     - This class relies on the behavior and attributes provided by DBFSTablePath
#         (e.g. _prefix, _folder_root); consult that base class for details about
#         prefix formatting and alternative folder resolution.
#     - Use clean() carefully: it deletes files matching the prefix and is not
#         reversible.
#     """

#     def __init__(self, table_def: TableDefBase) -> None:
#         super().__init__(os.getenv("ARCHIVE_SPLIT_PATH", None), table_def)

#     def get_table_data_path(self, with_prefix: bool = False):
#         path = f"{self._folder_root}/{self._table_def.schema_dot_table}"
#         return (f"{self._prefix}:/{path}" if with_prefix else path) + ".tar.zst.part"

#     def clean(self):
#         logger.info(
#             f"Cleaning up archive parts for table {self._table_def.schema_dot_table}..."
#         )
#         base_path = f"{self._folder_root}/{self._table_def.schema_dot_table}"
#         archive_parts = glob.glob(f"{base_path}*")
#         for archive_part in archive_parts:
#             logger.info(f"Removing archive part {archive_part}")
#             os.remove(archive_part)
#         logger.info(
#             f"Cleaned up archive parts for table {self._table_def.schema_dot_table}"
#         )
