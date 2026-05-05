# Waggle RLM-style Benchmark Results

> **Warning:** This benchmark follows the benchmark families used in the RLM paper,
> but uses deterministic synthetic memory tasks mapped to Waggle's graph/transcript
> environment. It should **not** be compared numerically to the RLM paper until the
> exact public datasets and matching model setup are run.

| Benchmark family | Scale | Method | Score | F1 | Ev. Coverage | Tokens returned | Latency (ms) |
|---|---:|---|---:|---:|---:|---:|---:|
| CodeQA-style | 128 | raw_context | 0.000 | 0.500 | 0.500 | 1382 | 3 |
| CodeQA-style | 128 | query_graph | 1.000 | 1.000 | 1.000 | 178 | 5 |
| CodeQA-style | 128 | build_context | 1.000 | 1.000 | 1.000 | 535 | 32 |
| CodeQA-style | 512 | raw_context | 0.000 | 0.500 | 0.500 | 1400 | 8 |
| CodeQA-style | 512 | query_graph | 1.000 | 1.000 | 1.000 | 178 | 16 |
| CodeQA-style | 512 | build_context | 1.000 | 1.000 | 1.000 | 668 | 116 |
| CodeQA-style | 2048 | raw_context | 0.000 | 0.500 | 0.500 | 1400 | 37 |
| CodeQA-style | 2048 | query_graph | 1.000 | 1.000 | 1.000 | 150 | 64 |
| CodeQA-style | 2048 | build_context | 1.000 | 1.000 | 1.000 | 646 | 483 |

## Token efficiency: build_context vs baselines

| Benchmark family | Scale | Method | Tokens returned | Score |
|---|---:|---|---:|---:|
| CodeQA-style | 128 | query_graph | 178 | 1.000 |
| CodeQA-style | 128 | build_context | 535 | 1.000 |
| CodeQA-style | 128 | raw_context | 1382 | 0.000 |
| CodeQA-style | 512 | query_graph | 178 | 1.000 |
| CodeQA-style | 512 | build_context | 668 | 1.000 |
| CodeQA-style | 512 | raw_context | 1400 | 0.000 |
| CodeQA-style | 2048 | query_graph | 150 | 1.000 |
| CodeQA-style | 2048 | build_context | 646 | 1.000 |
| CodeQA-style | 2048 | raw_context | 1400 | 0.000 |
