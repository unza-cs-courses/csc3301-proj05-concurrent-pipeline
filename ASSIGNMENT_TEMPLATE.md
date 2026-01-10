# Project 5: Concurrent Data Pipeline

**CSC3301 Programming Language Paradigms**
**Student ID:** {{STUDENT_ID}}
**Variant Hash:** {{VARIANT_HASH}}
**Weight:** 5.5% | **Capstone Project**

---

## Your Unique Assignment Parameters

This assignment has been personalized for you. Your implementation must meet these specific requirements:

### Worker Pool Configuration

| Parameter | Your Value |
|-----------|------------|
| Thread Workers | {{THREAD_WORKERS}} |
| Process Workers | {{PROCESS_WORKERS}} |
| Async Workers | {{ASYNC_WORKERS}} |
| Batch Size | {{BATCH_SIZE}} |

### Required Transformations

Your pipeline must implement these transformation stages:

{{REQUIRED_TRANSFORMS}}

### Required Filter

Your pipeline must filter data using:

- **{{FILTER_NAME}}**: {{FILTER_DESCRIPTION}}
- Implementation: `{{FILTER_FUNC}}`

### Required Reducer

Your sink must implement this reducer operation:

- **{{REDUCER_NAME}}**: {{REDUCER_DESCRIPTION}}
- Initial value: `{{REDUCER_INITIAL}}`
- Implementation: `{{REDUCER_FUNC}}`

### Concurrency Mode Priority

Test your implementation in this order:
1. {{MODE_1}}
2. {{MODE_2}}
3. {{MODE_3}}

Your primary mode for grading will be: **{{MODE_1}}**

### Thread Safety Test Parameters

| Parameter | Your Value |
|-----------|------------|
| Number of Threads | {{NUM_THREADS}} |
| Items per Thread | {{ITEMS_PER_THREAD}} |
| Expected Total | {{EXPECTED_TOTAL}} |

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

Implement concurrent processing with **{{THREAD_WORKERS}}** thread workers:

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

**Your reducer must implement:** {{REDUCER_NAME}} ({{REDUCER_DESCRIPTION}})

### 5. Pipeline (`src/pipeline/pipeline.py`)

Create a fluent API for pipeline composition:

```python
result = (Pipeline(FileSource("data.txt"))
    .transform(PipelineStage.map(str.upper))
    .transform(PipelineStage.filter(lambda x: len(x) > 10))
    .parallel(process_item, mode=ConcurrencyMode.THREADING, workers={{THREAD_WORKERS}})
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
Your implementation will be tested with **{{NUM_THREADS}}** threads, each adding **{{ITEMS_PER_THREAD}}** items. The final count must be exactly **{{EXPECTED_TOTAL}}**.

### Test Your Specific Transformations
```python
# Your required transforms
{{REQUIRED_TRANSFORMS_CODE}}

# Your required filter
filter_func = {{FILTER_FUNC}}

# Your required reducer
reducer_func = {{REDUCER_FUNC}}
initial_value = {{REDUCER_INITIAL}}
```

---

## Submission Checklist

- [ ] All source files in `src/pipeline/` are complete
- [ ] Thread-safe sinks pass with {{NUM_THREADS}} threads
- [ ] Worker pool works with {{THREAD_WORKERS}} thread workers
- [ ] All visible tests pass
- [ ] Code is documented with docstrings

---

## Academic Integrity

This assignment has unique parameters generated specifically for you (Student ID: {{STUDENT_ID}}). Sharing solutions will result in both parties receiving a zero.

**Variant Hash:** `{{VARIANT_HASH}}`

This hash is used to verify the authenticity of your submission.
