"""Thread-safe data sinks."""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Any, List
import threading

T = TypeVar('T')
U = TypeVar('U')

class DataSink(ABC, Generic[T]):
    """Abstract base for data sinks."""
    
    @abstractmethod
    def consume(self, item: T) -> None:
        pass
    
    @abstractmethod
    def finalize(self) -> Any:
        pass

class CollectorSink(DataSink[T]):
    """Thread-safe collector into a list."""
    
    def __init__(self):
        self._items: List[T] = []
        self._lock = threading.Lock()
    
    def consume(self, item: T) -> None:
        # YOUR CODE - must be thread-safe!
        pass
    
    def finalize(self) -> List[T]:
        return self._items.copy()

class ReducerSink(DataSink[T], Generic[T, U]):
    """Thread-safe reduce operation."""
    
    def __init__(self, reducer: Callable[[U, T], U], initial: U):
        self._reducer = reducer
        self._accumulator = initial
        self._lock = threading.Lock()
    
    def consume(self, item: T) -> None:
        # YOUR CODE - must be thread-safe!
        pass
    
    def finalize(self) -> U:
        return self._accumulator
