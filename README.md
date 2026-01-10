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
Source -> Pipeline Stages -> Worker Pool -> Sink
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

| Milestone | Deliverables | Weight |
|-----------|--------------|--------|
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

---

## Variant System

This assignment uses a variant-based system to generate unique parameters for each student. The system ensures academic integrity while providing consistent, reproducible test configurations.

### How It Works

1. **Variant Generation**: When a student repository is created via GitHub Classroom, the `generate-variant.yml` workflow automatically:
   - Extracts the student ID from the repository name
   - Generates a deterministic variant using SHA-256 hashing
   - Creates `.variant_config.json` with unique parameters
   - Generates a personalized `ASSIGNMENT.md`

2. **Unique Parameters**: Each student receives different:
   - Worker pool sizes (threads, processes, async workers)
   - Batch sizes for processing
   - Required transformation functions
   - Filter conditions
   - Reducer operations
   - Thread safety test parameters

3. **Testing**: The `conftest.py` fixtures automatically load variant configuration, with sensible defaults for local development.

### Variant Configuration Structure

```json
{
  "student_id": "username",
  "variant_hash": "abc123...",
  "worker_pool": {
    "thread_workers": 4,
    "process_workers": 2,
    "async_workers": 8,
    "batch_size": 50
  },
  "processing": {
    "min_items": 100,
    "required_transforms": [...],
    "required_filter": {...},
    "mode_priority": ["threading", "multiprocessing", "async"]
  },
  "sink": {
    "required_reducer": {...}
  },
  "thread_safety": {
    "num_threads": 10,
    "items_per_thread": 100,
    "expected_total": 1000
  }
}
```

### For Instructors

#### Manual Variant Generation

```bash
# Generate variant for a specific student
python scripts/variant_generator.py student123

# Generate personalized assignment
python scripts/generate_assignment.py
```

#### Customizing Variants

Edit `scripts/variant_generator.py` to modify:
- Range of worker pool sizes
- Available transformation functions
- Filter conditions
- Reducer operations
- Thread safety parameters

### For Students

Your personalized assignment is in `ASSIGNMENT.md`. It contains your specific:
- Worker pool configuration
- Required transformations
- Thread safety test parameters

The tests will automatically use your variant configuration.

### Running Tests

```bash
# Run all visible tests
pytest tests/visible/ -v

# Run with variant info
pytest tests/visible/ -v --tb=short
```

### Default Configuration

If no `.variant_config.json` exists (e.g., during local development), the tests use sensible defaults:
- 4 thread workers
- 2 process workers
- 8 async workers
- 10 threads x 100 items for thread safety tests

---

## Project Structure

```
csc3301-proj05-concurrent-pipeline/
├── .github/
│   └── workflows/
│       ├── autograding.yml      # Test runner
│       └── generate-variant.yml # Variant generator
├── scripts/
│   ├── variant_generator.py     # Generate unique variants
│   └── generate_assignment.py   # Create personalized ASSIGNMENT.md
├── src/
│   └── pipeline/
│       ├── __init__.py
│       ├── sources.py           # Data sources (YOUR CODE)
│       ├── stages.py            # Pipeline stages (YOUR CODE)
│       ├── workers.py           # Worker pool (YOUR CODE)
│       ├── sinks.py             # Data sinks (YOUR CODE)
│       └── pipeline.py          # Pipeline orchestration (YOUR CODE)
├── tests/
│   └── visible/
│       ├── conftest.py          # Variant-aware fixtures
│       └── test_pipeline.py     # Visible tests
├── ASSIGNMENT_TEMPLATE.md       # Template for personalized assignments
├── ASSIGNMENT.md                # Your personalized assignment (generated)
├── .variant_config.json         # Your variant configuration (generated)
└── README.md
```

---

## Getting Started

1. Clone your assignment repository
2. Check `ASSIGNMENT.md` for your specific requirements
3. Implement the required classes in `src/pipeline/`
4. Run tests with `pytest tests/visible/ -v`
5. Push to trigger autograding
