import pytest
from unittest.mock import MagicMock
from backend.api.projects.resources import setup_search_dto

def test_setup_search_dto_basic():
    # Mocking FastAPI Request
    request_mock = MagicMock()
    request_mock.headers.get.return_value = "en"
    request_mock.query_params.get.side_effect = lambda k, d=None: {
        "difficulty": "EASY",
        "action": "map",
        "organisationName": "HOT",
        "organisationId": "1",
        "teamId": "2",
        "campaign": "malaria",
        "orderBy": "priority",
        "country": "Peru",
        "orderByType": "DESC",
        "page": "2",
        "textSearch": "river",
        "omitMapResults": "true",
        "lastUpdatedFrom": "2023-01-01",
        "lastUpdatedTo": "2023-12-31",
        "createdFrom": "2023-01-01",
        "createdTo": "2023-12-31",
        "partnerId": "3",
        "partnershipFrom": "2023-01-01",
        "partnershipTo": "2023-12-31",
        "downloadAsCSV": "true",
        "createdByMe": "true",
        "mappedByMe": "true",
        "favoritedByMe": "true",
        "managedByMe": "true",
        "basedOnMyInterests": "true",
        "mappingTypes": "ROADS,BUILDINGS",
        "mappingTypesExact": "true",
        "projectStatuses": "PUBLISHED,DRAFT",
        "interests": "1,2,3"
    }.get(k, d)
    
    # Mock user
    request_mock.user = MagicMock()
    request_mock.user.display_name = "testuser"
    
    # Run function
    dto = setup_search_dto(request_mock)
    
    # Assertions to increase coverage
    assert dto.preferred_locale == "en"
    assert dto.difficulty == "EASY"
    assert dto.action == "map"
    assert dto.organisation_name == "HOT"
    assert dto.organisation_id == "1"
    assert dto.team_id == "2"
    assert dto.campaign == "malaria"
    assert dto.order_by == "priority"
    assert dto.country == "Peru"
    assert dto.order_by_type == "DESC"
    assert dto.page == 2
    assert dto.text_search == "river"
    assert dto.omit_map_results is True
    assert dto.last_updated_gte == "2023-01-01"
    assert dto.last_updated_lte == "2023-12-31"
    assert dto.created_gte == "2023-01-01"
    assert dto.created_lte == "2023-12-31"
    assert dto.partner_id == "3"
    assert dto.partnership_from == "2023-01-01"
    assert dto.partnership_to == "2023-12-31"
    assert dto.download_as_csv == "true"
    assert dto.created_by == "testuser"
    assert dto.mapped_by == "testuser"
    assert dto.favorited_by == "testuser"
    assert dto.managed_by == "testuser"
    assert dto.based_on_user_interests == "testuser"
    assert "ROADS" in dto.mapping_types
    assert "BUILDINGS" in dto.mapping_types
    assert dto.mapping_types_exact is True
    assert "PUBLISHED" in dto.project_statuses
    assert "DRAFT" in dto.project_statuses
    assert list(dto.interests) == [1, 2, 3]

def test_setup_search_dto_defaults():
    # Mocking FastAPI Request with no params
    request_mock = MagicMock()
    request_mock.headers.get.return_value = None
    request_mock.query_params.get.side_effect = lambda k, d=None: d
    request_mock.user = None
    
    dto = setup_search_dto(request_mock)
    
    assert dto.preferred_locale is None
    assert dto.difficulty is None
    assert dto.page == 1
    assert dto.omit_map_results is False
    assert dto.mapping_types_exact is False
    assert dto.created_by is None
