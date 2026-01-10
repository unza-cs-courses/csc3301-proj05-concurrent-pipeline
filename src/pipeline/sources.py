"""Data sources for the pipeline."""
from abc import ABC, abstractmethod
from typing import TypeVar, Iterator, Generic, Callable

T = TypeVar('T')

class DataSource(ABC, Generic[T]):
    """Abstract base for data sources."""
    
    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        pass
    
    def take(self, n: int) -> 'DataSource[T]':
        """Limit to first n items."""
        return LimitedSource(self, n)

class LimitedSource(DataSource[T]):
    def __init__(self, source: DataSource[T], limit: int):
        self._source = source
        self._limit = limit
    
    def __iter__(self) -> Iterator[T]:
        # YOUR CODE
        pass

class FileSource(DataSource[str]):
    """Read lines from file."""
    def __init__(self, path: str):
        self._path = path
    
    def __iter__(self) -> Iterator[str]:
        # YOUR CODE
        pass

class GeneratorSource(DataSource[T]):
    """Wrap a generator function."""
    def __init__(self, gen_func: Callable[[], Iterator[T]]):
        self._gen_func = gen_func
    
    def __iter__(self) -> Iterator[T]:
        # YOUR CODE
        pass
