import pytest
from pydantic import ValidationError

from backend.models.dtos.mapping_badge_dto import (
    MappingBadgeCreateDTO,
    MappingBadgeDTO,
    MappingBadgeListDTO,
    MappingBadgePublicDTO,
    MappingBadgePublicListDTO,
    MappingBadgeUpdateDTO,
    has_valid_requirements,
)


@pytest.mark.anyio
class TestMappingBadgeDTOs:
    def test_has_valid_requirements_valid(self):
        result = has_valid_requirements('{"req1": "value"}')
        assert result == '{"req1": "value"}'

    def test_has_valid_requirements_empty_keys(self):
        with pytest.raises(ValueError, match="needs at least one requirement"):
            has_valid_requirements("{}")

    def test_has_valid_requirements_invalid_json(self):
        with pytest.raises(ValueError, match="invalid json"):
            has_valid_requirements("{invalid}")

    def test_mapping_badge_dto(self):
        data = {
            "id": 1,
            "name": "Badge 1",
            "description": "Desc",
            "imagePath": "/path",
            "requirements": '{"test": 1}',
            "isEnabled": True,
            "isInternal": False,
        }
        dto = MappingBadgeDTO(**data)
        assert dto.id == 1
        assert dto.name == "Badge 1"
        assert dto.image_path == "/path"
        assert dto.is_enabled is True
        assert dto.is_internal is False

    def test_mapping_badge_create_dto(self):
        data = {
            "name": "Badge 1",
            "description": "Desc",
            "imagePath": "/path",
            "requirements": '{"req": 1}',
        }
        dto = MappingBadgeCreateDTO(**data)
        assert dto.name == "Badge 1"
        assert dto.requirements == '{"req": 1}'

    def test_mapping_badge_create_dto_invalid_requirements(self):
        data = {
            "name": "Badge 1",
            "description": "Desc",
            "imagePath": "/path",
            "requirements": "invalid_json",
        }
        with pytest.raises(ValidationError):
            MappingBadgeCreateDTO(**data)

    def test_mapping_badge_update_dto(self):
        data = {
            "id": 1,
            "requirements": '{"test": 2}',
        }
        dto = MappingBadgeUpdateDTO(**data)
        assert dto.id == 1
        assert dto.requirements == '{"test": 2}'

    def test_mapping_badge_list_dto(self):
        data = {
            "badges": [
                {
                    "id": 1,
                    "name": "B1",
                    "description": "D1",
                    "imagePath": None,
                    "requirements": None,
                }
            ]
        }
        dto = MappingBadgeListDTO(**data)
        assert len(dto.badges) == 1
        assert dto.badges[0].id == 1

    def test_mapping_badge_public_list_dto(self):
        data = {
            "badges": [
                {"id": 1, "name": "B1", "description": "D1", "imagePath": None}
            ]
        }
        dto = MappingBadgePublicListDTO(**data)
        assert len(dto.badges) == 1
        assert dto.badges[0].name == "B1"
