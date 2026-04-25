from __future__ import annotations

from types import MethodType

from waggle.models import SubgraphResult
from waggle.neo4j_graph import Neo4jMemoryGraph


def make_stub_graph() -> Neo4jMemoryGraph:
    graph = object.__new__(Neo4jMemoryGraph)
    graph.tenant_id = "local-default"
    return graph


def test_neo4j_context_window_stubs_do_not_raise() -> None:
    graph = make_stub_graph()

    repo_id, window_id = graph.resolve_window_context("project", "session")
    window = graph.get_context_window(window_id)
    closed = graph.close_context_window(window_id)

    assert repo_id == "default"
    assert window.id == "session"
    assert graph.list_context_windows() == []
    assert graph.get_context_window_edges(window_id) == []
    assert graph.get_window_nodes(window_id) == []
    assert graph.compute_window_embedding(window_id) is None
    assert graph.derive_context_window_edges(window_id, repo_id) == []
    assert graph.get_nodes_without_window() == []
    assert graph.assign_nodes_to_window(["node"], window_id) == 0
    assert graph.list_repos() == []
    assert graph.update_window_node_count(window_id) == 0
    assert closed.status == "closed"


def test_neo4j_tiered_query_falls_back_to_flat_query() -> None:
    graph = make_stub_graph()

    def fake_query(self: Neo4jMemoryGraph, **kwargs: object) -> SubgraphResult:
        return SubgraphResult(query=str(kwargs["query"]), retrieval_mode="graph")

    graph.query = MethodType(fake_query, graph)

    result = graph.tiered_query(query="database", project="project")

    assert result.query == "database"
    assert result.retrieval_mode == "flat_fallback"
