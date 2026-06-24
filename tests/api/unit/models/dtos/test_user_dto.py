import pytest
from pydantic import ValidationError

from backend.models.dtos.user_dto import (
    AuthUserDTO,
    ListedUser,
    MappedProject,
    ProjectParticipantUser,
    UserCountriesContributed,
    UserCountryContributed,
    UserContributionDTO,
    UserDTO,
    UserFilterDTO,
    UserMappedProjectsDTO,
    UserNextLevelDTO,
    UserOSMDTO,
    UserRegisterEmailDTO,
    UserSearchDTO,
    UserSearchQuery,
    UserStatsDTO,
    UserTaskDTOs,
    is_known_role,
)


@pytest.mark.anyio
class TestUserDTOs:
    def test_is_known_role_valid(self):
        # Should not raise exception
        is_known_role("ADMIN,MAPPER")

    def test_is_known_role_invalid(self):
        with pytest.raises(ValueError):
            is_known_role("INVALID")

    def test_user_dto(self):
        data = {
            "id": 1,
            "username": "user1",
            "role": "MAPPER",
            "isExpert": True,
            "gender": "MALE",
        }
        dto = UserDTO(**data)
        assert dto.username == "user1"
        assert dto.gender == "MALE"

    def test_user_dto_validate_self_description(self):
        data = {
            "id": 1,
            "username": "user1",
            "isExpert": True,
            "gender": "SELF_DESCRIBE",
        }
        # Assuming Pydantic will call validate_self_description during initialization or manually
        dto = UserDTO(**data)
        with pytest.raises(ValueError):
            dto.validate_self_description(dto.model_dump(), dto.self_description_gender)

    def test_user_country_contributed(self):
        data = {"name": "Peru", "mapped": 10, "validated": 5, "total": 15}
        dto = UserCountryContributed(**data)
        assert dto.name == "Peru"

    def test_user_countries_contributed(self):
        data = {
            "countries": [{"name": "Peru", "mapped": 10, "validated": 5, "total": 15}],
            "total": 1,
        }
        dto = UserCountriesContributed(**data)
        assert dto.total == 1
        assert len(dto.countries_contributed) == 1

    def test_user_contribution_dto(self):
        data = {"date": "2023-01-01T00:00:00Z", "count": 10}
        dto = UserContributionDTO(**data)
        assert dto.count == 10

    def test_user_stats_dto(self):
        data = {
            "totalTimeSpent": 3600,
            "timeSpentMapping": 1800,
            "timeSpentValidating": 1800,
            "projectsMapped": 5,
            "tasksMapped": 10,
            "tasksValidated": 5,
            "tasksInvalidated": 1,
            "tasksInvalidatedByOthers": 2,
            "tasksValidatedByOthers": 3,
        }
        dto = UserStatsDTO(**data)
        assert dto.total_time_spent == 3600

    def test_user_osm_dto(self):
        data = {"accountCreated": "2020-01-01", "changesetCount": 100}
        dto = UserOSMDTO(**data)
        assert dto.changeset_count == 100

    def test_mapped_project(self):
        data = {"projectId": 1, "name": "Proj", "tasksMapped": 10, "tasksValidated": 5}
        dto = MappedProject(**data)
        assert dto.project_id == 1

    def test_user_mapped_projects_dto(self):
        data = {"mappedProjects": [{"projectId": 1}]}
        dto = UserMappedProjectsDTO(**data)
        assert len(dto.mapped_projects) == 1

    def test_user_search_query(self):
        data = {"username": " user ", "role": "MAPPER", "voter_id": 1}
        dto = UserSearchQuery(**data)
        assert dto.username == "user"
        assert dto.role == "MAPPER"

    def test_user_search_query_invalid_role(self):
        data = {"username": "user", "role": "INVALID", "voter_id": 1}
        with pytest.raises(ValidationError):
            UserSearchQuery(**data)

    def test_user_search_query_hashing(self):
        dto1 = UserSearchQuery(username="user", role="MAPPER", voter_id=1)
        dto2 = UserSearchQuery(username="user", role="MAPPER", voter_id=1)
        assert hash(dto1) == hash(dto2)

    def test_listed_user(self):
        data = {"username": "user1", "mappingLevel": "ADVANCED"}
        dto = ListedUser(**data)
        assert dto.username == "user1"

    def test_user_register_email_dto(self):
        data = {"email": "test@test.com", "success": True}
        dto = UserRegisterEmailDTO(**data)
        assert dto.email == "test@test.com"

    def test_project_participant_user(self):
        data = {"username": "user1", "projectId": 1, "isParticipant": True}
        dto = ProjectParticipantUser(**data)
        assert dto.username == "user1"

    def test_user_search_dto(self):
        dto = UserSearchDTO()
        assert dto.users == []

    def test_user_filter_dto(self):
        dto = UserFilterDTO()
        assert dto.users == []
        assert dto.usernames == []

    def test_user_task_dtos(self):
        dto = UserTaskDTOs()
        assert dto.user_tasks == []

    def test_user_next_level_dto(self):
        data = {
            "nextLevel": "ADVANCED",
            "aggregatedProgress": 50.0,
            "aggregatedGoal": 100.0,
            "metrics": ["time", "projects"],
        }
        dto = UserNextLevelDTO(**data)
        assert dto.next_level == "ADVANCED"

    def test_auth_user_dto(self):
        data = {"id": 1}
        dto = AuthUserDTO(**data)
        assert dto.id == 1
