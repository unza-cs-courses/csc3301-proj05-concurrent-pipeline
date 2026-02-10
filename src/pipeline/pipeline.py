"""
Pipeline — CSC3301 Project 5: Concurrent Data Pipeline

This module defines the main Pipeline class that orchestrates
concurrent data processing through multiple stages.

The Pipeline supports:
- Fluent API for stage composition
- Multiple concurrency modes (threading, multiprocessing, async)
- Configurable worker pools and buffer sizes
- Thread-safe data collection

Students must implement the Pipeline class and compose_stages helper.
"""
import queue
import threading
from typing import TypeVar, Generic, Callable, Any, Iterator, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from .stages import PipelineStage, MapStage, FilterStage

T = TypeVar('T')
U = TypeVar('U')


class Pipeline:
    """Main pipeline orchestrator for concurrent data processing.

    Connects multiple processing stages and executes them concurrently
    with configurable worker pools and buffering.

    Example usage:
        pipeline = Pipeline(
            stages=[MapStage(str.strip), FilterStage(bool), MapStage(str.upper)],
            workers=4,
            buffer_size=100
        )
        results = list(pipeline.process_batch(data))

    Args:
        stages: List of PipelineStage instances to execute in order
        workers: Number of concurrent workers (default: 4)
        buffer_size: Size of inter-stage buffers (default: 0 = unlimited)
    """

    def __init__(
        self,
        stages: list[PipelineStage] | None = None,
        workers: int = 4,
        buffer_size: int = 0
    ):
        # TODO: Initialize pipeline with stages, worker count, and buffer config
        ...

    def process(self, item: Any) -> Any:
        """Process a single item through all pipeline stages sequentially.

        Args:
            item: The input data item

        Returns:
            The fully transformed item after all stages
        """
        # TODO: Pass item through each stage in order
        ...

    def process_batch(self, items: Iterator[Any]) -> Iterator[Any]:
        """Process multiple items through the pipeline concurrently.

        Uses worker threads/processes to parallelize stage execution.
        Results are yielded as they complete.

        Args:
            items: Iterator of input data items

        Yields:
            Transformed items after all stages
        """
        # TODO: Implement concurrent batch processing
        # Hint: Use queue.Queue for inter-stage buffering
        # Hint: Use ThreadPoolExecutor for worker management
        ...

    @property
    def stages(self) -> list[PipelineStage]:
        """Return the list of pipeline stages."""
        # TODO: Return stored stages
        ...


def compose_stages(*stages: PipelineStage) -> Callable:
    """Compose multiple pipeline stages into a single function.

    Creates a function that applies all stages sequentially to an input.

    Args:
        *stages: Pipeline stages to compose

    Returns:
        A function that applies all stages in order

    Example:
        transform = compose_stages(
            MapStage(str.strip),
            MapStage(str.upper)
        )
        transform("  hello  ")  # => "HELLO"
    """
    # TODO: Return a composed function
    ...
