import time

from loguru import logger


class Timer:
    def __init__(self, name: str = ''):
        self.start_time = None
        self.name = name if name == '' else f"{name} "

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter()
        logger.info(f"{self.name}code executed in {end_time - self.start_time} seconds")
