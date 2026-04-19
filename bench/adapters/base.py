from abc import ABC, abstractmethod
from typing import Optional

class MemoryAdapter(ABC):
    @abstractmethod
    def reset(self):
        """Reset the memory state representing a fresh conversation or session."""
        pass

    @abstractmethod
    def ingest_message(self, role: str, content: str, metadata: Optional[dict] = None):
        """Ingest a single message into memory.
        
        Args:
            role: Usually 'user' or 'assistant'.
            content: The text content of the message.
            metadata: Any additional context (e.g., timestamp, turn ID).
        """
        pass

    @abstractmethod
    def answer(self, question: str) -> str:
        """Answer a question based on ingested memory."""
        pass
