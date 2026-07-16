import pytest
from unittest.mock import patch, AsyncMock
import base64
from urllib.parse import parse_qs, urlparse
from itsdangerous import URLSafeTimedSerializer
from backend.config import test_settings as settings
from httpx import AsyncClient

from backend.services.messaging.smtp_service import SMTPService
from backend.services.users.authentication_service import (
    AuthenticationService,
    UserService,
    MessageService,
    NotFound,
    verify_token,
    AuthServiceError,
)
from backend.models.postgis.statuses import UserRole
from tests.api.helpers.test_helpers import (
    get_canned_osm_user_details,
    return_canned_user,
    create_canned_user,
    TEST_USERNAME,
)

TEST_USER_EMAIL = "thinkwheretest@test.com"

def make_token_for_user(user_id: int) -> str:
    raw = AuthenticationService.generate_session_token_for_user(user_id)
    return f"Token {base64.b64encode(raw.encode('utf-8')).decode('utf-8')}"

@pytest.mark.anyio
class TestAuthenticationService:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        canned = await return_canned_user(
            username="TEST_USER", id=111111111, db=self.db
        )
        self.test_user = await create_canned_user(self.db, canned)

    async def test_unable_to_find_user_in_osm_response_raises_error(self):
        osm_response = get_canned_osm_user_details()
        with pytest.raises(AuthServiceError):
            await AuthenticationService().login_user(
                osm_response, None, self.db, "wont-find"
            )

    @patch.object(MessageService, "send_welcome_message", new_callable=AsyncMock)
    @patch.object(UserService, "register_user", new_callable=AsyncMock)
    @patch.object(UserService, "get_and_save_stats", new_callable=AsyncMock)
    @patch.object(UserService, "update_user", new_callable=AsyncMock)
    async def test_if_login_user_calls_user_create_if_user_not_found(
        self,
        mock_update_user,
        mock_get_and_save_stats,
        mock_user_register,
        mock_message,
    ):
        osm_response = get_canned_osm_user_details()
        mock_update_user.side_effect = NotFound()
        await AuthenticationService.login_user(osm_response, None, self.db)
        mock_user_register.assert_called_with(
            7777777, TEST_USERNAME, 16, None, None, self.db
        )
        mock_get_and_save_stats.assert_awaited_once_with(7777777, self.db)
        mock_message.assert_awaited()

    @patch.object(MessageService, "send_welcome_message", new_callable=AsyncMock)
    @patch.object(UserService, "register_user", new_callable=AsyncMock)
    @patch.object(UserService, "get_and_save_stats", new_callable=AsyncMock)
    @patch.object(UserService, "update_user", new_callable=AsyncMock)
    async def test_if_login_user_calls_send_welcome_if_user_not_found(
        self,
        mock_update_user,
        mock_get_and_save_stats,
        mock_user_register,
        mock_message,
    ):
        osm_response = get_canned_osm_user_details()
        mock_update_user.side_effect = NotFound()
        new_user = await return_canned_user(self.db)
        mock_user_register.return_value = new_user
        await AuthenticationService.login_user(osm_response, None, self.db)
        mock_message.assert_awaited_once_with(new_user, self.db)

    @patch.object(UserService, "update_user", new_callable=AsyncMock)
    @patch.object(UserService, "get_user_by_id", new_callable=AsyncMock)
    async def test_if_login_user_calls_user_update_if_user_found(
        self, mock_user_get, mock_user_update
    ):
        osm_response = get_canned_osm_user_details()
        osm_response["user"]["id"] = 12345678
        osm_response["user"]["display_name"] = "Thinkwhere Test2"
        await AuthenticationService.login_user(osm_response, None, self.db)
        mock_user_update.assert_awaited_once_with(
            12345678, "Thinkwhere Test2", None, self.db
        )

    @patch.object(UserService, "get_and_save_stats", new_callable=AsyncMock)
    @patch.object(UserService, "update_user", new_callable=AsyncMock)
    async def test_if_login_user_returns_all_required_params(
        self, mock_update_user, mock_get_and_save_stats
    ):
        osm_response = get_canned_osm_user_details()
        user_params = await AuthenticationService.login_user(
            osm_response, None, self.db
        )
        assert user_params.get("username") is not None
        assert user_params.get("session_token") is not None
        assert "picture" in user_params

    @patch.object(UserService, "get_user_by_username", new_callable=AsyncMock)
    async def test_authenticate_email_token_raises_error_when_unable_to_find_user(
        self, mock_user_get
    ):
        mock_user_get.side_effect = NotFound()
        email_auth_url = SMTPService._generate_email_verification_url(
            TEST_USER_EMAIL, TEST_USERNAME
        )
        parsed_url = urlparse(email_auth_url)
        token = parse_qs(parsed_url.query)["token"][0]
        with pytest.raises(NotFound):
            await AuthenticationService().authenticate_email_token(
                username=TEST_USERNAME,
                token=token,
                db=self.db,
            )

    @patch.object(UserService, "get_user_by_username", new_callable=AsyncMock)
    async def test_authenticate_email_token_raises_error_when_invalid_token_supplied(
        self, mock_user_get
    ):
        user = await return_canned_user(self.db)
        user.email_address = TEST_USER_EMAIL
        mock_user_get.return_value = user
        with pytest.raises(AuthServiceError):
            await AuthenticationService().authenticate_email_token(
                username=TEST_USERNAME,
                token="XnRoaW5rd2hlcmV0ZXN0QHRlc3QuY29tIg.YnIWEw.9yg8kxVJXDD6dxxIktYGgnCrZNE",
                db=self.db,
            )

    @patch.object(UserService, "get_user_by_username", new_callable=AsyncMock)
    @patch.object(AuthenticationService, "is_valid_token")
    async def test_authenticate_email_token_returns_email_validated_url(
        self, mock_is_valid_token, mock_user_get
    ):
        user = await return_canned_user(self.db)
        user.email_address = TEST_USER_EMAIL
        mock_user_get.return_value = user
        mock_is_valid_token.return_value = (True, TEST_USER_EMAIL)
        result = await AuthenticationService().authenticate_email_token(
            username=TEST_USERNAME,
            token="valid-token-does-not-matter",
            db=self.db,
        )
        assert result is not None

    @patch.object(UserService, "get_user_by_username", new_callable=AsyncMock)
    async def test_authenticate_email_token_raises_error_if_email_not_matched(
        self, mock_user_get
    ):
        user = await return_canned_user(self.db)
        user.email_address = "thinkwheretest2@test.com"
        mock_user_get.return_value = user
        entropy = getattr(settings, "secret_key", None) or "un1testingmode"
        serializer = URLSafeTimedSerializer(entropy)
        with pytest.raises(AuthServiceError):
            await AuthenticationService().authenticate_email_token(
                username=TEST_USERNAME,
                token=serializer.dumps(TEST_USER_EMAIL),
                db=self.db,
            )

    @patch.object(UserService, "get_and_save_stats", new_callable=AsyncMock)
    @patch.object(UserService, "update_user", new_callable=AsyncMock)
    @patch.object(UserService, "get_user_by_id", new_callable=AsyncMock)
    async def test_login_existing_user_succeeds_and_returns_session(
        self, mock_user_get, mock_user_update, mock_get_and_save_stats
    ):
        osm_response = get_canned_osm_user_details()
        osm_response["user"]["id"] = 12345678
        user = await return_canned_user(self.db)
        user.is_email_verified = True
        user.email_address = "verified@email.com"
        user.is_expert = True
        mock_user_get.return_value = user
        mock_user_update.return_value = user
        user_params = await AuthenticationService.login_user(
            osm_response, None, self.db
        )
        assert user_params.get("username") is not None
        assert user_params.get("session_token") is not None
        assert "picture" in user_params

    @patch.object(UserService, "get_user_by_username", new_callable=AsyncMock)
    async def test_authenticate_email_token_with_success(self, mock_user_get):
        user = await return_canned_user(self.db)
        user.email_address = TEST_USER_EMAIL
        mock_user_get.return_value = user
        entropy = getattr(settings, "SECRET_KEY", None) or "un1testingmode"
        serializer = URLSafeTimedSerializer(entropy)
        valid_token = serializer.dumps(TEST_USER_EMAIL)
        with patch.object(settings, "SECRET_KEY", entropy, create=True), \
             patch("backend.services.users.authentication_service.UserService.update_user", new_callable=AsyncMock):
            result = await AuthenticationService().authenticate_email_token(
                username=TEST_USERNAME,
                token=valid_token,
                db=self.db,
            )
            assert result is not None


@pytest.mark.anyio
class TestLoginRequiredOptional:
    async def test_login_required_optional_returns_none_if_no_auth(self, client: AsyncClient):
        resp = await client.get("/api/v2/users/test_user/tasks/")
        assert resp.status_code != 401


@pytest.mark.anyio
class TestAdminOnlyDependency:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        canned = await return_canned_user(username="admin_dep_test", id=888888, db=self.db)
        self.admin_user = await create_canned_user(self.db, canned)
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": 1, "id": self.admin_user.id},
        )
        raw = AuthenticationService.generate_session_token_for_user(self.admin_user.id)
        self.admin_token = f"Token {base64.b64encode(raw.encode('utf-8')).decode('utf-8')}"

        canned_regular = await return_canned_user(username="regular_dep_test", id=777777, db=self.db)
        self.regular_user = await create_canned_user(self.db, canned_regular)
        raw_r = AuthenticationService.generate_session_token_for_user(self.regular_user.id)
        self.regular_token = f"Token {base64.b64encode(raw_r.encode('utf-8')).decode('utf-8')}"

    async def test_admin_only_raises_403_for_non_admin(self, client: AsyncClient):
        resp = await client.patch(
            f"/api/v2/users/{self.regular_user.username}/actions/set-level/ADVANCED/",
            headers={"Authorization": self.regular_token},
        )
        assert resp.status_code in [401, 403]

    async def test_admin_only_allows_admin(self, client: AsyncClient):
        resp = await client.patch(
            f"/api/v2/users/{self.regular_user.username}/actions/set-level/BEGINNER/",
            headers={"Authorization": self.admin_token},
        )
        assert resp.status_code == 200


@pytest.mark.anyio
class TestAuthenticationServiceEdgeCases:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, "auth_edge_user", 888888)
        self.test_user = await create_canned_user(self.db, row)
        self.test_user.email_address = "test_edge@email.com"
        await self.db.execute(
            "UPDATE users SET email_address = :email WHERE id = :id",
            {"email": "test_edge@email.com", "id": self.test_user.id}
        )

    @patch.object(UserService, "update_user", new_callable=AsyncMock)
    async def test_login_user_with_picture_url(self, mock_update):
        osm_response = get_canned_osm_user_details()
        osm_response["user"]["img"] = {"href": "https://gravatar.com/avatar/123"}
        user = await return_canned_user(self.db)
        mock_update.return_value = user
        with patch.object(UserService, "get_and_save_stats", new_callable=AsyncMock):
            result = await AuthenticationService.login_user(
                osm_response, "test@email.com", self.db
            )
            assert result["picture"] == "https://gravatar.com/avatar/123"
            assert result["username"] == TEST_USERNAME

    @patch.object(UserService, "update_user", new_callable=AsyncMock)
    async def test_login_user_without_picture(self, mock_update):
        osm_response = get_canned_osm_user_details()
        if "img" in osm_response["user"]:
            del osm_response["user"]["img"]
        user = await return_canned_user(self.db)
        mock_update.return_value = user
        with patch.object(UserService, "get_and_save_stats", new_callable=AsyncMock):
            result = await AuthenticationService.login_user(
                osm_response, "test@email.com", self.db
            )
            assert result["picture"] is None

    @patch.object(UserService, "update_user", new_callable=AsyncMock)
    @patch.object(UserService, "register_user", new_callable=AsyncMock)
    async def test_login_user_with_email(self, mock_register, mock_update):
        osm_response = get_canned_osm_user_details()
        mock_update.side_effect = NotFound()
        mock_register.return_value = await return_canned_user(self.db)
        with patch.object(MessageService, "send_welcome_message", new_callable=AsyncMock):
            with patch.object(UserService, "get_and_save_stats", new_callable=AsyncMock):
                result = await AuthenticationService.login_user(
                    osm_response, "test@email.com", self.db
                )
                assert result is not None

    async def test_authenticate_email_token_expired(self):
        with patch.object(UserService, 'get_user_by_username', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = self.test_user
            with patch.object(AuthenticationService, 'is_valid_token') as mock_is_valid:
                mock_is_valid.return_value = (False, "ExpiredToken- Token has expired")
                with pytest.raises(AuthServiceError) as exc_info:
                    await AuthenticationService.authenticate_email_token(
                        username=self.test_user.username,
                        token="any_token",
                        db=self.db
                    )
                assert "Expired" in str(exc_info.value) or "expired" in str(exc_info.value).lower()

    async def test_authenticate_email_token_bad_signature(self):
        with patch.object(UserService, 'get_user_by_username', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = self.test_user
            with patch.object(AuthenticationService, 'is_valid_token') as mock_is_valid:
                mock_is_valid.return_value = (False, "BadSignature- Bad Token Signature")
                with pytest.raises(AuthServiceError) as exc_info:
                    await AuthenticationService.authenticate_email_token(
                        username=self.test_user.username,
                        token="invalid.token.here",
                        db=self.db
                    )
                assert "Signature" in str(exc_info.value) or "BadSignature" in str(exc_info.value)


@pytest.mark.anyio
class TestAdminOnlyDependencyEdgeCases:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        admin_row = await return_canned_user(self.db, "admin_dep", 999999)
        self.admin = await create_canned_user(self.db, admin_row)
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": UserRole.ADMIN.value, "id": self.admin.id},
        )
        self.admin_token = make_token_for_user(self.admin.id)
        regular_row = await return_canned_user(self.db, "regular_dep", 888888)
        self.regular = await create_canned_user(self.db, regular_row)
        self.regular_token = make_token_for_user(self.regular.id)

    async def test_admin_only_missing_header(self, client: AsyncClient):
        response = await client.get("/api/v2/users/")
        assert response.status_code == 403

    async def test_admin_only_non_admin_user(self, client: AsyncClient):
        response = await client.get(
            "/api/v2/users/",
            headers={"Authorization": self.regular_token}
        )
        assert response.status_code == 200


@pytest.mark.anyio
class TestLoginRequiredMissingCases:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, "login_req_user", 5550005)
        self.user = await create_canned_user(self.db, row)

    async def test_login_required_missing_header(self, client: AsyncClient):
        resp = await client.get("/api/v2/users/queries/favorites/")
        assert resp.status_code == 403


@pytest.mark.anyio
class TestLoginRequiredOptionalCases:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, "opt_user", 5550006)
        self.user = await create_canned_user(self.db, row)
        self.valid_token = make_token_for_user(self.user.id)

    async def test_optional_valid_token(self, client: AsyncClient):
        resp = await client.get(
            "/api/v2/users/",
            headers={"Authorization": self.valid_token}
        )
        assert resp.status_code == 200


@pytest.mark.anyio
class TestAdminOnlyCases:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        admin_row = await return_canned_user(self.db, "admin_test", 5550007)
        self.admin = await create_canned_user(self.db, admin_row)
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": UserRole.ADMIN.value, "id": self.admin.id},
        )
        regular_row = await return_canned_user(self.db, "regular_test", 5550008)
        self.regular = await create_canned_user(self.db, regular_row)

    async def test_admin_only_missing_header(self, client: AsyncClient):
        resp = await client.patch(
            f"/api/v2/users/{self.regular.username}/actions/set-level/ADVANCED/",
        )
        assert resp.status_code == 403

    async def test_admin_only_user_not_found(self, client: AsyncClient):
        raw = AuthenticationService.generate_session_token_for_user(9999999)
        ghost_token = f"Token {base64.b64encode(raw.encode('utf-8')).decode('utf-8')}"
        resp = await client.patch(
            f"/api/v2/users/{self.regular.username}/actions/set-level/ADVANCED/",
            headers={"Authorization": ghost_token}
        )
        assert resp.status_code == 404