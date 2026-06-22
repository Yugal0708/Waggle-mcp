# Changelog

All notable changes to this project will be documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **Temporal validity enforcement** (`valid_to` / `valid_from` filtering):
  - `query_graph` and `aggregate_graph` now exclude nodes whose `valid_to` has
    passed by default.
  - New parameter `include_invalidated: bool = False` on both tools — set to
    `true` to retrieve expired nodes.
  - New parameter `as_of: Optional[datetime] = None` on both tools — when
    provided, returns only nodes whose validity window contains that point in
    time (overrides `include_invalidated`).
  - `resolve_conflict` accepts a new optional `winner` parameter (node ID).
    When provided and the edge type is `CONTRADICTS` or `UPDATES`, the losing
    node's `valid_to` is set to `now()`, superseding it from future default
    queries. Passing a `winner` that is not an endpoint of the edge raises
    `ValueError`.
- Apache-2.0 licensing for Waggle Core via `LICENSE`.
- `docs/commercial.md` clarifying the public Core vs future paid Plus split.

### Changed
- `resolve_conflict` now records `winner` in edge metadata when provided.
- Supersession events are logged at `INFO` level with both node IDs and the
  resolution timestamp.
- Updated README positioning to present this repository as public Waggle Core,
  with Waggle Plus as coming soon.

### Feature Flag (temporary — removal scheduled)
- `WAGGLE_ENFORCE_VALID_TO` environment variable:
  - Default / unset / `"true"` → enforcement **active** (new behaviour).
  - `"false"` → enforcement **disabled** (legacy behaviour: expired nodes
    appear in default queries). A deprecation warning is logged.
  - **This flag will be removed in the next minor release.**

---

## [0.1.15] — 2026-05-07

### Added
- **VS Code extension**: `waggle-memory-0.0.2.vsix` — one-click workspace
  onboarding, installs `waggle-mcp` with consent if missing, safely creates
  or updates `.vscode/mcp.json`, preserves existing non-Waggle MCP servers,
  runs `waggle-mcp doctor`, opens Graph Studio, and exports Waggle memory
  from the editor.
- **Claude Desktop bundle**: `claude-desktop-extension.mcpb` distributed via
  GitHub Releases.
- Claude Code one-liner install:
- pipx install waggle-mcp
- 
claude mcp add --transport stdio waggle -- waggle-mcp serve --transport stdio
- VS Code Marketplace listing: **Waggle: Local Memory for AI Agents**.

### Links
- [Release notes](https://github.com/Abhigyan-Shekhar/Waggle-mcp/releases/tag/v0.1.15)
- [PyPI](https://pypi.org/project/waggle-mcp/0.1.15/)

---

## [0.1.12] — 2026-04-25

### Added
- README prompt instructions for automatic Waggle tool usage across sessions.
- Render deployment compatibility via `PORT` fallback env var and `render.yaml`
  blueprint config.
- Install failure troubleshooting section in docs.

### Fixed
- `prime_context` `KeyError` on non-embeddable seed nodes.

### Changed
- Removed public MIT/license metadata from the package; package URLs now
  point to PyPI.

### Links
- [Release notes](https://github.com/Abhigyan-Shekhar/Waggle-mcp/releases/tag/v0.1.12)

---

## [0.1.9] — 2026-04-22

### Added
- `waggle-mcp ingest-transcript-handoff` CLI command for rollover transcript
  ingestion and session-scoped handoff export.
- Automatic memory setup docs for **Codex** and **Antigravity**, including
  reusable rule text.
- Temporal retrieval improvements for queries about current/latest/original
  state.

### Fixed
- Append-only reruns producing duplicate ingestion.
- Trailing-user completion edge case in transcript ingestion.
- Evidence turn indexing off-by-one.
- Export failure handling in transcript handoff ingestion.

### Links
- [Release notes](https://github.com/Abhigyan-Shekhar/Waggle-mcp/releases/tag/v0.1.9)
- [PyPI](https://pypi.org/project/waggle-mcp/0.1.9/)

---

## [0.1.7] — 2026-04-18

### Added
- **Benchmark harness**: end-to-end `WaggleAdapter` connecting the graph
  engine to ConvoMem / MemBench runners with automated exact-match scoring
  and latency logging.
- **LongMemEval integration**: CLI-driven ingestion and retrieval evaluation
  against the official LongMemEval split.
  - Benchmark results: **97.4% R@5** (full split), **81.6% R@5** (held-out).
  - Deduplication recall: **77.3%** (zero false-positive merges maintained).
- **Logging utilities** (`logging_utils`): structured log helpers for
  consistent, level-aware output across all subsystems.
- **Evidence tracking** (`evidence.py`): records source provenance on stored
  nodes so reasoning chains are fully traceable.
- **Observability stack**: Grafana dashboard, Prometheus config, and Docker
  Compose overlay under `deploy/observability/`.
- **Kubernetes manifests**: production-grade `deployment.yaml`, network
  policy, external-secret, and certificate templates under `deploy/kubernetes/`.
- **Operational runbooks**: incident response, secret management, API-key
  rotation, and onboarding guides in `docs/runbooks/`.

### Changed
- README updated with honest benchmark presentation (held-out number leads),
  audience guide (individual dev vs. team), and visible edges warning in
  Quick Start.

### Links
- [Release notes](https://github.com/Abhigyan-Shekhar/Waggle-mcp/releases/tag/v0.1.7)
- [PyPI](https://pypi.org/project/waggle-mcp/0.1.7/)

---

## [0.1.3] — 2026-04-12

### Added
- `[project.urls]` in `pyproject.toml` package metadata — Homepage,
  Repository, Docs, Bug Tracker, and Changelog now appear on the PyPI sidebar.
- Animated terminal demo (`waggle-mcp init`) shipped with the repository.

### Fixed
- Banner and demo SVG now use the correct **waggle-mcp** branding throughout
  (was showing incorrect name in some places).

### Links
- [Release notes](https://github.com/Abhigyan-Shekhar/Waggle-mcp/releases/tag/v0.1.3)
- [PyPI](https://pypi.org/project/waggle-mcp/0.1.3/)

---

[Unreleased]: https://github.com/Abhigyan-Shekhar/Waggle-mcp/compare/v0.1.15...HEAD
[0.1.15]: https://github.com/Abhigyan-Shekhar/Waggle-mcp/compare/v0.1.12...v0.1.15
[0.1.12]: https://github.com/Abhigyan-Shekhar/Waggle-mcp/compare/v0.1.9...v0.1.12
[0.1.9]: https://github.com/Abhigyan-Shekhar/Waggle-mcp/compare/v0.1.7...v0.1.9
[0.1.7]: https://github.com/Abhigyan-Shekhar/Waggle-mcp/compare/v0.1.3...v0.1.7
[0.1.3]: https://github.com/Abhigyan-Shekhar/Waggle-mcp/releases/tag/v0.1.3
