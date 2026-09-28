import sys
import argparse
import json
from .tasks.verified_tasks import ALL_VERIFIED_TASKS
from .core.validator import TaskValidator


def list_instances():
    print(f"\n{'Instance ID':<35} {'Repo':<25} {'Version':<10} {'F2P Tests'}")
    print("=" * 85)
    for task in ALL_VERIFIED_TASKS:
        print(f"{task.instance_id:<35} {task.repo:<25} {task.version:<10} {len(task.FAIL_TO_PASS)}")
    print("=" * 85 + "\n")


def validate_all():
    validator = TaskValidator()
    print("\nValidating SWE-bench task instances...")
    all_passed = True
    for task in ALL_VERIFIED_TASKS:
        report = validator.validate_instance(task)
        status = "PASSED" if report.is_valid else "FAILED"
        print(f" -> [{status}] {report.instance_id}")
        if not report.is_valid:
            all_passed = False
            for note in report.notes:
                print(f"      - {note}")

    if all_passed:
        print("\nAll task instances strictly adhere to SWE-bench specification!\n")
    else:
        sys.exit(1)


def export_jsonl(output_file: str):
    with open(output_file, "w") as f:
        for task in ALL_VERIFIED_TASKS:
            f.write(json.dumps(task.to_dict()) + "\n")
    print(f"Successfully exported {len(ALL_VERIFIED_TASKS)} instances to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="SWE-Bench Task Forge: Toolchain for Authoring Benchmark Instances")
    subparsers = parser.add_subparsers(dest="command", help="Subcommand")

    subparsers.add_parser("list", help="List bundled verified instances")
    subparsers.add_parser("validate", help="Validate instances against SWE-bench rules")

    export_parser = subparsers.add_parser("export", help="Export instances to JSONL")
    export_parser.add_argument("--out", default="dataset/swe_bench_verified_custom.jsonl", help="Output JSONL path")

    args = parser.parse_args()

    if args.command == "list":
        list_instances()
    elif args.command == "validate":
        validate_all()
    elif args.command == "export":
        export_jsonl(args.out)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
