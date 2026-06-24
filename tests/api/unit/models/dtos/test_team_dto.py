import pytest
from fastapi import HTTPException

from backend.models.dtos.team_dto import (
    ListTeamsDTO,
    NewTeamDTO,
    ProjectTeamDTO,
    ProjectTeamPairDTO,
    ProjectTeamPairDTOList,
    TeamDetailsDTO,
    TeamDTO,
    TeamMembersDTO,
    TeamProjectDTO,
    TeamSearchDTO,
    TeamsListDTO,
    UpdateTeamDTO,
    validate_team_join_method,
    validate_team_member_function,
    validate_team_visibility,
)


@pytest.mark.anyio
class TestTeamDTOs:
    def test_validate_team_visibility_valid(self):
        assert validate_team_visibility("PUBLIC") == "PUBLIC"

    def test_validate_team_visibility_invalid(self):
        with pytest.raises(HTTPException):
            validate_team_visibility("INVALID")

    def test_validate_team_join_method_valid(self):
        assert validate_team_join_method("ANY") == "ANY"

    def test_validate_team_join_method_invalid(self):
        with pytest.raises(HTTPException):
            validate_team_join_method("INVALID")

    def test_validate_team_member_function_valid(self):
        assert validate_team_member_function("MEMBER") == "MEMBER"

    def test_validate_team_member_function_invalid(self):
        with pytest.raises(HTTPException):
            validate_team_member_function("INVALID")

    def test_team_members_dto(self):
        data = {
            "username": "user1",
            "function": "MEMBER",
            "active": True,
        }
        dto = TeamMembersDTO(**data)
        assert dto.username == "user1"
        assert dto.function == "MEMBER"
        assert dto.active is True

    def test_team_project_dto(self):
        data = {
            "project_name": "Proj 1",
            "project_id": 1,
            "role": "MAPPER",
        }
        dto = TeamProjectDTO(**data)
        assert dto.project_name == "Proj 1"
        assert dto.project_id == 1
        assert dto.role == "MAPPER"

    def test_project_team_dto(self):
        data = {"teamId": 1, "name": "Team 1", "role": "VALIDATOR"}
        dto = ProjectTeamDTO(**data)
        assert dto.team_id == 1
        assert dto.team_name == "Team 1"

    def test_team_details_dto(self):
        data = {
            "organisation_id": 1,
            "organisation": "Org 1",
            "name": "Team A",
            "joinMethod": "ANY",
            "visibility": "PUBLIC",
        }
        dto = TeamDetailsDTO(**data)
        assert dto.organisation_id == 1
        assert dto.name == "Team A"

    def test_team_dto(self):
        data = {
            "teamId": 1,
            "organisationId": 2,
            "organisation": "Org 2",
            "name": "Team B",
            "joinMethod": "BY_INVITE",
            "visibility": "PRIVATE",
        }
        dto = TeamDTO(**data)
        assert dto.team_id == 1
        assert dto.visibility == "PRIVATE"

    def test_teams_list_dto(self):
        dto = TeamsListDTO()
        assert dto.teams == []

    def test_list_teams_dto(self):
        dto = ListTeamsDTO()
        assert dto.teams == []

    def test_new_team_dto(self):
        data = {
            "creator": 1.0,
            "organisation_id": 1,
            "name": "New Team",
            "joinMethod": "ANY",
            "visibility": "PUBLIC",
        }
        dto = NewTeamDTO(**data)
        assert dto.name == "New Team"

    def test_update_team_dto(self):
        data = {
            "team_id": 1,
            "name": "Updated Team",
            "joinMethod": "ANY",
            "visibility": "PUBLIC",
        }
        dto = UpdateTeamDTO(**data)
        assert dto.name == "Updated Team"

    def test_team_search_dto(self):
        data = {
            "userId": 1,
            "team_name": "Search Team",
        }
        dto = TeamSearchDTO(**data)
        assert dto.user_id == 1
        assert dto.team_name == "Search Team"

    def test_project_team_pair_dto(self):
        data = {"project_id": 1, "team_id": 2}
        dto = ProjectTeamPairDTO(**data)
        assert dto.project_id == 1
        assert dto.team_id == 2

    def test_project_team_pair_dto_list(self):
        data = {"items": [{"project_id": 1, "team_id": 2}]}
        dto = ProjectTeamPairDTOList(**data)
        assert len(dto.items) == 1
