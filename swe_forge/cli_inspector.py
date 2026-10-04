import json
import argparse
from typing import Dict, Any, List


class TaskInstanceInspector:
    """
    CLI utility to inspect, format, and audit SWE-bench JSONL task instances.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.instances: List[Dict[str, Any]] = []

    def load_instances(self) -> int:
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    self.instances.append(json.loads(line))
        return len(self.instances)

    def print_summary(self) -> None:
        print(f"\n--- SWE-bench Dataset Summary: {self.filepath} ---")
        print(f"Total Instances Loaded: {len(self.instances)}")
        for idx, inst in enumerate(self.instances, start=1):
            instance_id = inst.get("instance_id", "UNKNOWN")
            repo = inst.get("repo", "UNKNOWN")
            base_commit = inst.get("base_commit", "N/A")[:8]
            hints_len = len(inst.get("hints_text", ""))
            print(f"  [{idx:02d}] {instance_id:<30} | Repo: {repo:<20} | Base: {base_commit} | Hints: {hints_len} chars")


def main():
    parser = argparse.ArgumentParser(description="SWE-bench Instance CLI Inspector")
    parser.add_argument("file", help="Path to JSONL task instances file")
    args = parser.parse_args()

    inspector = TaskInstanceInspector(args.file)
    count = inspector.load_instances()
    inspector.print_summary()


if __name__ == "__main__":
    main()
