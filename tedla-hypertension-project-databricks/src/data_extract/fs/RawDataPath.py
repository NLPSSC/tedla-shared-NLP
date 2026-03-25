# import os

# from nlp_method.fs.DBFSTablePath import TableExportPath
# from nlp_method.fs.TableDefBase import TableDefBase


# class RawDataPath(TableExportPath):
#     """
#     RawDataPath(table_def)
#     A small convenience subclass of DBFSTablePath that builds a DBFS-backed path for raw data
#     tables using the DBFS root folder specified in the environment.
#     This class reads the root folder from the TABLE_EXPORT_FOLDER_PATH environment variable and passes
#     that value along with the provided table definition to the DBFSTablePath constructor.
#     Args:
#         table_def (TableDefBase): Object describing the table (name, schema, partitioning, etc.)
#             used by DBFSTablePath to construct the final DBFS path.
#     Behavior:
#         - Uses os.getenv("TABLE_EXPORT_FOLDER_PATH", None) to obtain the root folder.
#         - If the environment variable is unset, None is forwarded to the base class; how that
#           is handled (e.g., falling back to a default or raising) is determined by DBFSTablePath.
#     Example:
#         >>> td = TableDefBase(name="raw_events", ...)
#         >>> p = RawDataPath(td)
#         # p will represent the path rooted at TABLE_EXPORT_FOLDER_PATH for the given table_def.
#     """

#     def __init__(self, table_def: TableDefBase) -> None:
#         super().__init__(os.getenv("TABLE_EXPORT_FOLDER_PATH", None), table_def)
