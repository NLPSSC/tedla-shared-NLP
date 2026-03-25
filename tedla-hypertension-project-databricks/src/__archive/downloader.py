# from nlp_method.exfiltration_manager import ExfiltrationManager

# from nlp_method.fs.TableDef import TableDef


# class TableDataDownloadPrep:

#     def __init__(self):
#         pass

#     def __call__(self, table_def: TableDef):

#         exfil_mgr: ExfiltrationManager = ExfiltrationManager(table_def)

#         # build dbfs data, if needed
#         exfil_mgr._export_data()

#         # Archive exported data to tar file in dbfs
#         exfil_mgr._archive_exported_data()

#         # Make splits, if needed
#         exfil_mgr._split_archive()

#         # Emit instructions for later use on the local machine
#         exfil_mgr._emit_instructions()

#         exfil_mgr._move_split_archive_to_workspace_for_download()


# __all__ = ["TableDataDownloadPrep"]
