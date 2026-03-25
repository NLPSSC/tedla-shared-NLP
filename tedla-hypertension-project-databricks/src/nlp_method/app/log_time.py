from loguru import logger


def calculate_timing_details(start_time, end_time):
    delta = end_time - start_time
    return {
        "total_seconds": round(delta, 2),
        "total_minutes": round(delta / 60, 2),
        "total_hours": round(delta / 3600, 2),
    }


def log_execution_time(start_time, end_time):
    total_execution_time = calculate_timing_details(start_time, end_time)
    logger.info(
        "Total execution time: {:.2f} seconds / {:.2f} minutes / {:.2f} hours",
        total_execution_time["total_seconds"],
        total_execution_time["total_minutes"],
        total_execution_time["total_hours"],
    )
