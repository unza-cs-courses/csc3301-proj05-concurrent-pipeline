#!/usr/bin/env python3
"""
Generate unique assignment variants for CSC3301 Concurrent Pipeline Project.

Uses student ID hash for deterministic, reproducible variant generation.
Each student gets unique:
- Worker pool sizes
- Batch sizes
- Data transformation requirements
- Test parameters
"""
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def generate_variant(student_id: str) -> dict[str, Any]:
    """
    Generate a deterministic variant configuration based on student ID.

    Uses SHA-256 hash of student ID to generate reproducible random values.
    """
    # Create deterministic hash from student ID
    hash_bytes = hashlib.sha256(student_id.encode()).digest()

    # Use different portions of the hash for different parameters
    def get_int(offset: int, min_val: int, max_val: int) -> int:
        """Extract an integer from hash bytes within a range."""
        value = int.from_bytes(hash_bytes[offset:offset+2], 'big')
        return min_val + (value % (max_val - min_val + 1))

    def get_choice(offset: int, choices: list) -> Any:
        """Select from a list of choices based on hash bytes."""
        idx = hash_bytes[offset] % len(choices)
        return choices[idx]

    # Worker Pool Configuration
    # Number of workers for each concurrency mode
    thread_workers = get_int(0, 2, 8)
    process_workers = get_int(2, 2, 4)  # Keep lower for processes
    async_workers = get_int(4, 4, 16)

    # Batch sizes for processing
    batch_size = get_int(6, 10, 100)

    # Minimum items to process in tests
    min_items = get_int(8, 50, 200)

    # Data transformation requirements
    transformations = [
        {"name": "uppercase", "func": "str.upper", "description": "Convert to uppercase"},
        {"name": "lowercase", "func": "str.lower", "description": "Convert to lowercase"},
        {"name": "strip", "func": "str.strip", "description": "Remove whitespace"},
        {"name": "title", "func": "str.title", "description": "Title case"},
        {"name": "reverse", "func": "lambda x: x[::-1]", "description": "Reverse string"},
    ]

    # Select required transformations (2-3)
    num_transforms = get_int(10, 2, 3)
    transform_indices = []
    for i in range(num_transforms):
        idx = get_int(12 + i * 2, 0, len(transformations) - 1)
        if idx not in transform_indices:
            transform_indices.append(idx)
    required_transforms = [transformations[i] for i in transform_indices]

    # Filter conditions
    filter_conditions = [
        {"name": "length_gt_5", "func": "lambda x: len(x) > 5", "description": "Length > 5"},
        {"name": "length_gt_10", "func": "lambda x: len(x) > 10", "description": "Length > 10"},
        {"name": "starts_with_a", "func": "lambda x: x.lower().startswith('a')", "description": "Starts with 'a'"},
        {"name": "contains_e", "func": "lambda x: 'e' in x.lower()", "description": "Contains 'e'"},
        {"name": "is_alpha", "func": "lambda x: x.isalpha()", "description": "Only letters"},
        {"name": "no_spaces", "func": "lambda x: ' ' not in x", "description": "No spaces"},
    ]
    filter_idx = get_int(18, 0, len(filter_conditions) - 1)
    required_filter = filter_conditions[filter_idx]

    # Concurrency mode priority for testing
    mode_priority = get_choice(20, [
        ["threading", "multiprocessing", "async"],
        ["threading", "async", "multiprocessing"],
        ["async", "threading", "multiprocessing"],
        ["multiprocessing", "threading", "async"],
    ])

    # Reducer test configuration
    reducer_operations = [
        {"name": "sum_lengths", "initial": 0, "func": "lambda acc, x: acc + len(x)", "description": "Sum of lengths"},
        {"name": "max_length", "initial": 0, "func": "lambda acc, x: max(acc, len(x))", "description": "Maximum length"},
        {"name": "count", "initial": 0, "func": "lambda acc, x: acc + 1", "description": "Count items"},
        {"name": "concat", "initial": "''", "func": "lambda acc, x: acc + x[:1]", "description": "Concatenate first chars"},
    ]
    reducer_idx = get_int(22, 0, len(reducer_operations) - 1)
    required_reducer = reducer_operations[reducer_idx]

    # Thread safety test parameters
    num_threads = get_int(24, 5, 15)
    items_per_thread = get_int(26, 50, 150)
    expected_total = num_threads * items_per_thread

    # Source test configuration
    source_lines = get_int(28, 20, 50)
    generator_items = get_int(30, 30, 80)

    return {
        "student_id": student_id,
        "variant_hash": hashlib.sha256(student_id.encode()).hexdigest()[:16],

        # Worker pool configuration
        "worker_pool": {
            "thread_workers": thread_workers,
            "process_workers": process_workers,
            "async_workers": async_workers,
            "batch_size": batch_size,
        },

        # Processing requirements
        "processing": {
            "min_items": min_items,
            "required_transforms": required_transforms,
            "required_filter": required_filter,
            "mode_priority": mode_priority,
        },

        # Sink configuration
        "sink": {
            "required_reducer": required_reducer,
        },

        # Thread safety tests
        "thread_safety": {
            "num_threads": num_threads,
            "items_per_thread": items_per_thread,
            "expected_total": expected_total,
        },

        # Source tests
        "source_tests": {
            "file_lines": source_lines,
            "generator_items": generator_items,
        },

        # Pipeline integration test
        "pipeline_test": {
            "input_size": get_int(31, 100, 500),
            "expected_concurrency_mode": mode_priority[0],
            "timeout_seconds": get_int(29, 10, 30),
        },
    }


def main():
    """Generate variant configuration file."""
    if len(sys.argv) < 2:
        print("Usage: python variant_generator.py <student_id>")
        sys.exit(1)

    student_id = sys.argv[1]

    # Generate variant
    variant = generate_variant(student_id)

    # Write configuration
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / ".variant_config.json"

    with open(config_path, 'w') as f:
        json.dump(variant, f, indent=2)

    print(f"Generated variant for student: {student_id}")
    print(f"Variant hash: {variant['variant_hash']}")
    print(f"Worker pool: {variant['worker_pool']['thread_workers']} threads, "
          f"{variant['worker_pool']['process_workers']} processes, "
          f"{variant['worker_pool']['async_workers']} async")
    print(f"Batch size: {variant['worker_pool']['batch_size']}")
    print(f"Priority mode: {variant['processing']['mode_priority'][0]}")
    print(f"Thread safety test: {variant['thread_safety']['num_threads']} threads x "
          f"{variant['thread_safety']['items_per_thread']} items = "
          f"{variant['thread_safety']['expected_total']} total")
    print(f"Configuration saved to: {config_path}")


if __name__ == "__main__":
    main()
