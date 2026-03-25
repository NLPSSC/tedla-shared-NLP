# import os

# from nlp_method.fs.TableDefBase import TableDefBase
# from nlp_method.fs.TablePath import TablePath


# class TableTarArchivePath(TablePath):
#     """
#     TarArchivePath(table_def)
#     Path helper for a table-level tar archive compressed with Zstandard (.tar.zst).
#     This class is a concrete TablePath implementation that builds and manipulates
#     paths pointing to a tar.zst archive for a given table. It expects the
#     associated TableDefBase instance to provide at least a `table_filename`
#     attribute.
#     Initialization
#     - table_def (TableDefBase): table definition object; used to derive the archive
#         filename (via table_def.table_filename).
#     - The base folder root is provided to the parent TablePath via the environment
#         variable TAR_ARCHIVE_PATH (if set). The parent class also provides a prefix
#         string (set to "file" for this subclass).
#     Behavior and API
#     - get_path(with_prefix: bool = False) -> str
#             Compose and return the filesystem path for the archive:
#             "<folder_root>/<table_filename>.tar.zst". If with_prefix is True the
#             returned path is prefixed as "<prefix>:/<path>".
#     - exists -> bool
#             True if any filesystem entry exists at the computed path (file or
#             directory). Uses os.path.exists internally.
#     - file_count -> int
#             If the computed path is a file returns 1.
#             If it is a directory returns the number of directory entries (len(os.listdir)).
#             Otherwise returns 0.
#     - clean() -> None
#             Remove the archive path:
#             - If the path is a directory, recursively remove it (shutil.rmtree).
#             - If the path exists and is not a directory, remove it (os.remove).
#             Note: this operation is destructive and may raise OSError / PermissionError
#             on failure.
#     Notes and expectations
#     - Relies on attributes provided by the parent TablePath (e.g., _folder_root, _prefix)
#         and on table_def.table_filename.
#     - Does not perform any archive-specific I/O (no creation or extraction of tar
#         contents) — it only manipulates the filesystem path and the underlying file
#         system entries.
#     - Callers should handle potential filesystem exceptions (permission errors,
#         concurrent modifications, missing environment configuration for folder root).
#     - Useful for code that needs a stable, canonical path to read, check, or remove
#         a table's compressed tar archive.
#     """

#     def __init__(self, table_def: TableDefBase) -> None:
#         super().__init__("file", os.getenv("TAR_ARCHIVE_PATH", None), table_def)

#     def get_table_data_path(self, with_prefix: bool = False):
#         path = f"{self._folder_root}/{self._table_def.schema_dot_table}"
#         return (f"{self._prefix}:/{path}" if with_prefix else path) + ".tar.zst"

#     @property
#     def exists(self) -> bool:
#         fs_path = self.get_table_data_path()
#         return os.path.exists(fs_path)

#     @property
#     def file_count(self) -> int:
#         fs_path = self.get_table_data_path()
#         if os.path.isfile(fs_path):
#             return 1
#         elif os.path.isdir(fs_path):
#             return len(os.listdir(fs_path))
#         return 0

#     def clean(self) -> None:
#         fs_path = self.get_table_data_path()
#         if os.path.isdir(fs_path):
#             import shutil

#             shutil.rmtree(fs_path)
#         elif os.path.exists(fs_path):
#             os.remove(fs_path)
