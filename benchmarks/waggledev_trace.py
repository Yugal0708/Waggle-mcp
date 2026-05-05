"""
benchmarks/waggledev_trace.py
==============================
WaggleDev-Trace: Semi-real benchmark using Waggle development history.

DISCLAIMER: This is a semi-real benchmark derived from Waggle development
documentation (paper, README, repo history). It is NOT real agent traces.
All entries are clearly labelled as semi-real synthetic data derived from
repo documentation.

The benchmark tests 6 task types:
  - latest_decision    : What is the current decision on X?
  - relevant_module    : Which module/file implements X?
  - active_constraint  : What is the constraint on X?
  - next_step          : What is the next step for X?
  - limitation_recall  : What is the limitation of X?
  - superseded_approach: What was superseded/rejected?

Usage:
  python benchmarks/waggledev_trace.py \\
    --methods raw_context query_graph hybrid_rrf prime_context build_context \\
    --seed 42 \\
    --output benchmark_results/
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import random
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Path bootstrap
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_SRC = _HERE.parent / "src"
if _SRC.exists() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import numpy as np

from waggle.graph import MemoryGraph
from waggle.models import NodeType

# Re-use helpers from rlm_style_waggle_eval (import directly by path)
_BENCH_DIR = Path(__file__).resolve().parent
if str(_BENCH_DIR) not in sys.path:
    sys.path.insert(0, str(_BENCH_DIR))

from rlm_style_waggle_eval import (  # noqa: E402
    _DeterministicEmbedding,
    _METHOD_RUNNERS,
    exact_match,
    token_estimate,
)

LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Semi-real trace data
# Clearly labelled: semi-real synthetic data derived from Waggle development
# documentation (paper/repo). NOT real agent traces.
# ---------------------------------------------------------------------------

WAGGLEDEV_TRACE = [
    # Decisions
    {
        "label": "Use SQLite for local storage",
        "content": (
            "We decided to use SQLite with WAL mode for local-first deployments. "
            "Neo4j is available as an optional backend."
        ),
        "node_type": "decision",
        "tags": ["storage", "architecture"],
    },
    {
        "label": "Hybrid retrieval as default",
        "content": (
            "query_graph uses hybrid retrieval (vector + BM25 + graph) by default. "
            "graph_raw is the most reproducible mode."
        ),
        "node_type": "decision",
        "tags": ["retrieval", "architecture"],
    },
    {
        "label": "Verbatim-first architecture",
        "content": (
            "observe_conversation always persists verbatim turns first before running "
            "extraction. Extraction failures are non-fatal."
        ),
        "node_type": "decision",
        "tags": ["architecture", "reliability"],
    },
    {
        "label": "all-MiniLM-L6-v2 as default embedding model",
        "content": (
            "The default embedding model is all-MiniLM-L6-v2 (384-dim, ~420MB). "
            "A deterministic SHA-256 fallback is available for offline use."
        ),
        "node_type": "decision",
        "tags": ["embeddings", "architecture"],
    },
    {
        "label": "AblationConfig via flags not copy-paste",
        "content": (
            "Ablation variants are implemented via AblationConfig dataclass flags, "
            "not copy-pasted controllers. ablation=None preserves existing behaviour."
        ),
        "node_type": "decision",
        "tags": ["ablation", "implementation"],
    },
    # Constraints
    {
        "label": "No external LLM APIs required",
        "content": (
            "All retrieval must work fully local. "
            "No external model API is required for the core system."
        ),
        "node_type": "preference",
        "tags": ["constraint", "local-first"],
    },
    {
        "label": "Deterministic seeds for benchmarks",
        "content": (
            "All benchmark runners must use deterministic seeds. "
            "Default seed is 42. Paper-quality runs use seeds 42, 43, 44."
        ),
        "node_type": "preference",
        "tags": ["constraint", "reproducibility"],
    },
    {
        "label": "API keys never written to output files",
        "content": (
            "GROQ_API_KEY must only be read from os.environ. "
            "Keys must never be written to CSV, JSON, or MD output files."
        ),
        "node_type": "preference",
        "tags": ["constraint", "security"],
    },
    # Superseded/rejected
    {
        "label": "Rejected: copy-paste ablation controllers",
        "content": (
            "We rejected implementing ablation variants as separate copy-pasted "
            "controller classes. Instead we use AblationConfig flags."
        ),
        "node_type": "note",
        "tags": ["rejected", "ablation"],
    },
    {
        "label": "Superseded: deterministic embedding for benchmarks",
        "content": (
            "Early benchmarks used only the deterministic hash-based embedding. "
            "This was superseded by adding --real-embeddings flag to use all-MiniLM-L6-v2."
        ),
        "node_type": "decision",
        "tags": ["superseded", "embeddings"],
    },
    # Implementation facts
    {
        "label": "RecursiveContextController implements build_context",
        "content": (
            "The build_context MCP tool is implemented by RecursiveContextController "
            "in src/waggle/recursive_context.py."
        ),
        "node_type": "fact",
        "tags": ["implementation", "module"],
    },
    {
        "label": "ContextReset fix: broad project-state subqueries",
        "content": (
            "Short continuation queries like 'Continue from where we left off' now use "
            "broad project-state subqueries: recent decisions, active constraints, "
            "next steps, superseded directions."
        ),
        "node_type": "fact",
        "tags": ["fix", "context-reset"],
    },
    {
        "label": "pairwise_hidden_edge benchmark limitation",
        "content": (
            "The pairwise_hidden_edge benchmark does not isolate graph expansion because "
            "node labels are semantically distinctive enough for direct retrieval. "
            "Requires semantically indistinguishable labels."
        ),
        "node_type": "fact",
        "tags": ["limitation", "benchmark"],
    },
    {
        "label": "LongMemEval cache keyed by SHA-256",
        "content": (
            "The LongMemEval prepared-session cache is keyed by dataset SHA-256, mode, "
            "limit, and embedding model. Warm cache is used for all reported numbers."
        ),
        "node_type": "fact",
        "tags": ["implementation", "longmemeval"],
    },
    {
        "label": "MCP tool aliases for build_context",
        "content": (
            "build_context has three aliases: recursive_context, assemble_context, "
            "rlm_context. All resolve to the same handler."
        ),
        "node_type": "fact",
        "tags": ["implementation", "mcp"],
    },
    # Next steps
    {
        "label": "Next: evaluate on real RLM benchmark datasets",
        "content": (
            "The most important next step is evaluating on the full RLM public benchmark "
            "suite: trec_coarse OOLONG, OOLONG-Pairs, BrowseComp-Plus, LongBench-v2 CodeQA."
        ),
        "node_type": "question",
        "tags": ["next-step", "future-work"],
    },
    {
        "label": "Next: replace heuristic decomposition with learned decomposer",
        "content": (
            "Future work: replace keyword-pattern subquery generation with a learned "
            "decomposer trained on agent memory tasks."
        ),
        "node_type": "question",
        "tags": ["next-step", "future-work"],
    },
    {
        "label": "Next: construct pairwise benchmark with indistinguishable labels",
        "content": (
            "To causally isolate graph expansion, construct a pairwise_hidden_edge variant "
            "where choice and constraint labels are semantically similar to distractors."
        ),
        "node_type": "question",
        "tags": ["next-step", "benchmark"],
    },
    # Bugs/limitations
    {
        "label": "graph_hybrid reranking sensitivity",
        "content": (
            "graph_hybrid has a 5.3pp dev/test gap on LongMemEval-S. "
            "The heuristic reranking weights are partially tuned to this distribution."
        ),
        "node_type": "note",
        "tags": ["limitation", "longmemeval"],
    },
    {
        "label": "OOLONG linear aggregation remains hard",
        "content": (
            "OOLONG-style linear aggregation degrades with scale for all methods. "
            "This is a fundamental O(n) coverage limit under fixed token budget."
        ),
        "node_type": "note",
        "tags": ["limitation", "oolong"],
    },
]

WAGGLEDEV_QUESTIONS = [
    {
        "question": "What is the default embedding model used by Waggle?",
        "gold": "all-MiniLM-L6-v2",
        "task_type": "latest_decision",
    },
    {
        "question": "Which module implements the build_context tool?",
        "gold": "RecursiveContextController",
        "task_type": "relevant_module",
    },
    {
        "question": "What storage backend does Waggle use by default?",
        "gold": "SQLite",
        "task_type": "latest_decision",
    },
    {
        "question": "What was rejected in favor of AblationConfig flags?",
        "gold": "copy-paste ablation controllers",
        "task_type": "rejected_approach",
    },
    {
        "question": "What is the active constraint on API key handling?",
        "gold": "GROQ_API_KEY must only be read from os.environ",
        "task_type": "active_constraint",
    },
    {
        "question": "What is the next step for evaluating on real benchmarks?",
        "gold": "trec_coarse OOLONG",
        "task_type": "next_step",
    },
    {
        "question": "What is the limitation of the pairwise_hidden_edge benchmark?",
        "gold": "node labels are semantically distinctive enough for direct retrieval",
        "task_type": "limitation_recall",
    },
    {
        "question": "What fix was applied to the ContextReset benchmark?",
        "gold": "broad project-state subqueries",
        "task_type": "latest_decision",
    },
    {
        "question": "What is the default retrieval mode for query_graph?",
        "gold": "hybrid",
        "task_type": "latest_decision",
    },
    {
        "question": "What is the dev/test gap for graph_hybrid on LongMemEval-S?",
        "gold": "5.3pp",
        "task_type": "limitation_recall",
    },
    {
        "question": "What are the MCP tool aliases for build_context?",
        "gold": "recursive_context, assemble_context, rlm_context",
        "task_type": "relevant_module",
    },
    {
        "question": "What is the constraint on benchmark seeds?",
        "gold": "deterministic seeds, default 42",
        "task_type": "active_constraint",
    },
    {
        "question": "What superseded the deterministic embedding for benchmarks?",
        "gold": "--real-embeddings flag to use all-MiniLM-L6-v2",
        "task_type": "superseded_approach",
    },
    {
        "question": "What is the fundamental limitation of OOLONG linear aggregation?",
        "gold": "O(n) coverage limit under fixed token budget",
        "task_type": "limitation_recall",
    },
    {
        "question": "How is the LongMemEval cache keyed?",
        "gold": "SHA-256",
        "task_type": "relevant_module",
    },
    {
        "question": "What is the next step for decomposition improvement?",
        "gold": "learned decomposer",
        "task_type": "next_step",
    },
    {
        "question": "What is the verbatim-first architecture decision?",
        "gold": "observe_conversation always persists verbatim turns first",
        "task_type": "latest_decision",
    },
    {
        "question": "What is the constraint on external LLM APIs?",
        "gold": "No external model API required",
        "task_type": "active_constraint",
    },
    {
        "question": "What benchmark needs semantically indistinguishable labels?",
        "gold": "pairwise_hidden_edge",
        "task_type": "next_step",
    },
    {
        "question": "What is the default seed for benchmark runs?",
        "gold": "42",
        "task_type": "active_constraint",
    },
]

# ---------------------------------------------------------------------------
# Node type mapping
# ---------------------------------------------------------------------------

_NODE_TYPE_MAP = {
    "decision": NodeType.DECISION,
    "preference": NodeType.PREFERENCE,
    "fact": NodeType.FACT,
    "note": NodeType.NOTE,
    "question": NodeType.QUESTION,
}


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class TraceResult:
    question: str
    task_type: str
    gold: str
    method: str
    exact_match: float
    evidence_coverage: float
    tokens_returned: int
    latency_ms: float
    seed: int
    token_budget: int
    notes: str = ""


# ---------------------------------------------------------------------------
# Graph factory (reuse deterministic embedding from rlm_style_waggle_eval)
# ---------------------------------------------------------------------------


def _make_trace_graph(db_path: str) -> MemoryGraph:
    """Create a fresh MemoryGraph with deterministic embedding."""
    return MemoryGraph(db_path, _DeterministicEmbedding())


def _insert_trace_nodes(graph: MemoryGraph, project: str = "waggledev") -> None:
    """Insert all 20 WAGGLEDEV_TRACE nodes into the graph."""
    for entry in WAGGLEDEV_TRACE:
        node_type = _NODE_TYPE_MAP.get(entry["node_type"], NodeType.FACT)
        graph.add_node(
            label=entry["label"],
            content=entry["content"],
            node_type=node_type,
            project=project,
            tags=entry.get("tags", []),
        )


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------


def _score_exact_match(pack: str, gold: str) -> float:
    """1.0 if gold appears verbatim (case-insensitive) in pack, else 0.0."""
    return 1.0 if gold.strip().lower() in pack.strip().lower() else 0.0


def _score_evidence_coverage(pack: str, gold: str) -> float:
    """Fraction of gold tokens found in pack (case-insensitive)."""
    gold_tokens = [t.strip().lower() for t in gold.split() if t.strip()]
    if not gold_tokens:
        return 1.0
    found = sum(1 for t in gold_tokens if t in pack.lower())
    return found / len(gold_tokens)


# ---------------------------------------------------------------------------
# Main benchmark runner
# ---------------------------------------------------------------------------


def run_waggledev_trace_benchmark(
    methods: list[str],
    token_budget: int = 1200,
    seed: int = 42,
    output_dir: str = "benchmark_results",
    verbose: bool = False,
) -> list[TraceResult]:
    """
    Run the WaggleDev-Trace benchmark.

    Creates a fresh MemoryGraph, inserts all 20 trace nodes, then for each
    question × method: runs the method, scores exact_match and evidence_coverage.

    Writes results to:
      {output_dir}/waggledev_trace_results.csv
      {output_dir}/waggledev_trace_results.md
      {output_dir}/waggledev_trace_results.json

    DISCLAIMER: Semi-real benchmark derived from Waggle development documentation.
    Not real agent traces.
    """
    rng = random.Random(seed)
    results: list[TraceResult] = []

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        graph = _make_trace_graph(db_path)
        _insert_trace_nodes(graph)

        if verbose:
            print(f"[WaggleDev-Trace] Inserted {len(WAGGLEDEV_TRACE)} trace nodes.")
            print(f"[WaggleDev-Trace] Running {len(WAGGLEDEV_QUESTIONS)} questions × {len(methods)} methods")

        for q_entry in WAGGLEDEV_QUESTIONS:
            question = q_entry["question"]
            gold = q_entry["gold"]
            task_type = q_entry["task_type"]

            for method in methods:
                runner = _METHOD_RUNNERS.get(method)
                if runner is None:
                    LOGGER.warning("Unknown method: %s — skipping", method)
                    continue

                t0 = time.perf_counter()
                pack, latency = runner(graph, question, token_budget)
                latency_ms = round(latency, 1)

                em = _score_exact_match(pack, gold)
                ev_cov = _score_evidence_coverage(pack, gold)
                tokens = token_estimate(pack)

                result = TraceResult(
                    question=question,
                    task_type=task_type,
                    gold=gold,
                    method=method,
                    exact_match=em,
                    evidence_coverage=ev_cov,
                    tokens_returned=tokens,
                    latency_ms=latency_ms,
                    seed=seed,
                    token_budget=token_budget,
                    notes="Semi-real benchmark derived from Waggle development documentation. Not real agent traces.",
                )
                results.append(result)

                if verbose:
                    status = "✓" if em == 1.0 else "✗"
                    print(
                        f"  {status} [{task_type}] {method}: "
                        f"em={em:.1f} cov={ev_cov:.2f} tokens={tokens} "
                        f"q={question[:50]!r}"
                    )

    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass

    # Write outputs
    _write_results(results, output_dir)
    return results


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------


def _write_results(results: list[TraceResult], output_dir: str) -> None:
    """Write results to CSV, MD, and JSON."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    disclaimer = (
        "Semi-real benchmark derived from Waggle development documentation. "
        "Not real agent traces."
    )

    # --- CSV ---
    csv_path = out / "waggledev_trace_results.csv"
    fieldnames = [
        "question", "task_type", "gold", "method",
        "exact_match", "evidence_coverage", "tokens_returned",
        "latency_ms", "seed", "token_budget", "notes",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(asdict(r))
    print(f"[WaggleDev-Trace] CSV written: {csv_path}")

    # --- JSON ---
    json_path = out / "waggledev_trace_results.json"
    summary = _build_summary(results, disclaimer)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"[WaggleDev-Trace] JSON written: {json_path}")

    # --- Markdown ---
    md_path = out / "waggledev_trace_results.md"
    _write_markdown(results, md_path, disclaimer, summary)
    print(f"[WaggleDev-Trace] Markdown written: {md_path}")


def _build_summary(results: list[TraceResult], disclaimer: str) -> dict:
    """Build a summary dict grouped by method."""
    from collections import defaultdict

    by_method: dict[str, list[TraceResult]] = defaultdict(list)
    for r in results:
        by_method[r.method].append(r)

    method_summaries = {}
    for method, rows in by_method.items():
        n = len(rows)
        avg_em = sum(r.exact_match for r in rows) / n if n else 0.0
        avg_cov = sum(r.evidence_coverage for r in rows) / n if n else 0.0
        avg_tokens = sum(r.tokens_returned for r in rows) / n if n else 0.0
        avg_latency = sum(r.latency_ms for r in rows) / n if n else 0.0

        by_task: dict[str, list[float]] = defaultdict(list)
        for r in rows:
            by_task[r.task_type].append(r.exact_match)
        task_scores = {t: sum(v) / len(v) for t, v in by_task.items()}

        method_summaries[method] = {
            "n_questions": n,
            "avg_exact_match": round(avg_em, 3),
            "avg_evidence_coverage": round(avg_cov, 3),
            "avg_tokens_returned": round(avg_tokens, 1),
            "avg_latency_ms": round(avg_latency, 1),
            "by_task_type": {t: round(v, 3) for t, v in sorted(task_scores.items())},
        }

    return {
        "benchmark": "WaggleDev-Trace",
        "disclaimer": disclaimer,
        "n_questions": len(WAGGLEDEV_QUESTIONS),
        "n_trace_nodes": len(WAGGLEDEV_TRACE),
        "methods": method_summaries,
    }


def _write_markdown(
    results: list[TraceResult],
    md_path: Path,
    disclaimer: str,
    summary: dict,
) -> None:
    """Write a human-readable Markdown report."""
    lines = [
        "# WaggleDev-Trace Benchmark Results",
        "",
        f"> **Disclaimer:** {disclaimer}",
        "",
        f"- Questions: {len(WAGGLEDEV_QUESTIONS)}",
        f"- Trace nodes: {len(WAGGLEDEV_TRACE)}",
        "",
        "## Summary by Method",
        "",
        "| Method | Exact Match | Evidence Coverage | Avg Tokens | Avg Latency (ms) |",
        "|--------|-------------|-------------------|------------|-----------------|",
    ]

    for method, stats in summary["methods"].items():
        lines.append(
            f"| `{method}` "
            f"| {stats['avg_exact_match']:.3f} "
            f"| {stats['avg_evidence_coverage']:.3f} "
            f"| {stats['avg_tokens_returned']:.0f} "
            f"| {stats['avg_latency_ms']:.1f} |"
        )

    lines += [
        "",
        "## By Task Type",
        "",
    ]

    # Collect all task types
    task_types = sorted({r.task_type for r in results})
    methods = sorted({r.method for r in results})

    header = "| Task Type | " + " | ".join(f"`{m}`" for m in methods) + " |"
    sep = "|-----------|" + "|".join("------" for _ in methods) + "|"
    lines += [header, sep]

    from collections import defaultdict
    by_task_method: dict[tuple[str, str], list[float]] = defaultdict(list)
    for r in results:
        by_task_method[(r.task_type, r.method)].append(r.exact_match)

    for tt in task_types:
        row = f"| {tt} |"
        for m in methods:
            scores = by_task_method.get((tt, m), [])
            avg = sum(scores) / len(scores) if scores else 0.0
            row += f" {avg:.3f} |"
        lines.append(row)

    lines += [
        "",
        "## Per-Question Results",
        "",
        "| Question | Gold | Task Type | Method | EM | Coverage | Tokens |",
        "|----------|------|-----------|--------|----|----------|--------|",
    ]

    for r in results:
        q_short = r.question[:50].replace("|", "\\|")
        g_short = r.gold[:30].replace("|", "\\|")
        lines.append(
            f"| {q_short} | {g_short} | {r.task_type} "
            f"| `{r.method}` | {r.exact_match:.1f} "
            f"| {r.evidence_coverage:.2f} | {r.tokens_returned} |"
        )

    lines += ["", f"*{disclaimer}*", ""]

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "WaggleDev-Trace: Semi-real benchmark using Waggle development history. "
            "DISCLAIMER: Semi-real benchmark derived from Waggle development documentation. "
            "Not real agent traces."
        )
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        default=["raw_context", "query_graph", "build_context"],
        help="Methods to evaluate (default: raw_context query_graph build_context)",
    )
    parser.add_argument(
        "--token-budget",
        type=int,
        default=1200,
        help="Token budget for context assembly (default: 1200)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42)",
    )
    parser.add_argument(
        "--output",
        default="benchmark_results",
        help="Output directory for results (default: benchmark_results)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-question results",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    print(
        "\n[WaggleDev-Trace] DISCLAIMER: Semi-real benchmark derived from Waggle "
        "development documentation. Not real agent traces.\n"
    )
    print(f"[WaggleDev-Trace] Methods: {args.methods}")
    print(f"[WaggleDev-Trace] Token budget: {args.token_budget}")
    print(f"[WaggleDev-Trace] Seed: {args.seed}")
    print(f"[WaggleDev-Trace] Output: {args.output}")
    print()

    results = run_waggledev_trace_benchmark(
        methods=args.methods,
        token_budget=args.token_budget,
        seed=args.seed,
        output_dir=args.output,
        verbose=args.verbose,
    )

    # Print summary table
    from collections import defaultdict
    by_method: dict[str, list[TraceResult]] = defaultdict(list)
    for r in results:
        by_method[r.method].append(r)

    print("\n[WaggleDev-Trace] Summary:")
    print(f"{'Method':<25} {'Exact Match':>12} {'Coverage':>10} {'Tokens':>8}")
    print("-" * 60)
    for method in args.methods:
        rows = by_method.get(method, [])
        if not rows:
            continue
        avg_em = sum(r.exact_match for r in rows) / len(rows)
        avg_cov = sum(r.evidence_coverage for r in rows) / len(rows)
        avg_tok = sum(r.tokens_returned for r in rows) / len(rows)
        print(f"{method:<25} {avg_em:>12.3f} {avg_cov:>10.3f} {avg_tok:>8.0f}")

    print(
        "\n[WaggleDev-Trace] DISCLAIMER: Semi-real benchmark derived from Waggle "
        "development documentation. Not real agent traces."
    )


if __name__ == "__main__":
    main()
