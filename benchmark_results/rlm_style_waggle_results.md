# Waggle RLM-style Benchmark Results

> **Warning:** This benchmark follows the benchmark families used in the RLM paper,
> but uses deterministic synthetic memory tasks mapped to Waggle's graph/transcript
> environment. It should **not** be compared numerically to the RLM paper until the
> exact public datasets and matching model setup are run.

| Benchmark family | Scale | Method | Score | F1 | Ev. Coverage | Tokens returned | Latency (ms) |
|---|---:|---|---:|---:|---:|---:|---:|
| BrowseComp-Plus-style | 128 | build_context | 1.000 | 1.000 | 1.000 | 193 | 9 |
| BrowseComp-Plus-style | 128 | query_graph | 1.000 | 1.000 | 1.000 | 98 | 1 |
| BrowseComp-Plus-style | 128 | raw_context | 1.000 | 1.000 | 1.000 | 175 | 2 |
| BrowseComp-Plus-style | 512 | build_context | 1.000 | 1.000 | 1.000 | 193 | 8 |
| BrowseComp-Plus-style | 512 | query_graph | 1.000 | 1.000 | 1.000 | 98 | 1 |
| BrowseComp-Plus-style | 512 | raw_context | 1.000 | 1.000 | 1.000 | 175 | 1 |
| BrowseComp-Plus-style | 2048 | build_context | 1.000 | 1.000 | 1.000 | 193 | 8 |
| BrowseComp-Plus-style | 2048 | query_graph | 1.000 | 1.000 | 1.000 | 98 | 1 |
| BrowseComp-Plus-style | 2048 | raw_context | 1.000 | 1.000 | 1.000 | 175 | 1 |
| CodeQA-style | 128 | build_context | 1.000 | 1.000 | 1.000 | 535 | 32 |
| CodeQA-style | 128 | query_graph | 1.000 | 1.000 | 1.000 | 178 | 5 |
| CodeQA-style | 128 | raw_context | 0.000 | 0.500 | 0.500 | 1382 | 3 |
| CodeQA-style | 512 | build_context | 1.000 | 1.000 | 1.000 | 668 | 116 |
| CodeQA-style | 512 | query_graph | 1.000 | 1.000 | 1.000 | 178 | 16 |
| CodeQA-style | 512 | raw_context | 0.000 | 0.500 | 0.500 | 1400 | 8 |
| CodeQA-style | 2048 | build_context | 1.000 | 1.000 | 1.000 | 646 | 483 |
| CodeQA-style | 2048 | query_graph | 1.000 | 1.000 | 1.000 | 150 | 64 |
| CodeQA-style | 2048 | raw_context | 0.000 | 0.500 | 0.500 | 1400 | 37 |
| OOLONG-style | 128 | build_context | 0.513 | 0.513 | 0.345 | 251 | 32 |
| OOLONG-style | 128 | query_graph | 0.242 | 0.242 | 0.138 | 81 | 6 |
| OOLONG-style | 128 | raw_context | 0.885 | 0.885 | 0.793 | 1416 | 5 |
| OOLONG-style | 512 | build_context | 0.224 | 0.224 | 0.126 | 355 | 81 |
| OOLONG-style | 512 | query_graph | 0.035 | 0.035 | 0.018 | 81 | 15 |
| OOLONG-style | 512 | raw_context | 0.403 | 0.403 | 0.252 | 1425 | 8 |
| OOLONG-style | 2048 | build_context | 0.069 | 0.069 | 0.036 | 372 | 266 |
| OOLONG-style | 2048 | query_graph | 0.010 | 0.010 | 0.005 | 81 | 58 |
| OOLONG-style | 2048 | raw_context | 0.000 | 0.000 | 0.000 | 1450 | 31 |
| S-NIAH-style | 128 | build_context | 1.000 | 1.000 | 1.000 | 181 | 21 |
| S-NIAH-style | 128 | query_graph | 1.000 | 1.000 | 1.000 | 93 | 5 |
| S-NIAH-style | 128 | raw_context | 1.000 | 1.000 | 1.000 | 1423 | 3 |
| S-NIAH-style | 512 | build_context | 1.000 | 1.000 | 1.000 | 201 | 78 |
| S-NIAH-style | 512 | query_graph | 1.000 | 1.000 | 1.000 | 93 | 15 |
| S-NIAH-style | 512 | raw_context | 1.000 | 1.000 | 1.000 | 1444 | 8 |
| S-NIAH-style | 2048 | build_context | 1.000 | 1.000 | 1.000 | 202 | 231 |
| S-NIAH-style | 2048 | query_graph | 1.000 | 1.000 | 1.000 | 94 | 50 |
| S-NIAH-style | 2048 | raw_context | 1.000 | 1.000 | 1.000 | 1430 | 32 |

## Token efficiency: build_context vs baselines

| Benchmark family | Scale | Method | Tokens returned | Score |
|---|---:|---|---:|---:|
| BrowseComp-Plus-style | 128 | query_graph | 98 | 1.000 |
| BrowseComp-Plus-style | 128 | raw_context | 175 | 1.000 |
| BrowseComp-Plus-style | 128 | build_context | 193 | 1.000 |
| BrowseComp-Plus-style | 512 | query_graph | 98 | 1.000 |
| BrowseComp-Plus-style | 512 | raw_context | 175 | 1.000 |
| BrowseComp-Plus-style | 512 | build_context | 193 | 1.000 |
| BrowseComp-Plus-style | 2048 | query_graph | 98 | 1.000 |
| BrowseComp-Plus-style | 2048 | raw_context | 175 | 1.000 |
| BrowseComp-Plus-style | 2048 | build_context | 193 | 1.000 |
| CodeQA-style | 128 | query_graph | 178 | 1.000 |
| CodeQA-style | 128 | build_context | 535 | 1.000 |
| CodeQA-style | 128 | raw_context | 1382 | 0.000 |
| CodeQA-style | 512 | query_graph | 178 | 1.000 |
| CodeQA-style | 512 | build_context | 668 | 1.000 |
| CodeQA-style | 512 | raw_context | 1400 | 0.000 |
| CodeQA-style | 2048 | query_graph | 150 | 1.000 |
| CodeQA-style | 2048 | build_context | 646 | 1.000 |
| CodeQA-style | 2048 | raw_context | 1400 | 0.000 |
| OOLONG-style | 128 | query_graph | 81 | 0.242 |
| OOLONG-style | 128 | build_context | 251 | 0.513 |
| OOLONG-style | 128 | raw_context | 1416 | 0.885 |
| OOLONG-style | 512 | query_graph | 81 | 0.035 |
| OOLONG-style | 512 | build_context | 355 | 0.224 |
| OOLONG-style | 512 | raw_context | 1425 | 0.403 |
| OOLONG-style | 2048 | query_graph | 81 | 0.010 |
| OOLONG-style | 2048 | build_context | 372 | 0.069 |
| OOLONG-style | 2048 | raw_context | 1450 | 0.000 |
| S-NIAH-style | 128 | query_graph | 93 | 1.000 |
| S-NIAH-style | 128 | build_context | 181 | 1.000 |
| S-NIAH-style | 128 | raw_context | 1423 | 1.000 |
| S-NIAH-style | 512 | query_graph | 93 | 1.000 |
| S-NIAH-style | 512 | build_context | 201 | 1.000 |
| S-NIAH-style | 512 | raw_context | 1444 | 1.000 |
| S-NIAH-style | 2048 | query_graph | 94 | 1.000 |
| S-NIAH-style | 2048 | build_context | 202 | 1.000 |
| S-NIAH-style | 2048 | raw_context | 1430 | 1.000 |
