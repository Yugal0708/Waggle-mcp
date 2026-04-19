import tempfile
from pathlib import Path
from typing import Optional
from bench.adapters.base import MemoryAdapter
from waggle.graph import MemoryGraph
from waggle.embeddings import EmbeddingModel

class WaggleAdapter(MemoryAdapter):
    def __init__(self, embedding_model: str = "deterministic"):
        """Initialize the Waggle graph memory adapter."""
        # Using deterministic for fast local testing. Use 'all-MiniLM-L6-v2' for real runs.
        self.embedding_model = EmbeddingModel(embedding_model)
        self.tmp_dir = None
        self.graph = None
        self.reset()
        
    def reset(self):
        """Create a fresh Waggle MemoryGraph in an empty temporary directory."""
        if self.tmp_dir:
            self.tmp_dir.cleanup()
        self.tmp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.tmp_dir.name) / "memory.db"
        self.graph = MemoryGraph(db_path=db_path, embedding_model=self.embedding_model)
        
    def ingest_message(self, role: str, content: str, metadata: Optional[dict] = None):
        """Ingest conversational messages into the graph."""
        if not isinstance(content, str): content = str(content)
        if not isinstance(role, str): role = str(role)

        if role == "user":
            self.graph.observe_conversation(user_message=content, assistant_response="...")
        elif role == "assistant" or role == "agent":
            self.graph.observe_conversation(user_message="...", assistant_response=content)
        else:
            self.graph.observe_conversation(user_message=content, assistant_response="...")

    def answer(self, question: str) -> str:
        """
        Waggle returns a bundle of graph nodes rather than generatively answering.
        For benchmarking match scores, we serialize the retrieved evidence into a string format.
        """
        query_res = self.graph.query(query=question, max_nodes=5, retrieval_mode="graph")
        return " ".join([node.content for node in query_res.nodes])
        
    def __del__(self):
        if self.tmp_dir:
            self.tmp_dir.cleanup()
