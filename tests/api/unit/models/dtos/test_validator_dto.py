import pytest
from datetime import datetime
from pydantic import ValidationError

from backend.models.dtos.validator_dto import (
    ExtendedStringType,
    InvalidatedTask,
    InvalidatedTasks,
    LockForValidationDTO,
    MappedTasks,
    MappedTasksByUser,
    ResetValidatingTask,
    RevertUserTasksDTO,
    StopValidationDTO,
    UnlockAfterValidationDTO,
    ValidatedTask,
    ValidationMappingIssue,
    is_valid_revert_status,
    is_valid_validated_status,
)
from backend.models.dtos.stats_dto import Pagination


@pytest.mark.anyio
class TestValidatorDTOs:
    def test_extended_string_type(self):
        ext_str = ExtendedStringType(converters=[str.upper, lambda x: x + " TEST"])
        res = ext_str.convert("hello")
        assert res == "HELLO TEST"

    def test_is_valid_validated_status_valid(self):
        # Should not raise exception
        is_valid_validated_status("VALIDATED")
        is_valid_validated_status("MAPPED")

    def test_is_valid_validated_status_invalid(self):
        with pytest.raises(ValidationError):
            is_valid_validated_status("INVALID_STATUS")

        with pytest.raises(ValidationError):
            # BADIMAGERY is not allowed for validated status
            is_valid_validated_status("BADIMAGERY")

    def test_is_valid_revert_status_valid(self):
        is_valid_revert_status("BADIMAGERY")
        is_valid_revert_status("VALIDATED")

    def test_is_valid_revert_status_invalid(self):
        with pytest.raises(ValidationError):
            is_valid_revert_status("INVALID_STATUS")

        with pytest.raises(ValidationError):
            # MAPPED is not allowed for revert status
            is_valid_revert_status("MAPPED")

    def test_lock_for_validation_dto(self):
        data = {"project_id": 1, "taskIds": [1, 2], "user_id": 3}
        dto = LockForValidationDTO(**data)
        assert dto.project_id == 1
        assert dto.task_ids == [1, 2]

    def test_validation_mapping_issue(self):
        data = {"mappingIssueCategoryId": 1, "issue": "overlap", "count": 2}
        dto = ValidationMappingIssue(**data)
        assert dto.mapping_issue_category_id == 1
        assert dto.issue == "overlap"

    def test_validated_task(self):
        data = {"taskId": 1, "status": "VALIDATED"}
        dto = ValidatedTask(**data)
        assert dto.task_id == 1
        assert dto.status == "VALIDATED"

    def test_reset_validating_task(self):
        data = {"taskId": 1, "comment": "reset"}
        dto = ResetValidatingTask(**data)
        assert dto.task_id == 1
        assert dto.comment == "reset"

    def test_unlock_after_validation_dto(self):
        data = {
            "project_id": 1,
            "validatedTasks": [{"taskId": 1, "status": "VALIDATED"}],
            "user_id": 2,
        }
        dto = UnlockAfterValidationDTO(**data)
        assert dto.project_id == 1
        assert len(dto.validated_tasks) == 1

    def test_stop_validation_dto(self):
        data = {"project_id": 1, "resetTasks": [{"taskId": 1}], "user_id": 2}
        dto = StopValidationDTO(**data)
        assert dto.project_id == 1
        assert len(dto.reset_tasks) == 1

    def test_mapped_tasks_by_user(self):
        dt = datetime(2023, 1, 1, 12, 0, 0)
        data = {"username": "user1", "dateRegistered": dt}
        dto = MappedTasksByUser(**data)
        assert dto.username == "user1"

    def test_invalidated_task(self):
        dt = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            "taskId": 1,
            "projectId": 2,
            "projectName": "P2",
            "historyId": 3,
            "closed": False,
            "updatedDate": dt,
        }
        dto = InvalidatedTask(**data)
        assert dto.task_id == 1

    def test_invalidated_tasks(self):
        pag = Pagination(
            hasNext=False,
            hasPrev=False,
            nextNum=None,
            page=1,
            pages=1,
            prevNum=None,
            perPage=10,
            total=1,
        )
        dto = InvalidatedTasks(invalidatedTasks=[], pagination=pag)
        assert dto.invalidated_tasks == []

    def test_mapped_tasks(self):
        dt = datetime(2023, 1, 1, 12, 0, 0)
        data = {"mappedTasks": [{"username": "user1", "dateRegistered": dt}]}
        dto = MappedTasks(**data)
        assert len(dto.mapped_tasks) == 1

    def test_revert_user_tasks_dto_valid(self):
        data = {"project_id": 1, "user_id": 2, "action_by": 3, "action": "VALIDATED"}
        dto = RevertUserTasksDTO(**data)
        assert dto.action == "VALIDATED"

    def test_revert_user_tasks_dto_invalid_action(self):
        data = {"project_id": 1, "user_id": 2, "action_by": 3, "action": "INVALID"}
        with pytest.raises(ValidationError):
            RevertUserTasksDTO(**data)

    def test_revert_user_tasks_dto_invalid_type(self):
        data = {"project_id": 1, "user_id": 2, "action_by": 3, "action": 123}
        with pytest.raises(ValidationError):
            RevertUserTasksDTO(**data)

    def test_revert_user_tasks_dto_wrong_status(self):
        data = {"project_id": 1, "user_id": 2, "action_by": 3, "action": "MAPPED"}
        with pytest.raises(ValidationError):
            RevertUserTasksDTO(**data)
