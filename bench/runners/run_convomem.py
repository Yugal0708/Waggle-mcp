import argparse
import time
import json
import os
from bench.adapters.waggle_adapter import WaggleAdapter
from bench.datasets.loaders import ConvoMemLoader
from bench.scoring.exact_match import exact_match_score

def main():
    parser = argparse.ArgumentParser(description="Run ConvoMem Benchmark")
    parser.add_argument("--category", type=str, default="user_evidence_1", help="ConvoMem split/category to load")
    parser.add_argument("--limit", type=int, default=100, help="Number of examples to evaluate")
    parser.add_argument("--output", type=str, default="bench/outputs/convomem_results.jsonl", help="Output JSONL path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    adapter = WaggleAdapter()
    loader = ConvoMemLoader(subset=args.category)

    total = 0
    correct = 0
    total_latency = 0.0

    print(f"Starting ConvoMem evaluation on category: {args.category}")
    with open(args.output, "w") as f:
        for idx, item in enumerate(loader.load(limit=args.limit)):
            adapter.reset()
            
            # ConvoMem format often has 'messages' or 'context' or it might be raw HuggingFace records
            # We'll adapt it dynamically if possible
            messages = item.get("messages", [])
            if not messages and "context" in item:
                messages = item["context"]
            
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                adapter.ingest_message(role, content)

            question = item.get("question", "What is the answer?")
            gold_answer = item.get("answer", "")
            if not gold_answer and "answers" in item:
                gold_answer = item["answers"][0]

            # Measure latency
            start_time = time.time()
            try:
                prediction = adapter.answer(question)
                error_msg = None
            except Exception as e:
                prediction = ""
                error_msg = str(e)
            end_time = time.time()

            latency_ms = (end_time - start_time) * 1000
            total_latency += latency_ms

            score = exact_match_score(prediction, gold_answer)
            correct += score
            total += 1

            result = {
                "benchmark_name": "ConvoMem",
                "split": args.category,
                "sample_id": item.get("id", str(idx)),
                "question": question,
                "gold_answer": gold_answer,
                "predicted_answer": prediction,
                "exact_match": score,
                "latency_ms": latency_ms,
                "error": error_msg
            }
            f.write(json.dumps(result) + "\n")
            print(f"Processed {total} items. Current Acc: {correct/total:.2%}")

    avg_latency = total_latency / total if total > 0 else 0
    accuracy = correct / total if total > 0 else 0
    print("-" * 40)
    print("CONVOMEM EVALUATION COMPLETE")
    print(f"Total Examples: {total}")
    print(f"Accuracy (Exact Match): {accuracy:.2%}")
    print(f"Avg Latency: {avg_latency:.2f} ms")
    
    # Save summary
    summary = {"benchmark": "ConvoMem", "category": args.category, "total": total, "accuracy": accuracy, "avg_latency_ms": avg_latency}
    with open("bench/outputs/summary.csv", "a") as f:
        if os.stat("bench/outputs/summary.csv").st_size == 0:
            f.write("benchmark,category,total,accuracy,avg_latency_ms\n")
        f.write(f"{summary['benchmark']},{summary['category']},{summary['total']},{summary['accuracy']},{summary['avg_latency_ms']}\n")

if __name__ == "__main__":
    main()
