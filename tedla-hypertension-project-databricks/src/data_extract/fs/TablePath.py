# from abc import ABC, abstractmethod
# from typing import Literal

# from nlp_method.fs import PATH_PATTERN, get_dbutils
# from nlp_method.fs.TableDefBase import TableDefBase


# class TablePath(ABC):
#     """
#     Abstract base class representing a filesystem-backed table path.
#     This class encapsulates the construction and basic inspection of a table
#     location on a filesystem (either Databricks DBFS or a local/file path).
#     It is designed to be subclassed to provide concrete behavior for cleaning
#     or managing the table-specific storage.
#     Args:
#         prefix (Literal["dbfs", "file"]):
#             The prefix that identifies the filesystem type. Valid values are
#             "dbfs" and "file". When used, get_path(with_prefix=True) will
#             prepend "<prefix>:" to the returned path.
#         folder_root (str | None):
#             The root folder (absolute or relative, depending on PATH_PATTERN)
#             under which table files are stored. Must match PATH_PATTERN and
#             cannot be None.
#         table_def (TableDefBase):
#             An instance describing the table (for example, providing
#             table_filename). TablePath uses table_def.table_filename to
#             construct the concrete path.
#     Attributes:
#         _folder_root (str):
#             Validated folder root supplied at initialization.
#         _table_def (TableDefBase):
#             Table definition object provided at initialization.
#         _prefix (Literal["dbfs", "file"]):
#             The validated prefix provided at initialization.
#         _dbutils:
#             A DBUtils-like object obtained via get_dbutils() used to query
#             the filesystem (e.g., to list directory contents).
#     Properties:
#         exists -> bool:
#             True when the path contains one or more files (i.e. file_count > 0).
#             Determined by attempting to list files with _dbutils and treating
#             any error as absence (False).
#         file_count -> int:
#             Number of entries returned by listing the directory at the table
#             path. If the underlying filesystem listing raises an exception,
#             this property returns 0.
#     Methods:
#         clean() -> None:
#             Abstract method that subclasses must implement to perform any
#             cleanup/removal of table files or directories. Implementations
#             should raise or handle exceptions as appropriate for the target
#             filesystem.
#         get_path(with_prefix: bool = False) -> str:
#             Build and return the path to the table by joining folder_root and
#             table_def.table_filename. If with_prefix is True, the returned
#             string is prefixed with "<prefix>:" (for example "dbfs:/path/...").
#     Raises:
#         ValueError:
#             - If folder_root is None.
#             - If folder_root does not match PATH_PATTERN.
#             - If prefix is not one of "dbfs" or "file".
#     Notes:
#         - This class depends on external symbols PATH_PATTERN, TableDefBase, and
#           get_dbutils(). The semantics of table_def.table_filename and the
#           exact PATH_PATTERN are defined elsewhere.
#         - file_count silently treats any exception from _dbutils.fs.ls as zero
#           files; callers that need to distinguish errors should override or
#           query _dbutils directly.
#     Example:
#         Subclasses should implement clean() to remove files specific to the
#         storage backend, for example by using _dbutils.fs.rm(...) on DBFS or
#         os.remove(...) for local storage.
#     """

#     def __init__(
#         self,
#         prefix: Literal["dbfs", "file"],
#         folder_root: str | None,
#         table_def: TableDefBase,
#     ) -> None:
#         if folder_root is None:
#             raise ValueError("folder_root cannot be None")
#         if not PATH_PATTERN.match(folder_root):
#             raise ValueError(f"Invalid folder_root: {folder_root}")
#         if prefix not in ["dbfs", "file"]:
#             raise ValueError(f"Invalid prefix: {prefix}")

#         self._folder_root: str = folder_root
#         self._table_def: TableDefBase = table_def
#         self._prefix: Literal["dbfs", "file"] = prefix
#         self._dbutils = get_dbutils()

#         self.mkdirs(self._folder_root)

#     @property
#     def exists(self) -> bool:
#         return self.file_count > 0

#     @property
#     def file_count(self) -> int:
#         tbl_path: str = self.get_table_data_path()
#         dbfs_file_count = 0
#         try:
#             dbfs_file_count = len(self._dbutils.fs.ls(tbl_path))
#         except Exception as ex:
#             dbfs_file_count = 0
#         return dbfs_file_count

#     @abstractmethod
#     def clean(self) -> None:
#         raise NotImplementedError("clean")

#     def get_table_data_path(self, with_prefix: bool = False):
#         path = f"{self._folder_root}/{self._table_def.schema_dot_table}"
#         return f"{self._prefix}:{path}" if with_prefix else path

#     def mkdirs(self, pth: str):
#         self._dbutils.fs.mkdirs(pth)
