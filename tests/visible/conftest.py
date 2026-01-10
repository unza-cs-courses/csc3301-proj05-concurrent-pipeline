"""
Pytest fixtures for CSC3301 Concurrent Pipeline Project.

Loads variant configuration and provides sensible defaults for testing.
"""
import json
import pytest
from pathlib import Path
from typing import Any


def load_variant_config() -> dict[str, Any]:
    """
    Load variant configuration from .variant_config.json.

    Returns default configuration if file doesn't exist (for local development).
    """
    repo_root = Path(__file__).parent.parent.parent
    config_path = repo_root / ".variant_config.json"

    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)

    # Default configuration for local development/testing
    return {
        "student_id": "default_student",
        "variant_hash": "0000000000000000",
        "worker_pool": {
            "thread_workers": 4,
            "process_workers": 2,
            "async_workers": 8,
            "batch_size": 50,
        },
        "processing": {
            "min_items": 100,
            "required_transforms": [
                {"name": "uppercase", "func": "str.upper", "description": "Convert to uppercase"},
                {"name": "strip", "func": "str.strip", "description": "Remove whitespace"},
            ],
            "required_filter": {
                "name": "length_gt_5",
                "func": "lambda x: len(x) > 5",
                "description": "Length > 5"
            },
            "mode_priority": ["threading", "multiprocessing", "async"],
        },
        "sink": {
            "required_reducer": {
                "name": "sum_lengths",
                "initial": 0,
                "func": "lambda acc, x: acc + len(x)",
                "description": "Sum of lengths"
            },
        },
        "thread_safety": {
            "num_threads": 10,
            "items_per_thread": 100,
            "expected_total": 1000,
        },
        "source_tests": {
            "file_lines": 30,
            "generator_items": 50,
        },
        "pipeline_test": {
            "input_size": 200,
            "expected_concurrency_mode": "threading",
            "timeout_seconds": 15,
        },
    }


@pytest.fixture(scope="session")
def variant_config() -> dict[str, Any]:
    """Provide the full variant configuration."""
    return load_variant_config()


@pytest.fixture(scope="session")
def student_id(variant_config) -> str:
    """Provide the student ID."""
    return variant_config["student_id"]


@pytest.fixture(scope="session")
def variant_hash(variant_config) -> str:
    """Provide the variant hash for identification."""
    return variant_config["variant_hash"]


# Worker Pool Fixtures

@pytest.fixture(scope="session")
def thread_workers(variant_config) -> int:
    """Number of thread workers for testing."""
    return variant_config["worker_pool"]["thread_workers"]


@pytest.fixture(scope="session")
def process_workers(variant_config) -> int:
    """Number of process workers for testing."""
    return variant_config["worker_pool"]["process_workers"]


@pytest.fixture(scope="session")
def async_workers(variant_config) -> int:
    """Number of async workers for testing."""
    return variant_config["worker_pool"]["async_workers"]


@pytest.fixture(scope="session")
def batch_size(variant_config) -> int:
    """Batch size for processing."""
    return variant_config["worker_pool"]["batch_size"]


# Processing Fixtures

@pytest.fixture(scope="session")
def min_items(variant_config) -> int:
    """Minimum items to process in tests."""
    return variant_config["processing"]["min_items"]


@pytest.fixture(scope="session")
def required_transforms(variant_config) -> list[dict]:
    """Required transformation functions."""
    return variant_config["processing"]["required_transforms"]


@pytest.fixture(scope="session")
def required_filter(variant_config) -> dict:
    """Required filter condition."""
    return variant_config["processing"]["required_filter"]


@pytest.fixture(scope="session")
def mode_priority(variant_config) -> list[str]:
    """Priority order of concurrency modes."""
    return variant_config["processing"]["mode_priority"]


@pytest.fixture(scope="session")
def primary_mode(mode_priority) -> str:
    """Primary concurrency mode to test."""
    return mode_priority[0]


# Sink Fixtures

@pytest.fixture(scope="session")
def required_reducer(variant_config) -> dict:
    """Required reducer operation."""
    return variant_config["sink"]["required_reducer"]


# Thread Safety Fixtures

@pytest.fixture(scope="session")
def num_threads(variant_config) -> int:
    """Number of threads for thread safety tests."""
    return variant_config["thread_safety"]["num_threads"]


@pytest.fixture(scope="session")
def items_per_thread(variant_config) -> int:
    """Items per thread in thread safety tests."""
    return variant_config["thread_safety"]["items_per_thread"]


@pytest.fixture(scope="session")
def expected_total(variant_config) -> int:
    """Expected total items after thread safety test."""
    return variant_config["thread_safety"]["expected_total"]


# Source Test Fixtures

@pytest.fixture(scope="session")
def file_lines(variant_config) -> int:
    """Number of lines for file source tests."""
    return variant_config["source_tests"]["file_lines"]


@pytest.fixture(scope="session")
def generator_items(variant_config) -> int:
    """Number of items for generator source tests."""
    return variant_config["source_tests"]["generator_items"]


# Pipeline Test Fixtures

@pytest.fixture(scope="session")
def pipeline_input_size(variant_config) -> int:
    """Input size for pipeline integration tests."""
    return variant_config["pipeline_test"]["input_size"]


@pytest.fixture(scope="session")
def pipeline_timeout(variant_config) -> int:
    """Timeout in seconds for pipeline tests."""
    return variant_config["pipeline_test"]["timeout_seconds"]


# Helper Fixtures

@pytest.fixture
def sample_data(min_items) -> list[str]:
    """Generate sample string data for testing."""
    return [f"item_{i}" for i in range(min_items)]


@pytest.fixture
def sample_numbers(min_items) -> list[int]:
    """Generate sample numeric data for testing."""
    return list(range(min_items))


@pytest.fixture
def temp_file(tmp_path, file_lines) -> Path:
    """Create a temporary file with test data."""
    file_path = tmp_path / "test_data.txt"
    with open(file_path, 'w') as f:
        for i in range(file_lines):
            f.write(f"Line {i}: Sample data for testing\n")
    return file_path


@pytest.fixture
def eval_transform(required_transforms):
    """Evaluate and return transform functions."""
    transforms = []
    for t in required_transforms:
        func_str = t["func"]
        if func_str.startswith("lambda"):
            transforms.append(eval(func_str))
        else:
            # Handle built-in methods like str.upper
            transforms.append(eval(func_str))
    return transforms


@pytest.fixture
def eval_filter(required_filter):
    """Evaluate and return the filter function."""
    return eval(required_filter["func"])


@pytest.fixture
def eval_reducer(required_reducer):
    """Evaluate and return the reducer function and initial value."""
    func = eval(required_reducer["func"])
    initial = eval(str(required_reducer["initial"]))
    return func, initial
