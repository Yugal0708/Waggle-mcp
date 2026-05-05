# Waggle RLM-style Benchmark Results

> **Warning:** This benchmark follows the benchmark families used in the RLM paper,
> but uses deterministic synthetic memory tasks mapped to Waggle's graph/transcript
> environment. It should **not** be compared numerically to the RLM paper until the
> exact public datasets and matching model setup are run.

| Benchmark family | Scale | Method | Score | F1 | Ev. Coverage | Tokens returned | Latency (ms) |
|---|---:|---|---:|---:|---:|---:|---:|
| OOLONG-style | 128 | raw_context | 0.885 | 0.885 | 0.793 | 1416 | 5 |
| OOLONG-style | 128 | query_graph | 0.242 | 0.242 | 0.138 | 81 | 6 |
| OOLONG-style | 128 | build_context | 0.513 | 0.513 | 0.345 | 251 | 32 |
| OOLONG-style | 512 | raw_context | 0.403 | 0.403 | 0.252 | 1425 | 8 |
| OOLONG-style | 512 | query_graph | 0.035 | 0.035 | 0.018 | 81 | 15 |
| OOLONG-style | 512 | build_context | 0.224 | 0.224 | 0.126 | 355 | 81 |
| OOLONG-style | 2048 | raw_context | 0.000 | 0.000 | 0.000 | 1450 | 31 |
| OOLONG-style | 2048 | query_graph | 0.010 | 0.010 | 0.005 | 81 | 58 |
| OOLONG-style | 2048 | build_context | 0.069 | 0.069 | 0.036 | 372 | 266 |

## Token efficiency: build_context vs baselines

| Benchmark family | Scale | Method | Tokens returned | Score |
|---|---:|---|---:|---:|
| OOLONG-style | 128 | query_graph | 81 | 0.242 |
| OOLONG-style | 128 | build_context | 251 | 0.513 |
| OOLONG-style | 128 | raw_context | 1416 | 0.885 |
| OOLONG-style | 512 | query_graph | 81 | 0.035 |
| OOLONG-style | 512 | build_context | 355 | 0.224 |
| OOLONG-style | 512 | raw_context | 1425 | 0.403 |
| OOLONG-style | 2048 | query_graph | 81 | 0.010 |
| OOLONG-style | 2048 | build_context | 372 | 0.069 |
| OOLONG-style | 2048 | raw_context | 1450 | 0.000 |
