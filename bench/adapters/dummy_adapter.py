from typing import Optional
from bench.adapters.base import MemoryAdapter

class DummyAdapter(MemoryAdapter):
    def __init__(self):
        self.history = []

    def reset(self):
        self.history = []

    def ingest_message(self, role: str, content: str, metadata: Optional[dict] = None):
        self.history.append({"role": role, "content": content})

    def answer(self, question: str) -> str:
        # Dummy logic: simulate processing
        import time
        time.sleep(0.01)
        # Just return a hardcoded answer for testing the pipeline
        return "Not mentioned."
