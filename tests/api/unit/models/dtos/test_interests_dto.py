import pytest
from pydantic import ValidationError

from backend.models.dtos.interests_dto import (
    InterestDTO,
    InterestRateDTO,
    InterestRateListDTO,
    InterestsListDTO,
)


@pytest.mark.anyio
class TestInterestsDTOs:
    def test_interest_dto_valid(self):
        data = {
            "id": 1,
            "name": "Ecology",
            "userSelected": True,
            "countProjects": 10,
            "countUsers": 50,
        }
        dto = InterestDTO(**data)
        assert dto.id == 1
        assert dto.name == "Ecology"
        assert dto.user_selected is True
        assert dto.count_projects == 10
        assert dto.count_users == 50

    def test_interest_dto_invalid_name(self):
        data = {
            "name": "",
        }
        with pytest.raises(ValidationError):
            InterestDTO(**data)

    def test_interest_dto_aliases(self):
        data = {
            "user_selected": False,
            "count_projects": 5,
        }
        # population by name should work because of Config.populate_by_name = True
        dto = InterestDTO(**data)
        assert dto.user_selected is False
        assert dto.count_projects == 5

    def test_interests_list_dto(self):
        dto = InterestsListDTO()
        assert dto.interests == []
        dto.interests.append(InterestDTO(name="Nature"))
        assert len(dto.interests) == 1

    def test_interest_rate_dto(self):
        data = {"name": "Test Interest", "rate": 45.5}
        dto = InterestRateDTO(**data)
        assert dto.name == "Test Interest"
        assert dto.rate == 45.5

    def test_interest_rate_list_dto(self):
        dto = InterestRateListDTO()
        assert dto.rates == []
        dto.rates.append(InterestRateDTO(name="A", rate=10.0))
        assert len(dto.rates) == 1
