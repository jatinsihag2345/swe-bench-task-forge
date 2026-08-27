from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import json


@dataclass
class SWEBenchTaskInstance:
    """
    Standard schema for a SWE-bench task instance, adhering strictly to
    the official Princeton NLP SWE-bench evaluation benchmark format.
    """
    instance_id: str
    repo: str
    base_commit: str
    problem_statement: str
    patch: str
    test_patch: str
    version: str
    environment_setup_commit: str
    FAIL_TO_PASS: List[str] = field(default_factory=list)
    PASS_TO_PASS: List[str] = field(default_factory=list)
    hints_text: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SWEBenchTaskInstance":
        return cls(
            instance_id=data["instance_id"],
            repo=data["repo"],
            base_commit=data["base_commit"],
            problem_statement=data["problem_statement"],
            patch=data["patch"],
            test_patch=data["test_patch"],
            version=data.get("version", "1.0"),
            environment_setup_commit=data.get("environment_setup_commit", data["base_commit"]),
            FAIL_TO_PASS=data.get("FAIL_TO_PASS", []),
            PASS_TO_PASS=data.get("PASS_TO_PASS", []),
            hints_text=data.get("hints_text"),
            created_at=data.get("created_at")
        )


@dataclass
class TaskValidationReport:
    instance_id: str
    is_valid: bool
    fail_to_pass_verified: bool
    pass_to_pass_verified: bool
    gold_patch_verified: bool
    notes: List[str] = field(default_factory=list)
