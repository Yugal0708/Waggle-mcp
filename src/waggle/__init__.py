"""Persistent graph memory MCP server."""

from waggle.graph import MemoryGraph
from waggle.models import (
    ApiKeyCreateResult,
    ApiKeyRecord,
    BackupResult,
    ConflictRecord,
    Edge,
    GraphDiffResult,
    GraphStats,
    ImportResult,
    Node,
    NodeStoreResult,
    NodeType,
    ObservationResult,
    PrimeContextResult,
    RelationType,
    SubgraphResult,
    TenantRecord,
    TopicCluster,
    TopicResult,
)

try:  # pragma: no cover
    from waggle.neo4j_graph import Neo4jMemoryGraph
except Exception:  # pragma: no cover
    Neo4jMemoryGraph = None

__all__ = [
    "Edge",
    "ApiKeyCreateResult",
    "ApiKeyRecord",
    "BackupResult",
    "ConflictRecord",
    "GraphStats",
    "GraphDiffResult",
    "ImportResult",
    "MemoryGraph",
    "Neo4jMemoryGraph",
    "Node",
    "NodeStoreResult",
    "NodeType",
    "ObservationResult",
    "PrimeContextResult",
    "RelationType",
    "SubgraphResult",
    "TenantRecord",
    "TopicCluster",
    "TopicResult",
]

__version__ = "0.1.0"
