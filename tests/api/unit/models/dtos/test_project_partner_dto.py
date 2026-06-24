import pytest
from datetime import datetime
from pydantic import ValidationError

from backend.models.dtos.project_partner_dto import (
    ProjectPartnerAction,
    ProjectPartnershipDTO,
    ProjectPartnershipHistoryDTO,
    ProjectPartnershipUpdateDTO,
    is_known_action,
)


@pytest.mark.anyio
class TestProjectPartnerDTOs:
    def test_is_known_action_valid(self):
        # Should not raise exception
        is_known_action("CREATE")

    def test_is_known_action_invalid(self):
        with pytest.raises(ValidationError):
            is_known_action("INVALID")

    def test_project_partnership_dto(self):
        dt = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            "id": 1,
            "projectId": 2,
            "partnerId": 3,
            "startedOn": dt,
        }
        dto = ProjectPartnershipDTO(**data)
        assert dto.id == 1
        assert dto.project_id == 2
        assert dto.partner_id == 3
        assert dto.started_on == dt

    def test_project_partnership_update_dto(self):
        dt = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            "startedOn": dt,
            "endedOn": dt,
        }
        dto = ProjectPartnershipUpdateDTO(**data)
        assert dto.started_on == dt
        assert dto.ended_on == dt

    def test_project_partnership_history_dto(self):
        dt = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            "id": 1,
            "partnershipId": 2,
            "projectId": 3,
            "partnerId": 4,
            "action": "CREATE",
            "actionDate": dt,
        }
        dto = ProjectPartnershipHistoryDTO(**data)
        assert dto.id == 1
        assert dto.action == "CREATE"
        assert dto.action_date == dt
