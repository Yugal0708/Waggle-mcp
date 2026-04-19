# Memory System Benchmarking Harness

A unified local evaluation harness for conversational memory backends.

## Architecture

This framework is built around the `MemoryAdapter` interface. To test your custom memory MCP or backend, you simply implement a subclass of `MemoryAdapter` in `bench/adapters/`.

```python
from bench.adapters.base import MemoryAdapter

class MyMemoryAdapter(MemoryAdapter):
    def reset(self):
        # Clear local database or API context
        pass
    
    def ingest_message(self, role: str, content: str, metadata: dict = None):
        # Push message into your database/RAG
        pass
        
    def answer(self, question: str) -> str:
        # Query your system
        return "predicted answer"
```

Then wrap the runners to import your adapter instead of the `DummyAdapter`.

## Prerequisites

```bash
pip install -r bench/requirements.txt
```

## Running Benchmarks

**ConvoMem**
```bash
# Run a specific category limit to 50 examples
python -m bench.runners.run_convomem --category user_evidence --limit 50
```

**Run All (Smoke Test)**
```bash
python -m bench.runners.run_all
```

## Outputs
Results are logged to `bench/outputs/`:
- `convomem_results.jsonl`: Per-example deep dives (inputs, predicted answers, gold answers, latency tracking).
- `summary.csv`: Aggregated accuracy metrics and timing overviews.

## Notes & Assumptions
- **Latency Tracking**: Latency is tracked strictly over the `answer()` function. Time spent ingesting text is not counted.
