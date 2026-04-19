from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Dict, Iterator

from datasets import load_dataset


class DatasetLoadError(RuntimeError):
    """Raised when an evaluation dataset is unavailable or malformed."""


class ConvoMemLoader:
    def __init__(self, subset: str = "user_evidence_1"):
        self.subset = subset

    def load(self, limit: int | None = None) -> Iterator[Dict[str, Any]]:
        try:
            print("Loading Salesforce/ConvoMem slice...")
            conf = self.subset
            if "user_evidence" in conf:
                conf = "category_1_basic_facts"
            elif "changing_evidence" in conf:
                conf = "category_2_changing_facts"
            elif "preference_evidence" in conf:
                conf = "category_6_preferences"

            dset = load_dataset("Salesforce/ConvoMem", name=conf, split="train", streaming=True)
            count = 0
            for item in dset:
                yield item
                count += 1
                if limit and count >= limit:
                    break
        except Exception as exc:
            print(f"Error loading hf dataset: {exc}. Falling back to downloading batch JSON directly.")
            urls = [
                "https://raw.githubusercontent.com/SalesforceAIResearch/ConvoMem/main/core_benchmark/pre_mixed_testcases/user_evidence/1_evidence/batched/test_cases_batch_0.json",
                "https://raw.githubusercontent.com/SalesforceAIResearch/ConvoMem/main/core_benchmark/pre_mixed_testcases/changing_evidence/1_evidence/batched/test_cases_batch_0.json",
                "https://raw.githubusercontent.com/SalesforceAIResearch/ConvoMem/main/core_benchmark/pre_mixed_testcases/preference_evidence/1_evidence/batched/test_cases_batch_0.json",
            ]
            count = 0
            for url in urls:
                try:
                    req = urllib.request.urlopen(url)
                    data = json.loads(req.read().decode("utf-8"))
                    for test_case in data:
                        yield test_case
                        count += 1
                        if limit and count >= limit:
                            return
                except Exception as download_exc:
                    print(f"Could not download {url}: {download_exc}")
