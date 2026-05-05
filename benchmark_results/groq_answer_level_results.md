# RMCA Answer-Level Evaluation Results

> **DISCLAIMER:** Deterministic answer-level metrics are reproducible lower bounds. They are not equivalent to human preference ratings or LLM-judge quality assessments. Scores should be interpreted as retrieval-quality proxies, not end-to-end answer quality.

> **LLM EVAL CAVEAT:** These results use one answering model (Groq llama-3.3-70b-versatile) and should be replicated across models. The model is an answerer, not an independent human judge.

| Family | Scale | Method | Answerer | EM | F1 | Ev.Used | Contra.Corr | Hall.Rate | Tokens |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| context_reset | 128 | rmca_full | groq | 0.000 | 0.286 | 0.500 | 1.000 | 0.000 | 441 |
| context_reset | 128 | query_graph | groq | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 76 |
| context_reset | 128 | bm25_topk | groq | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1413 |
| context_reset | 128 | raw_context | groq | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1413 |
| context_reset | 512 | rmca_full | groq | 0.000 | 0.286 | 0.500 | 1.000 | 1.000 | 441 |
| context_reset | 512 | query_graph | groq | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 76 |
| context_reset | 512 | bm25_topk | groq | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1437 |
| context_reset | 512 | raw_context | groq | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1437 |
| codeqa | 128 | rmca_full | groq | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 535 |
| codeqa | 128 | query_graph | groq | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 178 |
| codeqa | 128 | bm25_topk | groq | 1.000 | 0.545 | 1.000 | 1.000 | 0.000 | 1398 |
| codeqa | 128 | raw_context | groq | 0.000 | 0.000 | 0.500 | 1.000 | 0.000 | 1382 |
| codeqa | 512 | rmca_full | groq | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | 642 |
| codeqa | 512 | query_graph | groq | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | 150 |
| codeqa | 512 | bm25_topk | groq | 0.000 | 0.000 | 0.500 | 1.000 | 1.000 | 1400 |
| codeqa | 512 | raw_context | groq | 0.000 | 0.000 | 0.500 | 1.000 | 1.000 | 1400 |

