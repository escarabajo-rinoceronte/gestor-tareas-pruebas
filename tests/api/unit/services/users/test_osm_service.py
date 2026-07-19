import pytest
from unittest.mock import patch, MagicMock

from backend.services.users.osm_service import OSMService, OSMServiceError
from backend.models.dtos.user_dto import UserOSMDTO
from tests.backend.helpers.test_helpers import get_canned_osm_user_json_details


@pytest.fixture
def anyio_backend():
    return 'asyncio'


class TestOsmService:
    def test_parse_osm_user_details_raises_error_if_user_not_found(self):
        # Arrange
        osm_response = get_canned_osm_user_json_details()

        # Act & Assert
        with pytest.raises(OSMServiceError):
            OSMService._parse_osm_user_details_response(osm_response, "wont-find")

    def test_parse_osm_user_details_can_parse_valid_osm_response(self):
        # Arrange
        osm_response = get_canned_osm_user_json_details()

        # Act
        dto = OSMService._parse_osm_user_details_response(osm_response, "user")

        # Assert
        assert dto.account_created == "2017-01-23T16:23:22Z"
        assert dto.changeset_count == 16

    @pytest.mark.anyio
    @patch("backend.services.users.osm_service.httpx.AsyncClient.head")
    async def test_is_osm_user_gone_returns_true_on_410(self, mock_head):
        mock_head.return_value = MagicMock(status_code=410)
        result = await OSMService.is_osm_user_gone(123)
        assert result is True

    @pytest.mark.anyio
    @patch("backend.services.users.osm_service.httpx.AsyncClient.head")
    async def test_is_osm_user_gone_returns_false_on_200(self, mock_head):
        mock_head.return_value = MagicMock(status_code=200)
        result = await OSMService.is_osm_user_gone(123)
        assert result is False

    @pytest.mark.anyio
    @patch("backend.services.users.osm_service.httpx.AsyncClient.head")
    async def test_is_osm_user_gone_raises_error_on_other_status(self, mock_head):
        mock_head.return_value = MagicMock(status_code=404)
        with pytest.raises(OSMServiceError, match="Bad response from OSM: 404"):
            await OSMService.is_osm_user_gone(123)

    def test_get_deleted_users_returns_none_if_different_url(self):
        with patch("backend.services.users.osm_service.settings") as mock_settings:
            mock_settings.OSM_SERVER_URL = "http://localhost"
            result = OSMService.get_deleted_users()
            assert result is None

    @pytest.mark.anyio
    async def test_get_deleted_users_yields_parsed_ids(self):
        class MockStreamResponse:
            def __init__(self, status_code, lines):
                self.status_code = status_code
                self.lines = lines

            async def aiter_lines(self):
                for line in self.lines:
                    yield line

            async def __aenter__(self): return self
            async def __aexit__(self, exc_type, exc_val, exc_tb): pass

        class MockStreamContext:
            def __init__(self, status_code, lines):
                self.response = MockStreamResponse(status_code, lines)
            async def __aenter__(self): return self.response
            async def __aexit__(self, exc_type, exc_val, exc_tb): pass

        with patch("backend.services.users.osm_service.settings") as mock_settings:
            mock_settings.OSM_SERVER_URL = "https://www.openstreetmap.org"
            
            lines = [
                "123",       # valid
                "",          # empty
                "  456  ",   # valid with spaces
                "invalid",   # invalid format
                "789\n"      # valid
            ]
            
            with patch("backend.services.users.osm_service.httpx.AsyncClient.stream", return_value=MockStreamContext(200, lines)):
                generator = OSMService.get_deleted_users()
                assert generator is not None
                
                ids = [user_id async for user_id in generator]
                assert ids == [123, 456, 789]

    @pytest.mark.anyio
    async def test_get_deleted_users_raises_error_if_not_200(self):
        class MockStreamResponse:
            def __init__(self, status_code):
                self.status_code = status_code
            async def __aenter__(self): return self
            async def __aexit__(self, exc_type, exc_val, exc_tb): pass

        class MockStreamContext:
            def __init__(self, status_code):
                self.response = MockStreamResponse(status_code)
            async def __aenter__(self): return self.response
            async def __aexit__(self, exc_type, exc_val, exc_tb): pass

        with patch("backend.services.users.osm_service.settings") as mock_settings:
            mock_settings.OSM_SERVER_URL = "https://www.openstreetmap.org"
            
            with patch("backend.services.users.osm_service.httpx.AsyncClient.stream", return_value=MockStreamContext(403)):
                generator = OSMService.get_deleted_users()
                with pytest.raises(OSMServiceError, match="Failed fetching deleted users: 403"):
                    async for _ in generator:
                        pass

    @patch("backend.services.users.osm_service.requests.get")
    def test_get_osm_details_for_user_raises_410(self, mock_get):
        mock_get.return_value = MagicMock(status_code=410)
        with pytest.raises(OSMServiceError, match="User no longer exists on OSM"):
            OSMService.get_osm_details_for_user(1)

    @patch("backend.services.users.osm_service.requests.get")
    def test_get_osm_details_for_user_raises_other_error(self, mock_get):
        mock_get.return_value = MagicMock(status_code=500)
        with pytest.raises(OSMServiceError, match="Bad response from OSM"):
            OSMService.get_osm_details_for_user(1)

    @patch("backend.services.users.osm_service.requests.get")
    @patch("backend.services.users.osm_service.OSMService._parse_osm_user_details_response")
    def test_get_osm_details_for_user_success(self, mock_parse, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = {"user": {"account_created": "2017-01-23T16:23:22Z"}}
        
        expected_dto = UserOSMDTO()
        expected_dto.account_created = "2017-01-23T16:23:22Z"
        mock_parse.return_value = expected_dto
        
        result = OSMService.get_osm_details_for_user(1)
        
        assert result == expected_dto
        mock_parse.assert_called_once_with({"user": {"account_created": "2017-01-23T16:23:22Z"}})

    def test_osm_service_error_initializes(self):
        error = OSMServiceError("Test Error")
        assert isinstance(error, Exception)