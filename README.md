# Project 5: Concurrent Data Pipeline

**CSC3301 Programming Language Paradigms**  
**Weight:** 5.5% | **Capstone Project**

## Overview
Build a concurrent data processing pipeline integrating multiple paradigms:
- **Functional:** Transformations (map, filter, reduce)
- **OOP:** Design patterns (Strategy, Observer)
- **Concurrent:** Threading, multiprocessing, async

## Architecture
```
Source → Pipeline Stages → Worker Pool → Sink
(generators)  (functional)   (concurrent)  (aggregation)
```

## Requirements
1. `DataSource` base class with File, Generator, API implementations
2. `PipelineStage` for functional transformations (map, filter, flatmap)
3. `WorkerPool` supporting threading, multiprocessing, AND async
4. Thread-safe `DataSink` for aggregation
5. Fluent API for pipeline composition
6. Progress reporting via Observer pattern

## Milestones
| M1 | Core classes (Source, Stage, Sink) | 25% |
| M2 | WorkerPool with all 3 modes | 30% |
| M3 | Integration + benchmarks | 30% |
| Final | Documentation + optimization | 15% |

## Example Usage
```python
result = (Pipeline(FileSource("data.txt"))
    .transform(PipelineStage.map(str.upper))
    .transform(PipelineStage.filter(lambda x: len(x) > 10))
    .parallel(process_item, mode=ConcurrencyMode.THREADING, workers=4)
    .run(CollectorSink()))
```
