from __future__ import annotations

import argparse
import subprocess
import sys


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Run all local memory benchmark harnesses.")


def main() -> int:
    build_arg_parser().parse_args()
    print("====================================")
    print("   RUNNING ALL MEMORY BENCHMARKS   ")
    print("====================================")

    convomem_categories: list[str] = []
    for category in convomem_categories:
        print(f"\n---> Running ConvoMem: {category}")
        subprocess.run(
            [sys.executable, "-m", "bench.runners.run_convomem", "--category", category, "--limit", "10"],
            check=False,
        )

    print("\nAll complete. Check bench/outputs/summary.csv for results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
