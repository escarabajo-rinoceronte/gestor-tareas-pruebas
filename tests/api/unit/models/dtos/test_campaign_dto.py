import pytest
from pydantic import ValidationError

from backend.models.dtos.campaign_dto import (
    CampaignDTO,
    CampaignListDTO,
    CampaignOrganisationDTO,
    CampaignProjectDTO,
    ListCampaignDTO,
    NewCampaignDTO,
    is_existent,
)


@pytest.mark.anyio
class TestCampaignDTOs:
    def test_is_existent_valid(self):
        # Arrange / Act
        result = is_existent("Valid Campaign Name")
        # Assert
        assert result == "Valid Campaign Name"

    def test_is_existent_empty_raises_error(self):
        # Arrange / Act / Assert
        with pytest.raises(ValueError, match="Empty campaign name string"):
            is_existent("   ")

    def test_new_campaign_dto_valid(self):
        # Arrange
        data = {
            "name": "Test Campaign",
            "logo": "https://example.com/logo.png",
            "url": "https://example.com",
            "description": "Test Description",
            "organisations": [1, 2],
        }

        # Act
        dto = NewCampaignDTO(**data)

        # Assert
        assert dto.name == "Test Campaign"
        assert dto.logo == "https://example.com/logo.png"
        assert dto.url == "https://example.com"
        assert dto.description == "Test Description"
        assert dto.organisations == [1, 2]

    def test_new_campaign_dto_invalid_name(self):
        # Arrange
        data = {"name": "   "}

        # Act / Assert
        with pytest.raises(ValidationError):
            NewCampaignDTO(**data)

    def test_campaign_dto(self):
        # Arrange
        data = {
            "id": 1,
            "name": "Campaign 1",
            "organisations": [],
        }

        # Act
        dto = CampaignDTO(**data)

        # Assert
        assert dto.id == 1
        assert dto.name == "Campaign 1"
        assert dto.organisations == []

    def test_campaign_project_dto(self):
        # Arrange
        data = {
            "project_id": 100,
            "campaign_id": 10,
        }

        # Act
        dto = CampaignProjectDTO(**data)

        # Assert
        assert dto.project_id == 100
        assert dto.campaign_id == 10

    def test_campaign_organisation_dto(self):
        # Arrange
        data = {
            "organisation_id": 5,
            "campaign_id": 10,
        }

        # Act
        dto = CampaignOrganisationDTO(**data)

        # Assert
        assert dto.organisation_id == 5
        assert dto.campaign_id == 10

    def test_list_campaign_dto(self):
        # Arrange
        data = {
            "id": 1,
            "name": "Campaign 1",
        }

        # Act
        dto = ListCampaignDTO(**data)

        # Assert
        assert dto.id == 1
        assert dto.name == "Campaign 1"

    def test_campaign_list_dto(self):
        # Arrange
        dto = CampaignListDTO()

        # Assert
        assert dto.campaigns == []

        # Act
        dto.campaigns.append(ListCampaignDTO(id=1, name="Campaign 1"))

        # Assert
        assert len(dto.campaigns) == 1
        assert dto.campaigns[0].id == 1
