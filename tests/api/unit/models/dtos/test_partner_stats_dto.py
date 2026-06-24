import pytest
import pandas as pd
from io import StringIO

from backend.models.dtos.partner_stats_dto import (
    AreaSwipedByProjectTypeDTO,
    ContributionTimeByDateDTO,
    ContributionsByDateDTO,
    ContributionsByProjectTypeDTO,
    FilteredPartnerStatsDTO,
    GeoContributionsDTO,
    GeojsonDTO,
    GroupedPartnerStatsDTO,
    OrganizationContributionsDTO,
    UserContributionsDTO,
    UserGroupMemberDTO,
)


@pytest.mark.anyio
class TestPartnerStatsDTOs:
    def test_user_group_member_dto(self):
        data = {
            "userId": "u1",
            "username": "user1",
            "isActive": True,
            "totalMappingProjects": 5,
            "totalcontributionTime": 3600,
            "totalcontributions": 100,
        }
        dto = UserGroupMemberDTO(**data)
        assert dto.user_id == "u1"
        assert dto.is_active is True

    def test_organization_contributions_dto(self):
        data = {
            "organizationName": "Org1",
            "totalcontributions": 50,
        }
        dto = OrganizationContributionsDTO(**data)
        assert dto.organization_name == "Org1"
        assert dto.total_contributions == 50

    def test_user_contributions_dto(self):
        data = {
            "username": "user1",
            "totalcontributions": 10,
        }
        dto = UserContributionsDTO(**data)
        assert dto.username == "user1"

    def test_geo_contributions_dto(self):
        geojson_data = {
            "type": "Point",
            "coordinates": [10.0, 20.0],
        }
        data = {
            "geojson": geojson_data,
            "totalcontributions": 5,
        }
        dto = GeoContributionsDTO(**data)
        assert dto.geojson.type == "Point"
        assert dto.geojson.coordinates == [10.0, 20.0]

    def test_contributions_by_date_dto(self):
        data = {
            "taskDate": "2023-01-01",
            "totalcontributions": 15,
        }
        dto = ContributionsByDateDTO(**data)
        assert dto.task_date == "2023-01-01"

    def test_contribution_time_by_date_dto(self):
        data = {
            "date": "2023-01-01",
            "totalcontributionTime": 3600,
        }
        dto = ContributionTimeByDateDTO(**data)
        assert dto.date == "2023-01-01"

    def test_contributions_by_project_type_dto(self):
        data = {
            "projectType": "type1",
            "projectTypeDisplay": "Type 1",
            "totalcontributions": 20,
        }
        dto = ContributionsByProjectTypeDTO(**data)
        assert dto.project_type == "type1"

    def test_area_swiped_by_project_type_dto(self):
        data = {
            "totalArea": 100.5,
            "projectType": "type1",
            "projectTypeDisplay": "Type 1",
        }
        dto = AreaSwipedByProjectTypeDTO(**data)
        assert dto.total_area == 100.5

    def test_grouped_partner_stats_dto_to_csv(self):
        # Arrange
        members = [
            {
                "id": "1",
                "userId": "u1",
                "username": "user1",
                "isActive": True,
                "totalMappingProjects": 5,
                "totalcontributionTime": 3600,
                "totalcontributions": 100,
            }
        ]
        data = {
            "provider": "prov1",
            "members": members,
        }
        dto = GroupedPartnerStatsDTO(**data)

        # Act
        csv_data = dto.to_csv()

        # Assert
        df = pd.read_csv(StringIO(csv_data))
        assert "id" not in df.columns
        assert "userId" in df.columns
        assert "totalSwipeTimeInSeconds" in df.columns
        assert "totalSwipes" in df.columns
        assert df["totalSwipeTimeInSeconds"].iloc[0] == 3600
        assert df["totalSwipes"].iloc[0] == 100

    def test_filtered_partner_stats_dto(self):
        data = {
            "provider": "prov1",
            "fromDate": "2023-01-01",
            "toDate": "2023-12-31",
            "contributionsByUser": [{"username": "user1", "totalcontributions": 10}],
        }
        dto = FilteredPartnerStatsDTO(**data)
        assert dto.provider == "prov1"
        assert len(dto.contributions_by_user) == 1
