from loguru import logger

import multiprocessing as mp

from nlp_method.__main__ import worker_ready_timeout_seconds


from tqdm import tqdm

from nlp_method.nlp.nlp_worker import NLPWorker


def validate_workers_started(worker_started_events, processes):
    # Wait for all workers to signal that they are ready before proceeding
    # If there was a long timeout waiting for the workers to initialize, then
    # it's likely that they encountered an error during initialization.
    for event in tqdm(worker_started_events):
        is_ready: bool = event.wait(timeout=worker_ready_timeout_seconds)
        if not is_ready:
            for p in processes:
                if p.is_alive():
                    p.terminate()
            raise RuntimeError(
                "Timed out waiting for workers to initialize. "
                f"Timeout: {worker_ready_timeout_seconds} seconds."
            )


def assign_workers_to_processes(nlp_workers) -> list[mp.Process]:
    # Assign each NLPWorker to a separate process and start the processes.
    processes: list[mp.Process] = []
    for nlp_worker_idx, nlp_worker in enumerate(nlp_workers):
        logger.info(
            "Initialized NLPWorker {} with results database path", nlp_worker_idx
        )
        p = mp.Process(target=nlp_worker)
        processes.append(p)
        p.start()
    return processes


def create_nlp_workers(num_workers, queue) -> tuple[list[NLPWorker], list[mp.Process]]:
    # Create an event for each worker to signal when they have started
    worker_started_events = [mp.Event() for _ in range(num_workers)]

    # Initialize NLPWorker instances and assign them to processes
    nlp_workers: list[NLPWorker] = [
        nlp_worker
        for id in range(num_workers)
        if (nlp_worker := NLPWorker(id, queue, worker_started_events[id]))
    ]

    processes: list[mp.Process] = assign_workers_to_processes(nlp_workers)

    validate_workers_started(worker_started_events, processes)
    return nlp_workers, processes
