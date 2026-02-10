"""
Pipeline Stages — CSC3301 Project 5: Concurrent Data Pipeline

This module defines the stage abstractions for the pipeline.
Each stage transforms data items as they flow through the pipeline.

Students must implement concrete stage classes that process data
using functional programming patterns (map, filter, reduce).
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Any, Iterator

T = TypeVar('T')
U = TypeVar('U')


class PipelineStage(ABC, Generic[T, U]):
    """Abstract base class for all pipeline stages.

    A stage receives items of type T and produces items of type U.
    Stages are composable — they can be chained together.
    """

    @abstractmethod
    def process(self, item: T) -> U:
        """Process a single item through this stage.

        Args:
            item: The input item to process

        Returns:
            The transformed item
        """
        ...

    def process_batch(self, items: Iterator[T]) -> Iterator[U]:
        """Process multiple items. Override for batch optimizations.

        Args:
            items: Iterator of input items

        Yields:
            Transformed items
        """
        # TODO: Implement batch processing
        ...


class MapStage(PipelineStage[T, U]):
    """Stage that applies a transformation function to each item.

    Example:
        stage = MapStage(str.upper)
        stage.process("hello")  # => "HELLO"
    """

    def __init__(self, func: Callable[[T], U]):
        """Initialize with a transformation function.

        Args:
            func: Function to apply to each item
        """
        # TODO: Store the function
        ...

    def process(self, item: T) -> U:
        # TODO: Apply self.func to item
        ...


class FilterStage(PipelineStage[T, T]):
    """Stage that filters items based on a predicate.

    Items passing the predicate are forwarded; others are dropped.

    Example:
        stage = FilterStage(lambda x: len(x) > 3)
        # Only passes strings longer than 3 characters
    """

    def __init__(self, predicate: Callable[[T], bool]):
        """Initialize with a predicate function.

        Args:
            predicate: Function returning True for items to keep
        """
        # TODO: Store the predicate
        ...

    def process(self, item: T) -> T | None:
        # TODO: Return item if predicate passes, None otherwise
        ...


class FlatMapStage(PipelineStage[T, U]):
    """Stage that maps each item to zero or more output items.

    Example:
        stage = FlatMapStage(lambda s: s.split())
        stage.process("hello world")  # => ["hello", "world"]
    """

    def __init__(self, func: Callable[[T], list[U]]):
        # TODO: Store the function
        ...

    def process(self, item: T) -> list[U]:
        # TODO: Apply function and return list of results
        ...
