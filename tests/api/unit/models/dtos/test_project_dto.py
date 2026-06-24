import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from backend.models.dtos.project_dto import (
    CustomEditorDTO,
    DraftProjectDTO,
    PMDashboardDTO,
    ProjectComment,
    ProjectCommentsDTO,
    ProjectContribDTO,
    ProjectContribsDTO,
    ProjectDTO,
    ProjectFavoriteDTO,
    ProjectFavoritesDTO,
    ProjectInfoDTO,
    ProjectSearchBBoxDTO,
    ProjectSearchDTO,
    ProjectStatsDTO,
    ProjectSummary,
    ProjectTaskAnnotationsDTO,
    ProjectUserStatsDTO,
    is_known_editor,
    is_known_mapping_permission,
    is_known_mapping_type,
    is_known_project_difficulty,
    is_known_project_priority,
    is_known_project_status,
    is_known_task_creation_mode,
    is_known_validation_permission,
)


@pytest.mark.anyio
class TestProjectDTOValidators:
    def test_is_known_project_status_valid(self):
        assert is_known_project_status("PUBLISHED") == "PUBLISHED"

    def test_is_known_project_status_invalid(self):
        with pytest.raises(HTTPException):
            is_known_project_status("INVALID")

    def test_is_known_project_priority_valid(self):
        assert is_known_project_priority("HIGH") == "HIGH"

    def test_is_known_project_priority_invalid(self):
        with pytest.raises(HTTPException):
            is_known_project_priority("INVALID")

    def test_is_known_mapping_type_valid(self):
        assert is_known_mapping_type("ROADS") == "ROADS"

    def test_is_known_mapping_type_invalid(self):
        with pytest.raises(HTTPException):
            is_known_mapping_type("INVALID")

    def test_is_known_editor_valid(self):
        assert is_known_editor("ID") == "ID"

    def test_is_known_editor_invalid(self):
        with pytest.raises(HTTPException):
            is_known_editor("INVALID")

    def test_is_known_task_creation_mode_valid(self):
        assert is_known_task_creation_mode("GRID") == "GRID"

    def test_is_known_task_creation_mode_invalid(self):
        with pytest.raises(HTTPException):
            is_known_task_creation_mode("INVALID")

    def test_is_known_mapping_permission_valid(self):
        assert is_known_mapping_permission("ANY") == "ANY"

    def test_is_known_mapping_permission_invalid(self):
        with pytest.raises(HTTPException):
            is_known_mapping_permission("INVALID")

    def test_is_known_validation_permission_valid(self):
        assert is_known_validation_permission("TEAMS") == "TEAMS"

    def test_is_known_validation_permission_invalid(self):
        with pytest.raises(HTTPException):
            is_known_validation_permission("INVALID")

    def test_is_known_project_difficulty_valid(self):
        assert is_known_project_difficulty("EASY,MODERATE") == "EASY,MODERATE"
        assert is_known_project_difficulty("ALL") == "ALL"

    def test_is_known_project_difficulty_invalid(self):
        with pytest.raises(HTTPException):
            is_known_project_difficulty("INVALID")


@pytest.mark.anyio
class TestProjectDTOModels:
    def test_project_info_dto_none_to_empty(self):
        data = {"locale": "en", "description": None, "instructions": None}
        dto = ProjectInfoDTO(**data)
        assert dto.description == ""
        assert dto.instructions == ""
        assert dto.locale == "en"

    def test_draft_project_dto(self):
        data = {
            "projectName": "New Draft",
            "areaOfInterest": {"type": "Polygon"},
        }
        dto = DraftProjectDTO(**data)
        assert dto.project_name == "New Draft"
        assert dto.area_of_interest["type"] == "Polygon"

    def test_project_search_dto_hashing(self):
        dto1 = ProjectSearchDTO(preferred_locale="en", mapping_types=["ROADS"])
        dto2 = ProjectSearchDTO(preferred_locale="en", mapping_types=["ROADS"])
        assert hash(dto1) == hash(dto2)

    def test_project_dto_invalid_status(self):
        data = {
            "projectId": 1,
            "status": "INVALID_STATUS",
            "projectPriority": "LOW",
            "defaultLocale": "en",
            "difficulty": "EASY",
            "mappingPermission": "ANY",
            "mappingPermissionLevelId": 1,
            "validationPermission": "ANY",
            "validationPermissionLevelId": 1,
            "private": False,
            "taskCreationMode": "GRID",
            "mappingEditors": ["ID"],
            "validationEditors": ["ID"],
        }
        with pytest.raises(ValidationError):
            ProjectDTO(**data)

    def test_project_dto_valid(self):
        data = {
            "projectId": 1,
            "status": "PUBLISHED",
            "projectPriority": "LOW",
            "defaultLocale": "en",
            "difficulty": "EASY",
            "mappingPermission": "ANY",
            "mappingPermissionLevelId": 1,
            "validationPermission": "ANY",
            "validationPermissionLevelId": 1,
            "private": False,
            "taskCreationMode": "GRID",
            "mappingEditors": ["ID"],
            "validationEditors": ["ID"],
        }
        dto = ProjectDTO(**data)
        assert dto.project_id == 1
        assert dto.project_status == "PUBLISHED"

    def test_project_search_bbox_dto(self):
        data = {"bbox": [0, 0, 10, 10], "input_srid": 4326}
        dto = ProjectSearchBBoxDTO(**data)
        assert dto.bbox == [0, 0, 10, 10]
        assert dto.input_srid == 4326

    def test_pm_dashboard_dto(self):
        dto = PMDashboardDTO()
        assert dto.draft_projects == []
        assert dto.active_projects == []
        assert dto.archived_projects == []
