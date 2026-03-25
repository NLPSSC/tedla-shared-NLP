# import re
# from threading import Lock
# from typing import Literal, TypeAlias

# DataFSLocation: TypeAlias = Literal["dbfs", "workspace"]

# PATH_PATTERN = re.compile(r"/.+(/.+)*")
# SPLIT_SIZE_IN_MB = 5
# DBFS_PATH_VALIDATION_PATTERN = re.compile(r"dbfs:/tmp(/.+)*")
# FS_PATH_VALIDATION_PATTERN = re.compile(
#     r"file:/Workspace/Users/[^/]+(/.+)*"
# )  # Made configurable by removing hardcoded user
# from loguru import logger

# _lock = Lock()


# def get_spark():
#     with _lock:
#         if hasattr(get_spark, "_spark") is False:
#             from pyspark.sql import SparkSession

#             spark = SparkSession.builder.getOrCreate()
#             setattr(get_spark, "_spark", spark)
#         return getattr(get_spark, "_spark")


# def get_dbutils():
#     try:
#         from pyspark.dbutils import DBUtils  # type: ignore
#         return DBUtils(get_spark())
#     except Exception as e:
#         logger.error("Error getting DBUtils, must be run in DataBricks: {}", e)
#         raise
