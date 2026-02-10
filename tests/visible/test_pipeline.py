"""
Visible Tests for Project 5: Concurrent Data Pipeline
CSC3301 Programming Language Paradigms

Tests cover: Pipeline, stages, sources, sinks, and worker pool basics.
Students should be able to pass these tests with a correct implementation.
"""
import pytest
import threading
import time
from typing import Iterator


# ── Stage Tests ──────────────────────────────────────────────


class TestMapStage:
    """Tests for MapStage."""

    def test_map_stage_applies_function(self):
        """MapStage.process should apply the stored function."""
        from src.pipeline.stages import MapStage

        stage = MapStage(lambda x: x * 2)
        assert stage.process(5) == 10

    def test_map_stage_with_strings(self):
        """MapStage should work with string transformations."""
        from src.pipeline.stages import MapStage

        stage = MapStage(str.upper)
        assert stage.process("hello") == "HELLO"

    def test_map_stage_with_type_conversion(self):
        """MapStage should handle type conversions."""
        from src.pipeline.stages import MapStage

        stage = MapStage(str)
        assert stage.process(42) == "42"


class TestFilterStage:
    """Tests for FilterStage."""

    def test_filter_stage_passes_matching(self):
        """FilterStage should return item when predicate is True."""
        from src.pipeline.stages import FilterStage

        stage = FilterStage(lambda x: x > 3)
        result = stage.process(5)
        assert result == 5 or result is True  # Accept item or True

    def test_filter_stage_rejects_non_matching(self):
        """FilterStage should return None when predicate is False."""
        from src.pipeline.stages import FilterStage

        stage = FilterStage(lambda x: x > 3)
        result = stage.process(1)
        assert result is None

    def test_filter_with_string_predicate(self):
        """FilterStage should work with string predicates."""
        from src.pipeline.stages import FilterStage

        stage = FilterStage(lambda s: len(s) > 3)
        assert stage.process("hello") == "hello"
        assert stage.process("hi") is None


class TestFlatMapStage:
    """Tests for FlatMapStage."""

    def test_flatmap_splits_string(self):
        """FlatMapStage should expand one item into many."""
        from src.pipeline.stages import FlatMapStage

        stage = FlatMapStage(lambda s: s.split())
        result = stage.process("hello world")
        assert result == ["hello", "world"]

    def test_flatmap_returns_list(self):
        """FlatMapStage result should be a list."""
        from src.pipeline.stages import FlatMapStage

        stage = FlatMapStage(lambda x: [x, x])
        result = stage.process(1)
        assert isinstance(result, list)
        assert result == [1, 1]


# ── Pipeline Tests ───────────────────────────────────────────


class TestPipeline:
    """Tests for the Pipeline class."""

    def test_pipeline_single_stage(self):
        """Pipeline with one stage should transform items."""
        from src.pipeline.pipeline import Pipeline
        from src.pipeline.stages import MapStage

        pipeline = Pipeline(stages=[MapStage(lambda x: x * 2)])
        assert pipeline.process(5) == 10

    def test_pipeline_multiple_stages(self):
        """Pipeline should chain multiple stages."""
        from src.pipeline.pipeline import Pipeline
        from src.pipeline.stages import MapStage

        pipeline = Pipeline(stages=[
            MapStage(lambda x: x + 1),
            MapStage(lambda x: x * 2),
        ])
        # (5 + 1) * 2 = 12
        assert pipeline.process(5) == 12

    def test_pipeline_stages_property(self):
        """Pipeline.stages should return the list of stages."""
        from src.pipeline.pipeline import Pipeline
        from src.pipeline.stages import MapStage

        stages = [MapStage(lambda x: x)]
        pipeline = Pipeline(stages=stages)
        assert pipeline.stages is not None
        assert len(pipeline.stages) == 1


class TestComposedStages:
    """Tests for compose_stages helper."""

    def test_compose_two_stages(self):
        """compose_stages should chain stage processing."""
        from src.pipeline.pipeline import compose_stages
        from src.pipeline.stages import MapStage

        transform = compose_stages(
            MapStage(lambda x: x + 1),
            MapStage(lambda x: x * 3),
        )
        # (2 + 1) * 3 = 9
        assert transform(2) == 9

    def test_compose_returns_callable(self):
        """compose_stages should return a callable."""
        from src.pipeline.pipeline import compose_stages
        from src.pipeline.stages import MapStage

        result = compose_stages(MapStage(lambda x: x))
        assert callable(result)


# ── Source Tests ─────────────────────────────────────────────


class TestSources:
    """Tests for data sources."""

    def test_generator_source_iterates(self):
        """GeneratorSource should yield items from generator function."""
        from src.pipeline.sources import GeneratorSource

        source = GeneratorSource(lambda: iter([1, 2, 3]))
        items = list(source)
        assert items == [1, 2, 3]

    def test_limited_source_takes_n(self):
        """LimitedSource should limit iteration to n items."""
        from src.pipeline.sources import GeneratorSource

        source = GeneratorSource(lambda: iter(range(100)))
        limited = source.take(5)
        items = list(limited)
        assert len(items) == 5
        assert items == [0, 1, 2, 3, 4]


# ── Sink Tests ───────────────────────────────────────────────


class TestCollectorSink:
    """Tests for CollectorSink."""

    def test_collector_collects_items(self):
        """CollectorSink should collect consumed items."""
        from src.pipeline.sinks import CollectorSink

        sink = CollectorSink()
        sink.consume("a")
        sink.consume("b")
        sink.consume("c")
        result = sink.finalize()
        assert len(result) == 3
        assert set(result) == {"a", "b", "c"}

    def test_collector_finalize_returns_copy(self):
        """Finalize should return a copy, not the internal list."""
        from src.pipeline.sinks import CollectorSink

        sink = CollectorSink()
        sink.consume(1)
        r1 = sink.finalize()
        r1.append(999)
        r2 = sink.finalize()
        assert 999 not in r2


class TestReducerSink:
    """Tests for ReducerSink."""

    def test_reducer_sums(self):
        """ReducerSink should accumulate values with reducer function."""
        from src.pipeline.sinks import ReducerSink

        sink = ReducerSink(lambda acc, x: acc + x, 0)
        for i in [1, 2, 3, 4, 5]:
            sink.consume(i)
        assert sink.finalize() == 15

    def test_reducer_concatenates_strings(self):
        """ReducerSink should work with string accumulation."""
        from src.pipeline.sinks import ReducerSink

        sink = ReducerSink(lambda acc, x: acc + x, "")
        for c in ["h", "e", "l", "l", "o"]:
            sink.consume(c)
        assert sink.finalize() == "hello"


# ── Thread Safety Tests ──────────────────────────────────────


class TestThreadSafety:
    """Thread safety tests for sinks."""

    def test_collector_thread_safe(self):
        """CollectorSink must be thread-safe under concurrent writes."""
        from src.pipeline.sinks import CollectorSink

        sink = CollectorSink()
        threads = []

        def worker(n):
            for i in range(100):
                sink.consume(f"{n}-{i}")

        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        result = sink.finalize()
        assert len(result) == 1000

    def test_reducer_thread_safe(self):
        """ReducerSink must be thread-safe under concurrent writes."""
        from src.pipeline.sinks import ReducerSink

        sink = ReducerSink(lambda acc, x: acc + x, 0)
        threads = []

        def worker():
            for _ in range(100):
                sink.consume(1)

        for _ in range(10):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert sink.finalize() == 1000
