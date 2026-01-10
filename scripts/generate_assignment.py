#!/usr/bin/env python3
"""
Generate personalized ASSIGNMENT.md from template.
CSC3301 Concurrent Pipeline Project
"""
import json
from pathlib import Path


def format_transforms(transforms: list[dict]) -> str:
    """Format transformation list for markdown display."""
    lines = []
    for i, t in enumerate(transforms, 1):
        lines.append(f"{i}. **{t['name']}**: {t['description']}")
        lines.append(f"   - Implementation: `{t['func']}`")
    return "\n".join(lines)


def format_transforms_code(transforms: list[dict]) -> str:
    """Format transformation list as Python code."""
    lines = []
    for t in transforms:
        lines.append(f"# {t['description']}")
        lines.append(f"transform_{t['name']} = {t['func']}")
    return "\n".join(lines)


def main():
    repo_root = Path(__file__).parent.parent

    # Load variant config
    config_path = repo_root / ".variant_config.json"
    if not config_path.exists():
        print("No variant config found. Run variant_generator.py first.")
        return

    with open(config_path) as f:
        variant = json.load(f)

    # Load template
    template_path = repo_root / "ASSIGNMENT_TEMPLATE.md"
    if not template_path.exists():
        print("No assignment template found.")
        return

    template = template_path.read_text()

    # Extract values from variant config
    worker_pool = variant["worker_pool"]
    processing = variant["processing"]
    sink = variant["sink"]
    thread_safety = variant["thread_safety"]

    # Replace placeholders
    assignment = template

    # Student info
    assignment = assignment.replace("{{STUDENT_ID}}", variant["student_id"])
    assignment = assignment.replace("{{VARIANT_HASH}}", variant["variant_hash"])

    # Worker pool
    assignment = assignment.replace("{{THREAD_WORKERS}}", str(worker_pool["thread_workers"]))
    assignment = assignment.replace("{{PROCESS_WORKERS}}", str(worker_pool["process_workers"]))
    assignment = assignment.replace("{{ASYNC_WORKERS}}", str(worker_pool["async_workers"]))
    assignment = assignment.replace("{{BATCH_SIZE}}", str(worker_pool["batch_size"]))

    # Transforms
    transforms = processing["required_transforms"]
    assignment = assignment.replace("{{REQUIRED_TRANSFORMS}}", format_transforms(transforms))
    assignment = assignment.replace("{{REQUIRED_TRANSFORMS_CODE}}", format_transforms_code(transforms))

    # Filter
    filter_config = processing["required_filter"]
    assignment = assignment.replace("{{FILTER_NAME}}", filter_config["name"])
    assignment = assignment.replace("{{FILTER_DESCRIPTION}}", filter_config["description"])
    assignment = assignment.replace("{{FILTER_FUNC}}", filter_config["func"])

    # Reducer
    reducer_config = sink["required_reducer"]
    assignment = assignment.replace("{{REDUCER_NAME}}", reducer_config["name"])
    assignment = assignment.replace("{{REDUCER_DESCRIPTION}}", reducer_config["description"])
    assignment = assignment.replace("{{REDUCER_INITIAL}}", str(reducer_config["initial"]))
    assignment = assignment.replace("{{REDUCER_FUNC}}", reducer_config["func"])

    # Mode priority
    modes = processing["mode_priority"]
    assignment = assignment.replace("{{MODE_1}}", modes[0])
    assignment = assignment.replace("{{MODE_2}}", modes[1])
    assignment = assignment.replace("{{MODE_3}}", modes[2])

    # Thread safety
    assignment = assignment.replace("{{NUM_THREADS}}", str(thread_safety["num_threads"]))
    assignment = assignment.replace("{{ITEMS_PER_THREAD}}", str(thread_safety["items_per_thread"]))
    assignment = assignment.replace("{{EXPECTED_TOTAL}}", str(thread_safety["expected_total"]))

    # Write personalized assignment
    output_path = repo_root / "ASSIGNMENT.md"
    output_path.write_text(assignment)
    print(f"Generated personalized assignment: {output_path}")
    print(f"Student ID: {variant['student_id']}")
    print(f"Variant Hash: {variant['variant_hash']}")


if __name__ == "__main__":
    main()
