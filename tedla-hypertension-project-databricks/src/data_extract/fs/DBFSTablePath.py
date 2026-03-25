# from nlp_method.fs.TableDefBase import TableDefBase
# from nlp_method.fs.TablePath import TablePath


# class TableExportPath(TablePath):
#     """Representation of a Databricks DBFS-backed table path.
#     This class specializes TablePath for the Databricks File System (DBFS). It relies on
#     a dbutils-like filesystem interface available as self._dbutils (provided by the
#     parent or runtime) to list and remove files under the table's path.
#     Args:
#         folder_root (str): Root folder for the table path (passed to the TablePath base).
#         table_def (TableDefBase): Table definition object containing metadata used to
#             construct the concrete path via the base class.
#     Attributes:
#         Inherits attributes and behavior from TablePath. Notably, get_path() is used to
#         compute the full DBFS path for this table.
#     Properties:
#         file_count (int): Number of entries returned by listing the DBFS directory at
#             get_path(). If an error occurs while listing (for example, if the path does
#             not exist or dbutils is unavailable), this property returns 0.
#     Methods:
#         clean(): Recursively remove the DBFS directory at get_path() by calling
#             self._dbutils.fs.rm(path, True). Exceptions raised by the underlying
#             dbutils.rm call are propagated to the caller.
#     Notes:
#         - The class assumes a dbutils-compatible object is available as self._dbutils.
#         - get_path() and other path-construction logic are implemented by the TablePath base.
#         - file_count deliberately swallows exceptions and returns 0 on failure to provide
#           a safe, read-only accessor for existence/emptiness checks.
#     """

#     def __init__(self, folder_root, table_def: TableDefBase) -> None:
#         super().__init__("dbfs", folder_root, table_def)

#     @property
#     def file_count(self) -> int:
#         try:
#             return len(self._dbutils.fs.ls(self.get_table_data_path()))
#         except Exception:
#             return 0

#     def clean(self):
#         self._dbutils.fs.rm(self.get_table_data_path(), True)
