# import os

# from nlp_method.fs.TablePath import TablePath


# class WorkspaceTablePath(TablePath):
#     """
#     WorkspaceTablePath(doc)
#     Represents a TablePath that maps to a workspace-local filesystem location.
#     This class provides filesystem-aware cleanup and inspection utilities for
#     a path that represents a table stored in the local workspace. It expects
#     the underlying path to be accessible via the inherited get_path() and
#     exists attributes/methods from TablePath.
#     Behavior:
#     - clean()
#         Remove the filesystem entry pointed to by this path if it exists.
#         - If the path is a directory, it is removed recursively (shutil.rmtree).
#         - If the path is a file, it is removed (os.remove).
#         This method has side effects on the local filesystem and may raise
#         OSError (or subclass) on failure (permission issues, concurrent access, etc.).
#     - file_count -> int
#         Return the number of entries in the directory at this path:
#         - If the path exists and is a directory, returns len(os.listdir(path)).
#         - Otherwise returns 0.
#         This count reflects directory entries (files and subdirectories) and does
#         not recurse into subdirectories.
#     Notes:
#     - The class relies on standard os and shutil operations and does not
#       perform additional locking or transactional guarantees. Callers should
#       ensure the path is correct and be prepared to handle filesystem-related
#       exceptions.
#     - Intended for local/workspace use; not designed for remote or distributed
#       filesystems without appropriate path handling provided by the base class.
#     """

#     def clean(self):
#         if self.exists:
#             _path = self.get_table_data_path()
#             if os.path.isdir(_path):
#                 import shutil

#                 shutil.rmtree(_path)
#             else:
#                 os.remove(_path)

#     @property
#     def file_count(self) -> int:
#         fs_path = self.get_table_data_path()
#         path_exists = os.path.exists(fs_path)
#         return len(os.listdir(fs_path)) if path_exists and os.path.isdir(fs_path) else 0
