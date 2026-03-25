# import os

# from nlp_method.fs.DBFSTablePath import TableExportPath
# from nlp_method.fs.TableDefBase import TableDefBase


# class TableDownloadPath(TableExportPath):
#     """Filesystem-backed DBFS table path.
#     This class is a thin wrapper around DBFSTablePath that supplies the base
#     filesystem folder from the WORKSPACE_DOWNLOAD_FOLDER environment variable.
#     Parameters
#     ----------
#     table_def : TableDefBase
#         Table definition object describing the table name, schema and any
#         metadata required by DBFSTablePath.
#     Behavior
#     --------
#     - Reads the environment variable WORKSPACE_DOWNLOAD_FOLDER at construction time and
#       forwards its value as the base folder to the superclass DBFSTablePath.
#     - If WORKSPACE_DOWNLOAD_FOLDER is not set, None is passed to the superclass and
#       the superclass is responsible for choosing any default behavior.
#     Exceptions
#     ----------
#     Any exception raised by DBFSTablePath.__init__ (for example, due to an
#     invalid table_def) will propagate to the caller.
#     Example
#     -------
#     # Constructing from an existing TableDefBase instance:
#     fs_path = FSTablePath(table_def)
#     """

#     def __init__(self, table_def: TableDefBase) -> None:
#         super().__init__(os.getenv("WORKSPACE_DOWNLOAD_FOLDER", None), table_def)
