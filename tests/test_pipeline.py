import pytest
import threading
from src.pipeline.sinks import CollectorSink

class TestThreadSafety:
    def test_collector_thread_safe(self):
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
