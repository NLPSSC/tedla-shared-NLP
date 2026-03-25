# from typing import Literal
# from loguru import logger
# from pyspark.sql import dataframe as pysparkDataFrame

# from nlp_method.fs import get_dbutils
# from nlp_method.fs.DBFSTablePath import TableExportPath
# from nlp_method.fs.ExportMixin import ExportMixin
# from nlp_method.fs.FSTablePath import TableDownloadPath
# from nlp_method.fs.RawDataPath import RawDataPath
# from nlp_method.fs.TableArchiveSplitsPath import TableArchiveSplitsPath
# from nlp_method.fs.TableDefBase import TableDefBase
# from nlp_method.fs.TableTarArchivePath import TableTarArchivePath


# class TableDef(TableDefBase, ExportMixin):
#     """
#     Represents a logical table and provides access to common filesystem and archive paths
#     associated with that table.
#     This class encapsulates a table identifier (schema + table name) and lazily exposes
#     several path-like helpers that are constructed from that identifier. It is a small
#     wrapper around more specific path helper classes (FSTablePath, TarArchivePath,
#     RawDataPath/DBFSTablePath, SplitsTablePath) so higher-level code can refer to the
#     various locations related to a table in a consistent way.
#     Parameters
#     ----------
#     table : str
#         The table name without schema. Used as the base identifier for all derived paths.
#     schema : str, optional
#         The schema or namespace containing the table. Defaults to "default".
#     Properties
#     ----------
#     name_without_schema : str
#         The raw table name as provided to the constructor (no schema prefix).
#     table_filename : str
#         The fully qualified table identifier in the form "{schema}.{table}".
#     fs_parquet_folder : FSTablePath
#         Filesystem path helper pointing to the Parquet folder for this table.
#     tar_archive_path : TarArchivePath
#         Path helper representing the tar-archive location for this table's exported data.
#     raw_data_path : DBFSTablePath
#         Path helper for the raw/DBFS input data associated with the table.
#     splits_folder : SplitsTablePath
#         Path helper for the location where dataset splits (train/val/test) are stored.
#     Notes
#     -----
#     - The class itself does not perform I/O or validate the existence of any paths; it
#       only composes and exposes helper objects that encapsulate path logic.
#     - The path helper attributes are created at initialization and returned via read-only
#       properties to encourage immutability of the TableDef instance after construction.
#     - The exact behavior and API of the helper classes (FSTablePath, TarArchivePath,
#       RawDataPath/DBFSTablePath, SplitsTablePath) determine how the returned objects are
#       used (e.g., to create directories, list files, or construct concrete file paths).
#     Example
#     -------
#     td = TableDef("my_table", schema="analytics")
#     td.table_filename         # "analytics.my_table"
#     td.fs_parquet_folder      # FSTablePath instance pointing to parquet folder for the table
#     td.raw_data_path          # DBFSTablePath instance for raw data location
#     """

#     def __init__(self, table: str, schema: str = "default"):
#         self._schema = schema
#         self._table = table
#         self._workspace_path = TableDownloadPath(self)
#         self._tar_archive_path = TableTarArchivePath(self)
#         self._export_path = RawDataPath(self)
#         self._split_archive_path = TableArchiveSplitsPath(self)
#         self._dbutils = get_dbutils()

#     def _clean_path(self, path_to_clean: str):
#         # remove folder recursively
#         dbfs_file_count = 0
#         try:
#             dbfs_file_count = len(self._dbutils.fs.ls(path_to_clean))
#         except Exception as ex:
#             dbfs_file_count = 0

#         if dbfs_file_count > 0:
#             self._dbutils.fs.rm(path_to_clean, True)

#     def clean_folder(self, which: Literal["workspace", "tar", "export", "splits"]):
#         if which == "workspace":
#             self._clean_path(self.workspace_path.get_table_data_path())
#         elif which == "tar":
#             self._clean_path(self.tar_archive_path.get_table_data_path())
#         elif which == "export":
#             self._clean_path(self.export_path.get_table_data_path())
#         elif which == "splits":
#             self._clean_path(self.split_archive_path.get_table_data_path())
#         else:
#             raise ValueError(f"Unknown folder type: {which}")

#     @property
#     def table_name_only(self):
#         return self._table

#     @property
#     def schema_dot_table(self) -> str:
#         return f"{self._schema}.{self._table}"

#     @property
#     def workspace_path(self) -> TableDownloadPath:
#         return self._workspace_path

#     @property
#     def tar_archive_path(self) -> TableTarArchivePath:
#         return self._tar_archive_path

#     @property
#     def split_archive_path(self) -> TableArchiveSplitsPath:
#         return self._split_archive_path

#     @property
#     def export_path(self) -> TableExportPath:
#         return self._export_path

#     def _export_data(self):

#         dbfs_path: str = self.export_path.get_table_data_path()
#         schema_dot_table: str = self.schema_dot_table

#         try:

#             if self.export_path.exists:
#                 # if the DBFS path already exists, skip export
#                 logger.info(
#                     "The export for {} already exists at path {}. Skipping...",
#                     schema_dot_table,
#                     dbfs_path,
#                 )
#                 return

#             logger.info("Loading table {}", schema_dot_table)
#             pyspdf: pysparkDataFrame.DataFrame = spark.table(schema_dot_table)

#             logger.info(f"Writing table {schema_dot_table} to {dbfs_path}...")
#             pyspdf.write.format("delta").option("compression", "zstd").mode(
#                 "overwrite"
#             ).parquet(dbfs_path)

#             logger.info(f"Table {schema_dot_table} written to {dbfs_path}.")

#         except Exception as ex:
#             logger.error(ex)
#             raise
