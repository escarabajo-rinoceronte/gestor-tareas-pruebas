import pytest
from pytest import raises
from unittest.mock import patch, MagicMock, AsyncMock

from backend.services.users.osm_service import OSMService, OSMServiceError


@pytest.mark.anyio
class TestOsmService:
    async def test_get_osm_details_for_user_raises_error_if_invalid_user_id(self):
        with raises(OSMServiceError):
            await OSMService.get_osm_details_for_user("1xcf")

    async def test_get_osm_details_for_user_returns_user_details_if_valid_user_id(self):
        dto = OSMService.get_osm_details_for_user(13526430)
        assert dto.account_created == "2021-06-10T01:27:18Z"


@pytest.mark.anyio
class TestOsmServiceIsUserGone:
    async def test_is_osm_user_gone_returns_true_on_410(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 410
        with patch("httpx.AsyncClient.head", new_callable=AsyncMock, return_value=mock_resp):
            result = await OSMService.is_osm_user_gone(99999)
            assert result is True

    async def test_is_osm_user_gone_returns_false_on_200(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        with patch("httpx.AsyncClient.head", new_callable=AsyncMock, return_value=mock_resp):
            result = await OSMService.is_osm_user_gone(13526430)
            assert result is False

    async def test_is_osm_user_gone_raises_error_on_unexpected_status(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 503
        with patch("httpx.AsyncClient.head", new_callable=AsyncMock, return_value=mock_resp):
            with raises(OSMServiceError):
                await OSMService.is_osm_user_gone(99999)


@pytest.mark.anyio
class TestOsmServiceGetDetailsSync:
    def test_get_osm_details_raises_on_410(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 410
        with patch("requests.get", return_value=mock_resp):
            with raises(OSMServiceError):
                OSMService.get_osm_details_for_user(99999)

    def test_get_osm_details_raises_on_non_200(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        with patch("requests.get", return_value=mock_resp):
            with raises(OSMServiceError):
                OSMService.get_osm_details_for_user(99999)