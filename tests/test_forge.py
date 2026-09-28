from swe_forge.tasks.verified_tasks import ALL_VERIFIED_TASKS
from swe_forge.core.validator import TaskValidator
from swe_forge.core.task_instance import SWEBenchTaskInstance


def test_task_instance_schema():
    assert len(ALL_VERIFIED_TASKS) >= 3
    for task in ALL_VERIFIED_TASKS:
        d = task.to_dict()
        assert "instance_id" in d
        assert "problem_statement" in d
        assert "patch" in d
        assert "test_patch" in d
        assert len(task.FAIL_TO_PASS) > 0


def test_task_validator_rules():
    validator = TaskValidator()
    for task in ALL_VERIFIED_TASKS:
        report = validator.validate_instance(task)
        assert report.is_valid is True, f"Failed validation for {task.instance_id}: {report.notes}"
