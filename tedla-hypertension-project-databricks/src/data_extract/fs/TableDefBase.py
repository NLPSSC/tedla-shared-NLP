# from abc import ABC, abstractmethod


# class TableDefBase(ABC):
#     """
#     Abstract base for table definition objects.
#     Subclasses must implement the abstract `table_filename` property to provide
#     the filename (or path fragment) that identifies the table resource associated
#     with that concrete table definition.
#     Contract and expectations:
#     - `table_filename` must return a str.
#     - The returned string should be a filename or a relative path (for example
#         "patients.csv" or "subdir/my_table.parquet"). Whether it is interpreted as
#         relative to a project data directory or as an absolute path is determined
#         by the code that consumes the TableDef instance.
#     - The value should be stable and uniquely identify the table within the
#         context of the project (avoid including transient information such as
#         timestamps unless intentionally part of the name).
#     - Implementations should avoid returning empty strings or None.
#     Usage example:
#             class MyTable(TableDefBase):
#                             return "my_table.csv"
#     Notes:
#     - This class provides only the interface/contract for table naming. It does
#         not perform I/O, validation of existence, or path resolution; those
#         responsibilities belong to the code that uses TableDef instances.
#     """

#     @property
#     @abstractmethod
#     def schema_dot_table(self) -> str:
#         raise NotImplementedError("def table_filename(self) -> str:")
