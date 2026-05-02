# Incident Postmortem: Embeddings Cache Invalidation and Ranking Regression

**Incident window:** April 25, 2026 to May 2, 2026
**Primary commit:** `f27011a` (`feat: ship hybrid retrieval, deterministic abhi, and graph studio refresh`)
**Severity:** Data integrity incident affecting benchmark validity
**Status:** Mitigated, with follow-up work open

## Summary

Commit `f27011a` introduced two separate regressions into the retrieval evaluation path at the same time:

1. A state-dependent initialization bug in [`src/waggle/embeddings.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/embeddings.py) caused `EmbeddingModel.model_version` to report `deterministic-v1` before the transformer had loaded, even when a real sentence-transformer model was configured.
2. A ranking formula change in [`src/waggle/longmemeval_benchmark.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/longmemeval_benchmark.py) reduced the semantic weight and added chunk-fusion behavior that regressed retrieval on LongMemEval short-answer sessions.

These regressions were discovered on May 2, 2026 after benchmark results from the April 25, 2026 to May 2, 2026 window showed inconsistent behavior across reruns. Detection was manual: a human noticed the inconsistency. No automated benchmark gate, cache-integrity check, or runtime monitor surfaced the problem first.

## Impact

- Cache keys generated during the incident window could claim deterministic embeddings while the cached vectors were actually produced by the configured transformer model.
- Any benchmark artifacts or tuning decisions produced from April 25, 2026 to May 2, 2026 must be treated as suspect until re-run.
- LongMemEval ranking quality regressed for queries with weak lexical overlap and heavy dependence on semantic similarity.
- The incident was silent. Existing tests did not assert cache-key/model consistency, and no benchmark gate blocked the regression before merge.

## What Happened

### 1. `model_version` returned the wrong cache identity

**Status:** Resolved  
**Code path:** [`src/waggle/embeddings.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/embeddings.py)

`EmbeddingModel.model_version` computed a cache identity from runtime state instead of configuration. After `f27011a`, the property inspected `self._model` directly. During cache-key construction, that property was called before any embeddings had been requested, so `self._model` was still `None`. The property then fell back to `deterministic-v1`.

Later in the same run, the real transformer model loaded successfully on demand and wrote transformer-produced vectors into cache files whose keys claimed deterministic embeddings. That broke cache determinism across runs and poisoned the benchmark cache.

### 2. `graph_raw` ranking regressed on LongMemEval

**Status:** Mitigated, generalization validation pending  
**Code path:** [`src/waggle/longmemeval_benchmark.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/longmemeval_benchmark.py#L736)

The same PR changed the raw ranking blend away from a semantic-dominant formula. The current restored implementation ranks with:

```python
combined_scores = (0.72 * semantic_scores) + (0.18 * lexical_scores) + (0.10 * temporal_scores)
```

This restored LongMemEval performance, but that does not prove the formula generalizes. The prior `0.60`-weighted variant appears to have been introduced to help a different distribution, likely OOLONG. LongMemEval therefore justifies the revert for that benchmark only. OOLONG validation is still required before this is treated as a global ranking decision.

### 3. Broad temporal hinting added ranking noise

**Status:** Resolved  
**Code path:** [`src/waggle/intelligence.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/intelligence.py#L612)

The broad temporal-hint additions to `infer_temporal_hints` were reverted after an ablation over 500 LongMemEval questions showed they triggered on too many non-temporal queries:

- `current` triggered on 25 questions, or `5.0%`
- `first` triggered on 42 questions, or `8.4%`
- broad rules applied temporal reranking to 67 additional questions, or `13.4%`, relative to the tighter rules

These triggers often did not imply temporal ordering. A representative failure mode was queries like "What is my current address?", where "current" identifies state, not a request for chronological reranking.

### 4. Exact@5 collapsed because retrieval depth was capped at 5

**Status:** Diagnosed  
**Code path:** LongMemEval report interpretation

For gold cardinalities `3`, `4`, `5`, and `6`, `R@5` remained `100%`. The drop in `Exact@5`, including `0.0%` at cardinality `6`, was a retrieval-depth limitation rather than a ranking failure. When six gold sessions exist, five result slots cannot contain all of them.

This means the next meaningful capability improvement is adaptive retrieval depth, not more scoring tweaks for these cases.

## Root Cause

This incident came from two mechanisms at once:

1. `f27011a` changed initialization behavior in the embedding stack. That created a configuration-versus-runtime identity bug in `model_version`.
2. `f27011a` was an oversized PR. `git show --stat f27011a` reports 81 files changed, with major edits across embeddings, ranking, graph retrieval, OOLONG evaluation, benchmark artifacts, and UI code. The PR scope was too broad to review the retrieval-specific regressions with enough isolation.

The correct lesson is therefore both architectural and process-oriented:

- initialization-path changes require benchmark and cache-integrity assertions
- large multi-system retrieval PRs need tighter scope or explicit benchmark gates before merge

## Detection Gap

This incident lasted for one week because the repository had prevention gaps and detection gaps at the same time. The incident did not close because the system detected it; it closed because a human became suspicious of rerun inconsistency on May 2, 2026 and investigated manually.

### Missing prevention checks

- No test asserted that `EmbeddingModel.model_version` must not resolve to `deterministic-v1` when a real transformer model is configured.
- No cache payload validation checked whether the stored vectors matched the declared embedding model identity.
- No benchmark test covered the ranking sensitivity of semantic-heavy LongMemEval prompts against alternative blends.

### Missing detection checks

- No CI benchmark gate blocked a LongMemEval regression before merge.
- No cache-integrity monitor flagged a mismatch between cache metadata and actual embedding outputs.
- No benchmark runbook marked the April 25, 2026 result window as untrusted after the cache identity bug was found.

## Customer and Artifact Revalidation

All benchmark artifacts generated from April 25, 2026 through May 2, 2026 are considered suspect until re-run.

**Revalidation requirement:**

- Re-run LongMemEval benchmark artifacts produced during the incident window.
- Re-run OOLONG benchmark artifacts that were used to justify or preserve the `0.60` ranking blend.
- Re-check any claims in docs or reports that were updated using incident-window results.

**Current local evidence in this repository:**

- [`benchmarks/longmemeval/results_graph_hybrid_2026-05-02.json`](/Users/abhigyanshekhar/Desktop/MCP/benchmarks/longmemeval/results_graph_hybrid_2026-05-02.json)
- [`benchmarks/longmemeval/results_graph_hybrid_2026-05-02_restored.json`](/Users/abhigyanshekhar/Desktop/MCP/benchmarks/longmemeval/results_graph_hybrid_2026-05-02_restored.json)
- [`benchmarks/longmemeval/results_graph_raw_2026-05-02.json`](/Users/abhigyanshekhar/Desktop/MCP/benchmarks/longmemeval/results_graph_raw_2026-05-02.json)
- [`benchmarks/longmemeval/results_graph_raw_2026-05-02_fixed.json`](/Users/abhigyanshekhar/Desktop/MCP/benchmarks/longmemeval/results_graph_raw_2026-05-02_fixed.json)
- [`benchmarks/longmemeval/results_graph_raw_2026-05-02_restored.json`](/Users/abhigyanshekhar/Desktop/MCP/benchmarks/longmemeval/results_graph_raw_2026-05-02_restored.json)
- [`benchmarks/longmemeval/results_graph_raw_2026-05-02_v2.json`](/Users/abhigyanshekhar/Desktop/MCP/benchmarks/longmemeval/results_graph_raw_2026-05-02_v2.json)

Those files should be retained as forensic context but not used as authoritative benchmark baselines unless they are explicitly marked revalidated.

## Corrective Actions

### Completed

- `model_version` was fixed to synchronously resolve the model if warmup has not started yet, so the version string behaves as a pure function of configuration.
- Broad temporal hints were reverted from [`infer_temporal_hints`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/intelligence.py#L612).
- The semantic-dominant LongMemEval formula was restored in [`_raw_candidate_order`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/longmemeval_benchmark.py#L736) as a mitigation for benchmark correctness.

### Correctness follow-ups

| Action | Owner | Due date | Status |
|-------|-------|----------|--------|
| Add an assertion that `model_version` never returns `deterministic-v1` when a non-deterministic transformer model is configured. | Retrieval | May 5, 2026 | Open |
| Add cache payload validation using a known probe vector checksum so silent embedding-model mismatches are caught on cache load. | Retrieval | May 9, 2026 | Open |
| Run OOLONG with both ranking formulas and publish a side-by-side comparison before treating the `0.72` blend as global policy. | Benchmarking | May 8, 2026 | Open |
| Decide whether ranking should be mode-specific, benchmark-specific, or dynamically blended after the OOLONG comparison. | Retrieval | May 9, 2026 | Open |
| Add a CI benchmark gate for LongMemEval retrieval-only `graph_raw` runs that fails PR validation if `R@5` drops by more than `1.0` absolute point or `Exact@5` drops by more than `2.0` absolute points relative to the checked-in baseline on the standard cache path. | Infra + Retrieval | May 12, 2026 | Open |

### Capability follow-ups

| Action | Owner | Target date | Status |
|-------|-------|-------------|--------|
| Design adaptive retrieval depth for high-cardinality queries where `Exact@5` is structurally capped. This is a capability project, not an incident-blocking correctness fix. | Retrieval | May 15, 2026 | Open |

## Blast Radius Audit

Section 5 in the original draft was too vague. The audit scope should track the actual retrieval-related surfaces touched by `f27011a`.

| Module | Why it is in scope | Owner | Due date | Status |
|-------|---------------------|-------|----------|--------|
| [`src/waggle/embeddings.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/embeddings.py) | State-dependent initialization and cache identity bug landed here. | Retrieval | May 5, 2026 | In progress |
| [`src/waggle/benchmark_cache.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/benchmark_cache.py) | Cache metadata and load validation should detect future mismatches. | Retrieval | May 9, 2026 | Open |
| [`src/waggle/longmemeval_benchmark.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/longmemeval_benchmark.py) | Raw candidate blend and chunk-fusion behavior changed here. | Benchmarking | May 8, 2026 | In progress |
| [`src/waggle/oolong_benchmark.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/oolong_benchmark.py) | Likely target distribution for the alternate formula; must be re-evaluated. | Benchmarking | May 8, 2026 | Open |
| [`src/waggle/retrieval/hybrid.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/retrieval/hybrid.py) | Same PR introduced hybrid retrieval behavior; inspect for similar lazy-init or weighting assumptions. | Retrieval | May 9, 2026 | Open |
| [`src/waggle/graph.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/graph.py) | Retrieval logic and temporal handling changed in the same PR. | Retrieval | May 9, 2026 | Open |
| [`src/waggle/neo4j_graph.py`](/Users/abhigyanshekhar/Desktop/MCP/src/waggle/neo4j_graph.py) | Mirror retrieval logic may duplicate scoring or threshold assumptions. | Retrieval | May 9, 2026 | Open |
| [`tests/test_embeddings.py`](/Users/abhigyanshekhar/Desktop/MCP/tests/test_embeddings.py) | Missing regression test coverage for cache identity invariants. | Retrieval | May 5, 2026 | Open |
| [`tests/test_longmemeval_benchmark.py`](/Users/abhigyanshekhar/Desktop/MCP/tests/test_longmemeval_benchmark.py) | Missing benchmark regression coverage for semantic-heavy sessions. | Benchmarking | May 8, 2026 | Open |

## Decision Record

- The `model_version` fix should merge immediately because it restores cache-key correctness and does not depend on benchmark policy.
- The LongMemEval `0.72` formula is accepted as a mitigation for LongMemEval only.
- OOLONG validation is a release-blocking follow-up for any claim that the restored formula is globally superior.
- Incident-window benchmark artifacts remain suspect until revalidated.

## Preventing Recurrence

1. Treat cache identity as configuration-derived metadata, enforced by the `model_version` assertion and cache probe-vector checksum follow-ups.
2. Require benchmark gates for retrieval-path changes that affect ranking, temporal interpretation, or cache identity, enforced by the LongMemEval CI gate defined above.
3. Add integrity checks that validate both metadata and payload, not just one or the other, enforced by the cache checksum follow-up.

## Appendix: Why "Heisenbug" Was the Wrong Label

The original header called the `model_version` bug a "Heisenbug". That label is imprecise. The bug was not observation-sensitive; it was an initialization-order bug caused by call timing and lazy loading. The distinction matters because the corrective action is deterministic: remove state-dependent identity from the API contract.
