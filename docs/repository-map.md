# Repository Map

This guide explains the important files and directories in the public Waggle repository so new contributors can find the right place to work.

## Top-level files

| Path | Purpose |
| --- | --- |
| `README.md` | Product overview, install paths, quick start, and high-level architecture. |
| `CONTRIBUTING.md` | Development setup, test commands, code style, and PR expectations. |
| `SECURITY.md` | Security reporting policy and repo-specific security notes. |
| `pyproject.toml` | Python package metadata, dependencies, CLI entrypoints, and tool config for Ruff and mypy. |
| `smithery.yaml` | Metadata for MCP ecosystem distribution and discovery. |
| `Dockerfile` | Container image build for the packaged Waggle server. |
| `LICENSE` | Apache-2.0 license for the public repo. |

## Main source tree

### `src/waggle/`

This is the product code for the MCP server and memory engine.

| File | Purpose |
| --- | --- |
| `server.py` | Main CLI and MCP tool surface. This is the first file to read if you want to understand what Waggle exposes. |
| `graph.py` | SQLite-backed graph storage and traversal engine. |
| `neo4j_graph.py` | Neo4j-backed graph implementation for deployments that need a remote graph backend. |
| `models.py` | Shared models for nodes, edges, transcripts, and API payloads. |
| `config.py` | Environment-driven application config and startup modes. |
| `embeddings.py` | Local embedding model integration plus deterministic fallback mode. |
| `intelligence.py` | Heuristics for extracting candidate memories, labels, and relationships from conversation text. |
| `recursive_context.py` | Recursive context assembly and token-budgeted context pack generation. |
| `orchestrator.py` | Automatic memory orchestration hooks that build context before an answer and ingest after a turn. |
| `chat_runtime.py` | Runtime wiring for session handling and orchestrated turns. |
| `abhi.py` | Import/export, validation, diff, and merge support for `.abhi` memory snapshots. |
| `serializer.py` | Serialization helpers for graph data and interchange formats. |
| `runtime_context.py` | Scope and runtime metadata helpers used during memory operations. |
| `context_bundle.py` | Context packaging helpers for returning concise memory payloads. |
| `auth.py` | Authentication helpers for hosted or protected setups. |
| `drive_sync.py` | Google Drive sync and token handling for export/import workflows. |
| `graph_ui.py` | Graph Studio serving and UI integration entrypoints. |
| `markdown_vault.py` | Markdown-based export and vault helpers. |
| `backfill.py` | Backfill/import workflows for existing data sources. |
| `evidence.py` | Evidence tracking for why a memory exists and where it came from. |
| `errors.py` | Shared exception types. |
| `locks.py` | File and process locking helpers to protect local state. |
| `logging_utils.py` | Logging setup and formatting helpers. |
| `metrics.py` | Internal counters and performance-oriented metrics helpers. |
| `rate_limit.py` | Safeguards for request pacing or repeated operations. |
| `rlm.py` | Integration layer for the RLM-inspired recursive context behavior. |
| `token_efficiency_benchmark.py` | Benchmark helpers for context-pack size and efficiency analysis. |
| `__init__.py` | Package version and top-level exports. |

### `src/waggle/retrieval/`

Retrieval strategies and ranking logic. Start with `hybrid.py` if you want to work on search quality.

### `src/waggle/hooks/claude_code/`

Hook scripts used by Claude Code integrations. These are the main files to inspect when debugging automatic memory behavior in that client.

### `src/rlm/`

Vendored or adapted Recursive Language Model support code used by Waggle's context assembly pipeline. Treat this subtree carefully and keep changes tightly scoped.

## Tests

| Path | Purpose |
| --- | --- |
| `tests/` | Main Python test suite for graph behavior, orchestration, hooks, packaging, and CLI flows. |
| `tests/fixtures/` | Fixture data for import/export, retrieval, and regression coverage. |

If you are making a focused change, search for the corresponding `tests/test_*.py` file before adding new coverage from scratch.

## Documentation

| Path | Purpose |
| --- | --- |
| `docs/install/` | Client-specific installation guides for Codex, Claude, Cursor, VS Code, and other MCP clients. |
| `docs/security/` | Security model and hardening guidance. |
| `docs/deployment/` | Production and deployment-facing material. |
| `docs/reference.md` | Command, configuration, and behavior reference. |
| `docs/memory-orchestration.md` | How automatic memory is wired through runtime orchestration. |
| `docs/hooks.md` | Hook behavior and integration details. |
| `docs/automatic-memory-rules.md` | The policy text that instructs clients to use automatic memory tools. |

## Packages and integrations

| Path | Purpose |
| --- | --- |
| `packages/vscode-extension/` | VS Code extension that installs and manages Waggle for workspace users. |
| `packages/claude-desktop-extension/` | Claude Desktop extension packaging and bundle metadata. |
| `graph-ui/` | Frontend code for Graph Studio and related UI assets. |
| `templates/waggle-plus/` | Template material for packaged or commercial-facing setups. |

## Scripts and support assets

| Path | Purpose |
| --- | --- |
| `scripts/oolong/` | Evaluation and dataset helpers that were moved out of the repo root for cleanliness. |
| `scripts/verification/` | Verification and benchmark-related utility scripts. |
| `assets/` | Images and static assets used by docs or packaging. |
| `deploy/` | Kubernetes and observability deployment helpers. |
| `examples/` | Example configuration and sample usage files. |
| `third_party/` | Imported upstream material and attribution-preserving references. |

## Good places to start

- Product behavior or tool surface: `src/waggle/server.py`
- Memory correctness: `src/waggle/graph.py`, `src/waggle/orchestrator.py`, `tests/test_graph.py`
- Retrieval quality: `src/waggle/retrieval/hybrid.py`, `src/waggle/recursive_context.py`
- Contributor ergonomics: `README.md`, `CONTRIBUTING.md`, `docs/install/`
- Extension work: `packages/vscode-extension/` or `packages/claude-desktop-extension/`
