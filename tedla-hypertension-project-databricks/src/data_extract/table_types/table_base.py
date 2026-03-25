# from abc import ABC, abstractmethod
# from typing import Callable, Self, Union, Any

# from loguru import logger


# class TableBase(ABC, TableMixin):
#     def __init__(
#         self,
#         table_name: str,
#         /,
#         table_builder: Callable[["TableBase"], Any] | None = None,
#         query_piece: str | None = None
#     ):
#         self._table_name: str = table_name
#         self._query_piece: str | None = query_piece
#         self._table_builder: Callable[[TableBase], Any] | None = table_builder
    
#     @property
#     def table_name(self) -> str:
#         return self._table_name
    
#     @property
#     @abstractmethod
#     def schema(self) -> str:
#         raise NotImplementedError("Subclasses must implement schema method")

#     @property
#     @abstractmethod
#     def database(self) -> Union[str, None]:
#         raise NotImplementedError("Subclasses must implement database method")

#     @property
#     def fully_qualified_table_name(self) -> str:
#         pieces = [self.database, self.schema, self.table_name]
#         fqtn = ".".join([p for p in pieces if p is not None])
#         return fqtn

#     @staticmethod
#     def build_query_piece_list(vals):
#         return ",".join([TableBase.emit_piece_item(x) for x in vals])

#     @staticmethod
#     def emit_piece_item(x):
#         if isinstance(x, int):
#             return str(x)
#         return f"'{x}'"

#     def exists_in_catalog(self):
#         return self._table_name in [
#             table.name for table in spark.catalog.listTables("default")
#         ]

#     def wrap_query(self, query_piece: str) -> str:
#         return f"CREATE TABLE IF NOT EXISTS {self.fully_qualified_table_name} AS \n{query_piece}"

#     def get_query_piece(self):
#         return self._query_piece if self._query_piece else ""

#     def create(self) -> Self:
#         if self.exists_in_catalog():
#             logger.info(f"{self.fully_qualified_table_name} table already exists.")
#             return self

#         if self._table_builder is not None:
#             self._table_builder(self)
#             return self

#         logger.info(f"Building {self.fully_qualified_table_name} table...")
#         query_for_execution = self.wrap_query(self.get_query_piece())
#         logger.info("Executing query\n\n{}", query_for_execution)
#         spark.sql(query_for_execution)
#         logger.info(f"{self.fully_qualified_table_name} table built.")
#         self._post_execute_action()
#         return self
    
#     @abstractmethod
#     def _post_execute_action(self):
#         raise NotImplementedError("def _post_execute_action(self):")
    
#     def __str__(self):
#         return self.fully_qualified_table_name

#     def __repr__(self):
#         return self.fully_qualified_table_name


# class ProjectTable(TableBase):

#     @property
#     def schema(self) -> str:
#         return "default"

#     @property
#     def database(self) -> Union[str, None]:
#         return None
    
#     def _post_execute_action(self):
#         pass


# class ProjectView(ProjectTable):

#     def __init__(self, table_name: str, cache_view: bool = True, *args, **kwargs):
#         self._cache_view: bool = cache_view
#         super().__init__(table_name, *args, **kwargs)
        

#     @property
#     def table_name(self) -> str:
#         tbl_name = f"vw_{super().table_name}"
#         return tbl_name

#     def wrap_query(self, query_piece: str) -> str:
#         fqtn = self.fully_qualified_table_name
#         return f"CREATE VIEW IF NOT EXISTS {fqtn} AS \n {query_piece}"

#     def exists_in_catalog(self):
#         return self._table_name in [
#             v.name for v in spark.catalog.listTables("default") if v.tableType == "VIEW"
#         ]

#     def _post_execute_action(self):
#         logger.info(f"Caching view {self.fully_qualified_table_name}...")
#         spark.sql(f"CACHE TABLE {self.fully_qualified_table_name};")
#         logger.info(f"View {self.fully_qualified_table_name} cached.")


# class RDTable(TableBase):
#     def __init__(self, name: str):
#         super().__init__(name)

#     @property
#     def schema(self) -> str:
#         return "rd_omop_prod"

#     @property
#     def database(self) -> Union[str, None]:
#         return "victr_rd"
    
#     def _post_execute_action(self):
#         pass
