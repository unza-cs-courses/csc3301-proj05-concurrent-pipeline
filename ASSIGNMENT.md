# Project 5: Concurrent Data Pipeline

**CSC3301 Programming Language Paradigms**
**Student ID:** pipeline
**Variant Hash:** 23bf0d244a4cb62c
**Weight:** 5.5% | **Capstone Project**

---

## Your Unique Assignment Parameters

This assignment has been personalized for you. Your implementation must meet these specific requirements:

### Worker Pool Configuration

| Parameter | Your Value |
|-----------|------------|
| Thread Workers | 4 |
| Process Workers | 3 |
| Async Workers | 5 |
| Batch Size | 54 |

### Required Transformations

Your pipeline must implement these transformation stages:

1. **strip**: Remove whitespace
   - Implementation: `str.strip`
2. **title**: Title case
   - Implementation: `str.title`

### Required Filter

Your pipeline must filter data using:

- **starts_with_a**: Starts with 'a'
- Implementation: `lambda x: x.lower().startswith('a')`

### Required Reducer

Your sink must implement this reducer operation:

- **count**: Count items
- Initial value: `0`
- Implementation: `lambda acc, x: acc + 1`

### Concurrency Mode Priority

Test your implementation in this order:
1. async
2. threading
3. multiprocessing

Your primary mode for grading will be: **async**

### Thread Safety Test Parameters

| Parameter | Your Value |
|-----------|------------|
| Number of Threads | 7 |
| Items per Thread | 137 |
| Expected Total | 959 |

---

## Overview

Build a concurrent data processing pipeline integrating multiple paradigms:
- **Functional:** Transformations (map, filter, reduce)
- **OOP:** Design patterns (Strategy, Observer)
- **Concurrent:** Threading, multiprocessing, async

## Architecture

```
Source -> Pipeline Stages -> Worker Pool -> Sink
(generators)  (functional)   (concurrent)  (aggregation)
```

## Implementation Requirements

### 1. Data Sources (`src/pipeline/sources.py`)

Complete the following classes:

```python
class LimitedSource(DataSource[T]):
    def __iter__(self) -> Iterator[T]:
        # Yield up to self._limit items from self._source
        pass

class FileSource(DataSource[str]):
    def __iter__(self) -> Iterator[str]:
        # Read and yield lines from self._path
        pass

class GeneratorSource(DataSource[T]):
    def __iter__(self) -> Iterator[T]:
        # Yield items from self._gen_func()
        pass
```

### 2. Pipeline Stages (`src/pipeline/stages.py`)

Implement functional transformation stages:
- `map(func)` - Apply function to each item
- `filter(predicate)` - Keep items matching predicate
- `flatmap(func)` - Map and flatten results

### 3. Worker Pool (`src/pipeline/workers.py`)

Implement concurrent processing with **4** thread workers:

```python
class WorkerPool(Generic[T, U]):
    def _process_threaded(self, items: Iterator[T]) -> Iterator[U]:
        # Use ThreadPoolExecutor with self._workers threads
        pass

    def _process_multiprocess(self, items: Iterator[T]) -> Iterator[U]:
        # Use ProcessPoolExecutor with self._workers processes
        pass

    def _process_async(self, items: Iterator[T]) -> Iterator[U]:
        # Use asyncio with self._workers concurrent tasks
        pass
```

### 4. Thread-Safe Sinks (`src/pipeline/sinks.py`)

Implement thread-safe data collection:

```python
class CollectorSink(DataSink[T]):
    def consume(self, item: T) -> None:
        # Thread-safe append using self._lock
        pass

class ReducerSink(DataSink[T], Generic[T, U]):
    def consume(self, item: T) -> None:
        # Thread-safe reduce using self._lock
        pass
```

**Your reducer must implement:** count (Count items)

### 5. Pipeline (`src/pipeline/pipeline.py`)

Create a fluent API for pipeline composition:

```python
result = (Pipeline(FileSource("data.txt"))
    .transform(PipelineStage.map(str.upper))
    .transform(PipelineStage.filter(lambda x: len(x) > 10))
    .parallel(process_item, mode=ConcurrencyMode.THREADING, workers=4)
    .run(CollectorSink()))
```

---

## Milestones

| Milestone | Deliverables | Weight |
|-----------|--------------|--------|
| M1 | Core classes (Source, Stage, Sink) | 25% |
| M2 | WorkerPool with all 3 modes | 30% |
| M3 | Integration + thread safety | 30% |
| Final | Documentation + optimization | 15% |

---

## Testing Your Implementation

### Run All Tests
```bash
pytest tests/visible/ -v
```

### Test Thread Safety
Your implementation will be tested with **7** threads, each adding **137** items. The final count must be exactly **959**.

### Test Your Specific Transformations
```python
# Your required transforms
# Remove whitespace
transform_strip = str.strip
# Title case
transform_title = str.title

# Your required filter
filter_func = lambda x: x.lower().startswith('a')

# Your required reducer
reducer_func = lambda acc, x: acc + 1
initial_value = 0
```

---

## Submission Checklist

- [ ] All source files in `src/pipeline/` are complete
- [ ] Thread-safe sinks pass with 7 threads
- [ ] Worker pool works with 4 thread workers
- [ ] All visible tests pass
- [ ] Code is documented with docstrings

---

## Academic Integrity

This assignment has unique parameters generated specifically for you (Student ID: pipeline). Sharing solutions will result in both parties receiving a zero.

**Variant Hash:** `23bf0d244a4cb62c`

This hash is used to verify the authenticity of your submission.
