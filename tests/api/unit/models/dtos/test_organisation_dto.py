import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from backend.models.dtos.organisation_dto import (
    ListOrganisationsDTO,
    NewOrganisationDTO,
    OrganisationDTO,
    OrganisationManagerDTO,
    OrganisationTeamsDTO,
    UpdateOrganisationDTO,
    is_known_organisation_type,
)


@pytest.mark.anyio
class TestOrganisationDTOs:
    def test_is_known_organisation_type_valid(self):
        # Should not raise any error
        result = is_known_organisation_type("free")
        assert result is None

    def test_is_known_organisation_type_invalid(self):
        with pytest.raises(HTTPException) as excinfo:
            is_known_organisation_type("invalid_type")
        assert excinfo.value.status_code == 500  # Default HTTP exception status or whatever is thrown
        assert "Unknown organisationType" in str(excinfo.value.detail)

    def test_organisation_manager_dto(self):
        data = {"username": "manager1", "pictureUrl": "http://pic"}
        dto = OrganisationManagerDTO(**data)
        assert dto.username == "manager1"
        assert dto.picture_url == "http://pic"

    def test_organisation_teams_dto(self):
        data = {
            "teamId": 1,
            "name": "Team A",
            "description": "Desc",
            "joinMethod": "ANY",
            "visibility": "PUBLIC",
            "members": [{"username": "user1"}],
        }
        dto = OrganisationTeamsDTO(**data)
        assert dto.team_id == 1
        assert dto.name == "Team A"
        assert dto.join_method == "ANY"
        assert len(dto.members) == 1

    def test_organisation_dto(self):
        data = {
            "organisationId": 1,
            "name": "Org A",
            "isManager": True,
            "projects": ["proj1"],
            "teams": [],
            "type": "FREE",
            "subscriptionTier": 1,
        }
        dto = OrganisationDTO(**data)
        assert dto.organisation_id == 1
        assert dto.is_manager is True
        assert dto.type == "FREE"

    def test_organisation_dto_invalid_type(self):
        data = {
            "name": "Org A",
            "teams": [],
            "type": "INVALID",
        }
        with pytest.raises(ValidationError):
            OrganisationDTO(**data)

    def test_list_organisations_dto(self):
        dto = ListOrganisationsDTO()
        assert dto.organisations == []

    def test_new_organisation_dto(self):
        data = {
            "managers": ["user1"],
            "name": "New Org",
            "type": "discounted",
        }
        dto = NewOrganisationDTO(**data)
        assert dto.name == "New Org"
        assert dto.type == "discounted"

    def test_new_organisation_dto_invalid_type(self):
        data = {
            "managers": ["user1"],
            "name": "New Org",
            "type": "INVALID",
        }
        with pytest.raises(ValidationError) as excinfo:
            NewOrganisationDTO(**data)
        assert "Unknown organisationType" in str(excinfo.value)

    def test_update_organisation_dto(self):
        data = {
            "managers": ["user1"],
            "name": "Update Org",
            "type": "full_fee",
            "teams": [],
        }
        dto = UpdateOrganisationDTO(**data)
        assert dto.name == "Update Org"
        assert dto.type == "full_fee"

    def test_update_organisation_dto_invalid_type(self):
        data = {
            "managers": [],
            "teams": [],
            "type": "INVALID",
        }
        with pytest.raises(ValidationError):
            UpdateOrganisationDTO(**data)
