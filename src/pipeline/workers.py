"""Concurrent worker pool."""
from enum import Enum
from typing import TypeVar, Generic, Callable, Iterator
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio

T = TypeVar('T')
U = TypeVar('U')

class ConcurrencyMode(Enum):
    THREADING = "threading"
    MULTIPROCESSING = "multiprocessing"
    ASYNC = "async"

class WorkerPool(Generic[T, U]):
    """Concurrent worker pool supporting multiple execution modes."""
    
    def __init__(
        self,
        processor: Callable[[T], U],
        mode: ConcurrencyMode = ConcurrencyMode.THREADING,
        workers: int = 4
    ):
        self._processor = processor
        self._mode = mode
        self._workers = workers
    
    def process(self, items: Iterator[T]) -> Iterator[U]:
        """Process items concurrently."""
        if self._mode == ConcurrencyMode.THREADING:
            yield from self._process_threaded(items)
        elif self._mode == ConcurrencyMode.MULTIPROCESSING:
            yield from self._process_multiprocess(items)
        else:
            yield from self._process_async(items)
    
    def _process_threaded(self, items: Iterator[T]) -> Iterator[U]:
        # YOUR CODE
        pass
    
    def _process_multiprocess(self, items: Iterator[T]) -> Iterator[U]:
        # YOUR CODE
        pass
    
    def _process_async(self, items: Iterator[T]) -> Iterator[U]:
        # YOUR CODE
        pass
