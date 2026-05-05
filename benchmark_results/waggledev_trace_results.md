# WaggleDev-Trace Benchmark Results

> **Disclaimer:** Semi-real benchmark derived from Waggle development documentation. Not real agent traces.

- Questions: 20
- Trace nodes: 20

## Summary by Method

| Method | Exact Match | Evidence Coverage | Avg Tokens | Avg Latency (ms) |
|--------|-------------|-------------------|------------|-----------------|
| `raw_context` | 0.850 | 0.978 | 865 | 0.9 |
| `query_graph` | 0.750 | 0.868 | 239 | 1.6 |
| `hybrid_rrf` | 0.850 | 0.978 | 865 | 0.9 |
| `prime_context` | 0.000 | 0.033 | 22 | 1.0 |
| `build_context` | 0.850 | 0.968 | 546 | 9.1 |

## By Task Type

| Task Type | `build_context` | `hybrid_rrf` | `prime_context` | `query_graph` | `raw_context` |
|-----------|------|------|------|------|------|
| active_constraint | 0.500 | 0.500 | 0.000 | 0.500 | 0.500 |
| latest_decision | 1.000 | 1.000 | 0.000 | 0.600 | 1.000 |
| limitation_recall | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 |
| next_step | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 |
| rejected_approach | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 |
| relevant_module | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 |
| superseded_approach | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Per-Question Results

| Question | Gold | Task Type | Method | EM | Coverage | Tokens |
|----------|------|-----------|--------|----|----------|--------|
| What is the default embedding model used by Waggle | all-MiniLM-L6-v2 | latest_decision | `raw_context` | 1.0 | 1.00 | 865 |
| What is the default embedding model used by Waggle | all-MiniLM-L6-v2 | latest_decision | `query_graph` | 1.0 | 1.00 | 210 |
| What is the default embedding model used by Waggle | all-MiniLM-L6-v2 | latest_decision | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What is the default embedding model used by Waggle | all-MiniLM-L6-v2 | latest_decision | `prime_context` | 0.0 | 0.00 | 22 |
| What is the default embedding model used by Waggle | all-MiniLM-L6-v2 | latest_decision | `build_context` | 1.0 | 1.00 | 598 |
| Which module implements the build_context tool? | RecursiveContextController | relevant_module | `raw_context` | 1.0 | 1.00 | 865 |
| Which module implements the build_context tool? | RecursiveContextController | relevant_module | `query_graph` | 1.0 | 1.00 | 218 |
| Which module implements the build_context tool? | RecursiveContextController | relevant_module | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| Which module implements the build_context tool? | RecursiveContextController | relevant_module | `prime_context` | 0.0 | 0.00 | 22 |
| Which module implements the build_context tool? | RecursiveContextController | relevant_module | `build_context` | 1.0 | 1.00 | 672 |
| What storage backend does Waggle use by default? | SQLite | latest_decision | `raw_context` | 1.0 | 1.00 | 865 |
| What storage backend does Waggle use by default? | SQLite | latest_decision | `query_graph` | 0.0 | 0.00 | 222 |
| What storage backend does Waggle use by default? | SQLite | latest_decision | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What storage backend does Waggle use by default? | SQLite | latest_decision | `prime_context` | 0.0 | 0.00 | 22 |
| What storage backend does Waggle use by default? | SQLite | latest_decision | `build_context` | 1.0 | 1.00 | 561 |
| What was rejected in favor of AblationConfig flags | copy-paste ablation controller | rejected_approach | `raw_context` | 1.0 | 1.00 | 865 |
| What was rejected in favor of AblationConfig flags | copy-paste ablation controller | rejected_approach | `query_graph` | 1.0 | 1.00 | 231 |
| What was rejected in favor of AblationConfig flags | copy-paste ablation controller | rejected_approach | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What was rejected in favor of AblationConfig flags | copy-paste ablation controller | rejected_approach | `prime_context` | 0.0 | 0.00 | 22 |
| What was rejected in favor of AblationConfig flags | copy-paste ablation controller | rejected_approach | `build_context` | 1.0 | 1.00 | 596 |
| What is the active constraint on API key handling? | GROQ_API_KEY must only be read | active_constraint | `raw_context` | 1.0 | 1.00 | 865 |
| What is the active constraint on API key handling? | GROQ_API_KEY must only be read | active_constraint | `query_graph` | 1.0 | 1.00 | 234 |
| What is the active constraint on API key handling? | GROQ_API_KEY must only be read | active_constraint | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What is the active constraint on API key handling? | GROQ_API_KEY must only be read | active_constraint | `prime_context` | 0.0 | 0.14 | 22 |
| What is the active constraint on API key handling? | GROQ_API_KEY must only be read | active_constraint | `build_context` | 1.0 | 1.00 | 552 |
| What is the next step for evaluating on real bench | trec_coarse OOLONG | next_step | `raw_context` | 1.0 | 1.00 | 865 |
| What is the next step for evaluating on real bench | trec_coarse OOLONG | next_step | `query_graph` | 1.0 | 1.00 | 257 |
| What is the next step for evaluating on real bench | trec_coarse OOLONG | next_step | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What is the next step for evaluating on real bench | trec_coarse OOLONG | next_step | `prime_context` | 0.0 | 0.00 | 22 |
| What is the next step for evaluating on real bench | trec_coarse OOLONG | next_step | `build_context` | 1.0 | 1.00 | 492 |
| What is the limitation of the pairwise_hidden_edge | node labels are semantically d | limitation_recall | `raw_context` | 1.0 | 1.00 | 865 |
| What is the limitation of the pairwise_hidden_edge | node labels are semantically d | limitation_recall | `query_graph` | 1.0 | 1.00 | 258 |
| What is the limitation of the pairwise_hidden_edge | node labels are semantically d | limitation_recall | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What is the limitation of the pairwise_hidden_edge | node labels are semantically d | limitation_recall | `prime_context` | 0.0 | 0.11 | 22 |
| What is the limitation of the pairwise_hidden_edge | node labels are semantically d | limitation_recall | `build_context` | 1.0 | 1.00 | 592 |
| What fix was applied to the ContextReset benchmark | broad project-state subqueries | latest_decision | `raw_context` | 1.0 | 1.00 | 865 |
| What fix was applied to the ContextReset benchmark | broad project-state subqueries | latest_decision | `query_graph` | 1.0 | 1.00 | 271 |
| What fix was applied to the ContextReset benchmark | broad project-state subqueries | latest_decision | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What fix was applied to the ContextReset benchmark | broad project-state subqueries | latest_decision | `prime_context` | 0.0 | 0.00 | 22 |
| What fix was applied to the ContextReset benchmark | broad project-state subqueries | latest_decision | `build_context` | 1.0 | 1.00 | 637 |
| What is the default retrieval mode for query_graph | hybrid | latest_decision | `raw_context` | 1.0 | 1.00 | 865 |
| What is the default retrieval mode for query_graph | hybrid | latest_decision | `query_graph` | 0.0 | 0.00 | 233 |
| What is the default retrieval mode for query_graph | hybrid | latest_decision | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What is the default retrieval mode for query_graph | hybrid | latest_decision | `prime_context` | 0.0 | 0.00 | 22 |
| What is the default retrieval mode for query_graph | hybrid | latest_decision | `build_context` | 1.0 | 1.00 | 565 |
| What is the dev/test gap for graph_hybrid on LongM | 5.3pp | limitation_recall | `raw_context` | 1.0 | 1.00 | 865 |
| What is the dev/test gap for graph_hybrid on LongM | 5.3pp | limitation_recall | `query_graph` | 1.0 | 1.00 | 247 |
| What is the dev/test gap for graph_hybrid on LongM | 5.3pp | limitation_recall | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What is the dev/test gap for graph_hybrid on LongM | 5.3pp | limitation_recall | `prime_context` | 0.0 | 0.00 | 22 |
| What is the dev/test gap for graph_hybrid on LongM | 5.3pp | limitation_recall | `build_context` | 1.0 | 1.00 | 626 |
| What are the MCP tool aliases for build_context? | recursive_context, assemble_co | relevant_module | `raw_context` | 1.0 | 1.00 | 865 |
| What are the MCP tool aliases for build_context? | recursive_context, assemble_co | relevant_module | `query_graph` | 1.0 | 1.00 | 214 |
| What are the MCP tool aliases for build_context? | recursive_context, assemble_co | relevant_module | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What are the MCP tool aliases for build_context? | recursive_context, assemble_co | relevant_module | `prime_context` | 0.0 | 0.00 | 22 |
| What are the MCP tool aliases for build_context? | recursive_context, assemble_co | relevant_module | `build_context` | 1.0 | 1.00 | 516 |
| What is the constraint on benchmark seeds? | deterministic seeds, default 4 | active_constraint | `raw_context` | 0.0 | 0.75 | 865 |
| What is the constraint on benchmark seeds? | deterministic seeds, default 4 | active_constraint | `query_graph` | 0.0 | 0.75 | 271 |
| What is the constraint on benchmark seeds? | deterministic seeds, default 4 | active_constraint | `hybrid_rrf` | 0.0 | 0.75 | 865 |
| What is the constraint on benchmark seeds? | deterministic seeds, default 4 | active_constraint | `prime_context` | 0.0 | 0.00 | 22 |
| What is the constraint on benchmark seeds? | deterministic seeds, default 4 | active_constraint | `build_context` | 0.0 | 0.75 | 583 |
| What superseded the deterministic embedding for be | --real-embeddings flag to use  | superseded_approach | `raw_context` | 0.0 | 0.80 | 865 |
| What superseded the deterministic embedding for be | --real-embeddings flag to use  | superseded_approach | `query_graph` | 0.0 | 0.60 | 235 |
| What superseded the deterministic embedding for be | --real-embeddings flag to use  | superseded_approach | `hybrid_rrf` | 0.0 | 0.80 | 865 |
| What superseded the deterministic embedding for be | --real-embeddings flag to use  | superseded_approach | `prime_context` | 0.0 | 0.20 | 22 |
| What superseded the deterministic embedding for be | --real-embeddings flag to use  | superseded_approach | `build_context` | 0.0 | 0.60 | 325 |
| What is the fundamental limitation of OOLONG linea | O(n) coverage limit under fixe | limitation_recall | `raw_context` | 1.0 | 1.00 | 865 |
| What is the fundamental limitation of OOLONG linea | O(n) coverage limit under fixe | limitation_recall | `query_graph` | 1.0 | 1.00 | 249 |
| What is the fundamental limitation of OOLONG linea | O(n) coverage limit under fixe | limitation_recall | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What is the fundamental limitation of OOLONG linea | O(n) coverage limit under fixe | limitation_recall | `prime_context` | 0.0 | 0.00 | 22 |
| What is the fundamental limitation of OOLONG linea | O(n) coverage limit under fixe | limitation_recall | `build_context` | 1.0 | 1.00 | 598 |
| How is the LongMemEval cache keyed? | SHA-256 | relevant_module | `raw_context` | 1.0 | 1.00 | 865 |
| How is the LongMemEval cache keyed? | SHA-256 | relevant_module | `query_graph` | 1.0 | 1.00 | 219 |
| How is the LongMemEval cache keyed? | SHA-256 | relevant_module | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| How is the LongMemEval cache keyed? | SHA-256 | relevant_module | `prime_context` | 0.0 | 0.00 | 22 |
| How is the LongMemEval cache keyed? | SHA-256 | relevant_module | `build_context` | 1.0 | 1.00 | 362 |
| What is the next step for decomposition improvemen | learned decomposer | next_step | `raw_context` | 1.0 | 1.00 | 865 |
| What is the next step for decomposition improvemen | learned decomposer | next_step | `query_graph` | 1.0 | 1.00 | 264 |
| What is the next step for decomposition improvemen | learned decomposer | next_step | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What is the next step for decomposition improvemen | learned decomposer | next_step | `prime_context` | 0.0 | 0.00 | 22 |
| What is the next step for decomposition improvemen | learned decomposer | next_step | `build_context` | 1.0 | 1.00 | 450 |
| What is the verbatim-first architecture decision? | observe_conversation always pe | latest_decision | `raw_context` | 1.0 | 1.00 | 865 |
| What is the verbatim-first architecture decision? | observe_conversation always pe | latest_decision | `query_graph` | 1.0 | 1.00 | 218 |
| What is the verbatim-first architecture decision? | observe_conversation always pe | latest_decision | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What is the verbatim-first architecture decision? | observe_conversation always pe | latest_decision | `prime_context` | 0.0 | 0.00 | 22 |
| What is the verbatim-first architecture decision? | observe_conversation always pe | latest_decision | `build_context` | 1.0 | 1.00 | 609 |
| What is the constraint on external LLM APIs? | No external model API required | active_constraint | `raw_context` | 0.0 | 1.00 | 865 |
| What is the constraint on external LLM APIs? | No external model API required | active_constraint | `query_graph` | 0.0 | 1.00 | 228 |
| What is the constraint on external LLM APIs? | No external model API required | active_constraint | `hybrid_rrf` | 0.0 | 1.00 | 865 |
| What is the constraint on external LLM APIs? | No external model API required | active_constraint | `prime_context` | 0.0 | 0.20 | 22 |
| What is the constraint on external LLM APIs? | No external model API required | active_constraint | `build_context` | 0.0 | 1.00 | 499 |
| What benchmark needs semantically indistinguishabl | pairwise_hidden_edge | next_step | `raw_context` | 1.0 | 1.00 | 865 |
| What benchmark needs semantically indistinguishabl | pairwise_hidden_edge | next_step | `query_graph` | 1.0 | 1.00 | 250 |
| What benchmark needs semantically indistinguishabl | pairwise_hidden_edge | next_step | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What benchmark needs semantically indistinguishabl | pairwise_hidden_edge | next_step | `prime_context` | 0.0 | 0.00 | 22 |
| What benchmark needs semantically indistinguishabl | pairwise_hidden_edge | next_step | `build_context` | 1.0 | 1.00 | 503 |
| What is the default seed for benchmark runs? | 42 | active_constraint | `raw_context` | 1.0 | 1.00 | 865 |
| What is the default seed for benchmark runs? | 42 | active_constraint | `query_graph` | 1.0 | 1.00 | 256 |
| What is the default seed for benchmark runs? | 42 | active_constraint | `hybrid_rrf` | 1.0 | 1.00 | 865 |
| What is the default seed for benchmark runs? | 42 | active_constraint | `prime_context` | 0.0 | 0.00 | 22 |
| What is the default seed for benchmark runs? | 42 | active_constraint | `build_context` | 1.0 | 1.00 | 582 |

*Semi-real benchmark derived from Waggle development documentation. Not real agent traces.*
