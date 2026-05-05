# Waggle RLM-style Benchmark Results

> **Warning:** This benchmark follows the benchmark families used in the RLM paper,
> but uses deterministic synthetic memory tasks mapped to Waggle's graph/transcript
> environment. It should **not** be compared numerically to the RLM paper until the
> exact public datasets and matching model setup are run.

| Benchmark family | Scale | Method | Score | F1 | Ev. Coverage | Tokens returned | Latency (ms) |
|---|---:|---|---:|---:|---:|---:|---:|
| BrowseComp-Plus-style | 128 | raw_context | 1.000 | 1.000 | 1.000 | 175 | 2 |
| BrowseComp-Plus-style | 128 | query_graph | 1.000 | 1.000 | 1.000 | 98 | 1 |
| BrowseComp-Plus-style | 128 | build_context | 1.000 | 1.000 | 1.000 | 193 | 9 |
| BrowseComp-Plus-style | 512 | raw_context | 1.000 | 1.000 | 1.000 | 175 | 1 |
| BrowseComp-Plus-style | 512 | query_graph | 1.000 | 1.000 | 1.000 | 98 | 1 |
| BrowseComp-Plus-style | 512 | build_context | 1.000 | 1.000 | 1.000 | 193 | 8 |
| BrowseComp-Plus-style | 2048 | raw_context | 1.000 | 1.000 | 1.000 | 175 | 1 |
| BrowseComp-Plus-style | 2048 | query_graph | 1.000 | 1.000 | 1.000 | 98 | 1 |
| BrowseComp-Plus-style | 2048 | build_context | 1.000 | 1.000 | 1.000 | 193 | 8 |

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
