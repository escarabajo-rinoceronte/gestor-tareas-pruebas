import base64
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import parse_qs, urlparse

from fastapi import HTTPException
from starlette.authentication import AuthenticationError

from backend.services.messaging.smtp_service import SMTPService
from backend.services.users.authentication_service import (
    AuthenticationService,
    AuthServiceError,
    login_required,
    login_required_optional,
    admin_only,
    UserRole,
)
from backend.services.users.user_service import NotFound


@pytest.fixture
def anyio_backend():
    return 'asyncio'


class TestAuthenticationService:
    def test_generate_session_token_for_user_returns_session_token(self):
        # Act
        session_token = AuthenticationService.generate_session_token_for_user(12345678)

        # Assert
        assert session_token is not None

    def test_is_valid_token_validates_user_token(self):
        # Arrange
        session_token = AuthenticationService.generate_session_token_for_user(12345678)
        invalid_session_token = session_token + "x"

        # Act
        is_valid_token, user_id = AuthenticationService.is_valid_token(
            session_token, 604800
        )
        is_invalid_token, _user_id = AuthenticationService.is_valid_token(
            invalid_session_token, 604800
        )

        # Assert
        assert is_valid_token is True
        assert user_id == 12345678
        assert is_invalid_token is False
        assert _user_id == "BadSignature- Bad Token Signature"

    def test_get_authentication_failed_url_returns_expected_url(self):
        # Act
        auth_failed_url = AuthenticationService.get_authentication_failed_url()

        # Assert
        parsed_url = urlparse(auth_failed_url)
        assert parsed_url.path == "/auth-failed"

    def test_get_email_validated_url_returns_expected_url(self):
        # Act
        email_validated_url = AuthenticationService._get_email_validated_url(True)

        # Assert
        parsed_url = urlparse(email_validated_url)
        assert parsed_url.path == "/validate-email"

    def test_can_parse_email_verification_token(self):
        # Arrange
        test_email = "test@test.com"
        auth_url = SMTPService._generate_email_verification_url(test_email, "mrtest")

        parsed_url = urlparse(auth_url)
        query = parse_qs(parsed_url.query)

        # Act
        is_valid, email_address = AuthenticationService.is_valid_token(
            query["token"][0], 86400
        )

        # Assert
        assert is_valid is True
        assert email_address == test_email

    def test_generate_random_state_returns_correct_length(self):
        # Arrange
        length = 20

        # Act
        state = AuthenticationService.generate_random_state(length=length)

        # Assert
        assert len(state) == length
        assert isinstance(state, str)

    def test_is_valid_token_returns_false_when_expired(self):
        # Arrange
        session_token = AuthenticationService.generate_session_token_for_user(12345)

        # Act
        is_valid, msg = AuthenticationService.is_valid_token(session_token, -1)

        # Assert
        assert is_valid is False
        assert "ExpiredToken" in msg

    def test_auth_service_error_initializes(self):
        # Act
        error = AuthServiceError("Test Error")

        # Assert
        assert isinstance(error, Exception)

    @pytest.mark.anyio
    async def test_login_user_raises_error_if_user_element_missing(self):
        # Arrange
        osm_details = {"wrong_key": {}}
        db_mock = AsyncMock()

        # Act & Assert
        with pytest.raises(AuthServiceError, match="User element not found"):
            await AuthenticationService.login_user(osm_details, "test@test.com", db_mock)

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.update_user")
    @patch("backend.services.users.authentication_service.UserService.get_and_save_stats")
    async def test_login_user_existing_user(self, mock_stats, mock_update):
        # Arrange
        osm_details = {
            "user": {
                "id": "123",
                "display_name": "TestUser",
                "img": {"href": "pic.jpg"}
            }
        }
        db_mock = AsyncMock()

        # Act
        result = await AuthenticationService.login_user(osm_details, "test@test.com", db_mock)

        # Assert
        mock_update.assert_called_once_with(123, "TestUser", "pic.jpg", db_mock)
        mock_stats.assert_called_once_with(123, db_mock)
        assert result["username"] == "TestUser"
        assert result["picture"] == "pic.jpg"
        assert "session_token" in result

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.update_user")
    @patch("backend.services.users.authentication_service.UserService.register_user")
    @patch("backend.services.users.authentication_service.MessageService.send_welcome_message")
    @patch("backend.services.users.authentication_service.UserService.get_and_save_stats")
    async def test_login_user_new_user(self, mock_stats, mock_welcome, mock_register, mock_update):
        # Arrange
        osm_details = {
            "user": {
                "id": "123",
                "display_name": "TestUser",
                "changesets": {"count": "5"}
            }
        }
        
        db_mock = MagicMock()
        db_mock.transaction.return_value.__aenter__.return_value = None
        db_mock.transaction.return_value.__aexit__.return_value = None

        mock_update.side_effect = NotFound()
        mock_register.return_value = MagicMock()

        # Act
        result = await AuthenticationService.login_user(osm_details, "test@test.com", db_mock)

        # Assert
        mock_update.assert_called_once()
        mock_register.assert_called_once_with(123, "TestUser", 5, None, "test@test.com", db_mock)
        mock_welcome.assert_called_once()
        mock_stats.assert_called_once()
        assert result["username"] == "TestUser"

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.get_user_by_username")
    async def test_authenticate_email_token_invalid_token(self, mock_get_user):
        # Arrange
        mock_get_user.return_value = MagicMock()
        db_mock = AsyncMock()

        # Act & Assert
        with pytest.raises(AuthServiceError):
            await AuthenticationService.authenticate_email_token("user", "invalid_token", db_mock)

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.get_user_by_username")
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_authenticate_email_token_mismatched_email(self, mock_is_valid, mock_get_user):
        # Arrange
        mock_user = MagicMock()
        mock_user.email_address = "real_db_email@test.com"
        mock_get_user.return_value = mock_user
        mock_is_valid.return_value = (True, "other_email@test.com")
        db_mock = AsyncMock()

        # Act & Assert
        with pytest.raises(AuthServiceError, match="InvalidEmail"):
            await AuthenticationService.authenticate_email_token("user", "valid_token", db_mock)


class TestFastAPIDependencies:
    @pytest.mark.anyio
    async def test_login_required_missing_auth(self):
        # Arrange
        auth_header = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await login_required(auth_header)
        assert exc.value.status_code == 401
        assert "Authorization header missing" in str(exc.value.detail)

    @pytest.mark.anyio
    async def test_login_required_invalid_scheme(self):
        # Arrange
        auth_header = "Bearer mi_token_aqui"

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await login_required(auth_header)
        assert exc.value.status_code == 401
        assert "Invalid authentication scheme" in str(exc.value.detail)

    @pytest.mark.anyio
    async def test_login_required_invalid_base64(self):
        # Arrange
        auth_header = "Token !!!no_es_base64!!!"

        # Act & Assert
        with pytest.raises(AuthenticationError):
            await login_required(auth_header)

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_login_required_valid_token(self, mock_is_valid):
        # Arrange
        valid_base64 = base64.b64encode(b"mocked_token_string").decode("ascii")
        auth_header = f"Token {valid_base64}"
        mock_is_valid.return_value = (True, 999)

        # Act
        user_dto = await login_required(auth_header)

        # Assert
        assert user_dto.id == 999

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_login_required_optional_returns_none_if_missing(self, mock_is_valid):
        # Act
        result = await login_required_optional(None)
        
        # Assert
        assert result is None

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_admin_only_valid_admin(self, mock_is_valid):
        # Arrange
        valid_base64 = base64.b64encode(b"mocked_token_string").decode("ascii")
        auth_header = f"Token {valid_base64}"
        mock_is_valid.return_value = (True, 999)

        db_mock = AsyncMock()
        db_mock.fetch_one.return_value = {"id": 999, "username": "admin", "role": UserRole.ADMIN.value}

        # Act
        user_dto = await admin_only(auth_header, db_mock)

        # Assert
        assert user_dto.id == 999
        db_mock.fetch_one.assert_called_once()

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_admin_only_forbidden_non_admin(self, mock_is_valid):
        # Arrange
        valid_base64 = base64.b64encode(b"mocked_token_string").decode("ascii")
        auth_header = f"Token {valid_base64}"
        mock_is_valid.return_value = (True, 999)

        db_mock = AsyncMock()
        db_mock.fetch_one.return_value = {"id": 999, "username": "user", "role": -1} 

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await admin_only(auth_header, db_mock)
        
        assert exc.value.status_code == 403
        assert "Admin access required" in str(exc.value.detail)

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.update_user")
    @patch("backend.services.users.authentication_service.UserService.get_and_save_stats")
    @patch("backend.services.users.authentication_service.AuthenticationService.generate_session_token_for_user")
    async def test_login_user_without_picture(self, mock_generate_token, mock_stats, mock_update):
        """Test login_user handles user without profile picture."""
        # Arrange
        osm_details = {
            "user": {
                "id": "123",
                "display_name": "TestUser",
                "changesets": {"count": "10"}
            }
        }
        db_mock = AsyncMock()
        mock_generate_token.return_value = "fake_token"
        mock_update.return_value = None

        # Act
        result = await AuthenticationService.login_user(osm_details, "test@test.com", db_mock)

        # Assert
        mock_update.assert_called_once_with(123, "TestUser", None, db_mock)
        mock_stats.assert_called_once_with(123, db_mock)
        assert result["username"] == "TestUser"
        assert result["picture"] is None
        assert result["session_token"] == "fake_token"

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.update_user")
    @patch("backend.services.users.authentication_service.UserService.get_and_save_stats")
    async def test_login_user_with_picture(self, mock_stats, mock_update):
        """Test login_user handles user with profile picture."""
        # Arrange
        osm_details = {
            "user": {
                "id": "123",
                "display_name": "TestUser",
                "img": {"href": "https://example.com/avatar.jpg"},
                "changesets": {"count": "10"}
            }
        }
        db_mock = AsyncMock()
        mock_update.return_value = None

        with patch("backend.services.users.authentication_service.AuthenticationService.generate_session_token_for_user") as mock_generate:
            mock_generate.return_value = "fake_token"
            
            # Act
            result = await AuthenticationService.login_user(osm_details, "test@test.com", db_mock)

        # Assert
        mock_update.assert_called_once_with(123, "TestUser", "https://example.com/avatar.jpg", db_mock)
        mock_stats.assert_called_once_with(123, db_mock)
        assert result["picture"] == "https://example.com/avatar.jpg"

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.update_user")
    @patch("backend.services.users.authentication_service.UserService.register_user")
    @patch("backend.services.users.authentication_service.MessageService.send_welcome_message")
    @patch("backend.services.users.authentication_service.UserService.get_and_save_stats")
    async def test_login_user_new_user_without_picture(
        self, mock_stats, mock_welcome, mock_register, mock_update
    ):
        """Test login_user handles new user without profile picture."""
        # Arrange
        osm_details = {
            "user": {
                "id": "123",
                "display_name": "TestUser",
                "changesets": {"count": "5"}
            }
        }
        
        db_mock = MagicMock()
        db_mock.transaction.return_value.__aenter__.return_value = None
        db_mock.transaction.return_value.__aexit__.return_value = None

        mock_update.side_effect = NotFound()
        mock_register.return_value = MagicMock()
        mock_stats.return_value = None

        with patch("backend.services.users.authentication_service.AuthenticationService.generate_session_token_for_user") as mock_generate:
            mock_generate.return_value = "fake_token"
            
            # Act
            result = await AuthenticationService.login_user(osm_details, "test@test.com", db_mock)

        # Assert
        mock_update.assert_called_once()
        mock_register.assert_called_once_with(123, "TestUser", 5, None, "test@test.com", db_mock)
        mock_welcome.assert_called_once()
        mock_stats.assert_called_once()
        assert result["picture"] is None

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.get_user_by_username")
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    @patch("backend.services.users.authentication_service.User.set_email_verified_status")
    async def test_authenticate_email_token_success(
        self, mock_set_verified, mock_is_valid, mock_get_user
    ):
        """Test authenticate_email_token successfully validates email token."""
        # Arrange
        mock_user = MagicMock()
        mock_user.email_address = "test@example.com"
        mock_get_user.return_value = mock_user
        mock_is_valid.return_value = (True, "test@example.com")
        mock_set_verified.return_value = None
        db_mock = AsyncMock()

        # Act
        result = await AuthenticationService.authenticate_email_token(
            "test_user", "valid_token", db_mock
        )

        # Assert
        mock_get_user.assert_called_once_with("test_user", db_mock)
        mock_is_valid.assert_called_once_with("valid_token", 86400)
        mock_set_verified.assert_called_once_with(mock_user, is_verified=True, db=db_mock)
        assert "/validate-email?is_valid=True" in result

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.get_user_by_username")
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_authenticate_email_token_expired(self, mock_is_valid, mock_get_user):
        """Test authenticate_email_token raises error when token is expired."""
        # Arrange
        mock_user = MagicMock()
        mock_user.email_address = "test@example.com"
        mock_get_user.return_value = mock_user
        mock_is_valid.return_value = (False, "ExpiredToken- Token has expired")
        db_mock = AsyncMock()

        # Act & Assert
        with pytest.raises(AuthServiceError, match="ExpiredToken"):
            await AuthenticationService.authenticate_email_token(
                "test_user", "expired_token", db_mock
            )

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.get_user_by_username")
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_authenticate_email_token_bad_signature(self, mock_is_valid, mock_get_user):
        """Test authenticate_email_token raises error when token has bad signature."""
        # Arrange
        mock_user = MagicMock()
        mock_user.email_address = "test@example.com"
        mock_get_user.return_value = mock_user
        mock_is_valid.return_value = (False, "BadSignature- Bad Token Signature")
        db_mock = AsyncMock()

        # Act & Assert
        with pytest.raises(AuthServiceError, match="BadSignature"):
            await AuthenticationService.authenticate_email_token(
                "test_user", "bad_token", db_mock
            )

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.UserService.get_user_by_username")
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_authenticate_email_token_email_mismatch(self, mock_is_valid, mock_get_user):
        """Test authenticate_email_token raises error when email doesn't match token."""
        # Arrange
        mock_user = MagicMock()
        mock_user.email_address = "real@example.com"
        mock_get_user.return_value = mock_user
        mock_is_valid.return_value = (True, "different@example.com")
        db_mock = AsyncMock()

        # Act & Assert
        with pytest.raises(AuthServiceError, match="InvalidEmail"):
            await AuthenticationService.authenticate_email_token(
                "test_user", "valid_token", db_mock
            )

    @patch("backend.services.users.authentication_service.settings")
    def test_generate_session_token_for_user_with_secret_key(self, mock_settings):
        """Test generate_session_token_for_user with secret key configured."""
        # Arrange
        mock_settings.SECRET_KEY = "test_secret_key"
        
        with patch("backend.services.users.authentication_service.URLSafeTimedSerializer") as mock_serializer:
            mock_serializer_instance = MagicMock()
            mock_serializer_instance.dumps = MagicMock(return_value="fake_token")
            mock_serializer.return_value = mock_serializer_instance
            
            # Act
            result = AuthenticationService.generate_session_token_for_user(123456)
            
            # Assert
            assert result == "fake_token"
            mock_serializer.assert_called_once_with("test_secret_key")

    @patch("backend.services.users.authentication_service.settings")
    def test_generate_session_token_for_user_no_secret_key(self, mock_settings):
        """Test generate_session_token_for_user without secret key configured."""
        # Arrange
        mock_settings.SECRET_KEY = None
        
        with patch("backend.services.users.authentication_service.URLSafeTimedSerializer") as mock_serializer:
            mock_serializer_instance = MagicMock()
            mock_serializer_instance.dumps = MagicMock(return_value="fake_token")
            mock_serializer.return_value = mock_serializer_instance
            
            # Act
            result = AuthenticationService.generate_session_token_for_user(123456)
            
            # Assert
            assert result == "fake_token"
            mock_serializer.assert_called_once_with("un1testingmode")

    @patch("backend.services.users.authentication_service.settings")
    def test_is_valid_token_success(self, mock_settings):
        """Test is_valid_token returns True for valid token."""
        # Arrange
        mock_settings.SECRET_KEY = "test_secret"
        
        with patch("backend.services.users.authentication_service.URLSafeTimedSerializer") as mock_serializer:
            mock_serializer_instance = MagicMock()
            mock_serializer_instance.loads = MagicMock(return_value=123456)
            mock_serializer.return_value = mock_serializer_instance
            
            # Act
            is_valid, user_id = AuthenticationService.is_valid_token("valid_token", 604800)
            
            # Assert
            assert is_valid is True
            assert user_id == 123456

    @patch("backend.services.users.authentication_service.settings")
    def test_generate_random_state_length(self, mock_settings):
        """Test generate_random_state returns correct length."""
        # Arrange
        with patch("backend.services.users.authentication_service.SystemRandom") as mock_random:
            mock_random_instance = MagicMock()
            mock_random_instance.choice = MagicMock(side_effect=lambda x: x[0])
            mock_random.return_value = mock_random_instance
            
            # Act
            result = AuthenticationService.generate_random_state(length=20)
            
            # Assert
            assert len(result) == 20

    @patch("backend.services.users.authentication_service.settings")
    def test_generate_random_state_default_length(self, mock_settings):
        """Test generate_random_state uses default length (48)."""
        # Arrange
        with patch("backend.services.users.authentication_service.SystemRandom") as mock_random:
            mock_random_instance = MagicMock()
            mock_random_instance.choice = MagicMock(side_effect=lambda x: x[0])
            mock_random.return_value = mock_random_instance
            
            # Act
            result = AuthenticationService.generate_random_state()
            
            # Assert
            assert len(result) == 48

    @patch("backend.services.users.authentication_service.settings")
    def test_generate_random_state_valid_chars(self, mock_settings):
        """Test generate_random_state uses valid characters."""
        # Arrange
        valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        
        with patch("backend.services.users.authentication_service.SystemRandom") as mock_random:
            mock_random_instance = MagicMock()
            mock_random_instance.choice = MagicMock(side_effect=lambda x: x[0])
            mock_random.return_value = mock_random_instance
            
            # Act
            result = AuthenticationService.generate_random_state(length=100)
            
            # Assert
            for char in result:
                assert char in valid_chars

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_login_required_optional_valid_token(self, mock_is_valid):
        """Test login_required_optional returns AuthUserDTO for valid token."""
        # Arrange
        valid_base64 = base64.b64encode(b"mocked_token_string").decode("ascii")
        auth_header = f"Token {valid_base64}"
        mock_is_valid.return_value = (True, 999)

        # Act
        user_dto = await login_required_optional(auth_header)

        # Assert
        assert user_dto.id == 999

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_login_required_optional_invalid_token(self, mock_is_valid):
        """Test login_required_optional returns None for invalid token."""
        # Arrange
        valid_base64 = base64.b64encode(b"mocked_token_string").decode("ascii")
        auth_header = f"Token {valid_base64}"
        mock_is_valid.return_value = (False, "Invalid token")

        # Act
        result = await login_required_optional(auth_header)

        # Assert
        assert result is None

    @pytest.mark.anyio
    async def test_login_required_optional_invalid_scheme(self):
        """Test login_required_optional raises error for invalid scheme."""
        # Arrange
        auth_header = "Bearer invalid_token"

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await login_required_optional(auth_header)
        assert exc.value.status_code == 401
        assert "Invalid authentication scheme" in str(exc.value.detail)

    @pytest.mark.anyio
    @patch("backend.services.users.authentication_service.AuthenticationService.is_valid_token")
    async def test_admin_only_user_not_found(self, mock_is_valid):
        """Test admin_only raises 404 when user not found."""
        # Arrange
        valid_base64 = base64.b64encode(b"mocked_token_string").decode("ascii")
        auth_header = f"Token {valid_base64}"
        mock_is_valid.return_value = (True, 999)

        db_mock = AsyncMock()
        db_mock.fetch_one.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await admin_only(auth_header, db_mock)
        assert exc.value.status_code == 404
        assert "User not found" in str(exc.value.detail)

    @pytest.mark.anyio
    async def test_admin_only_missing_auth(self):
        """Test admin_only raises 401 when Authorization header missing."""
        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await admin_only(None)
        assert exc.value.status_code == 401
        assert "Authorization header missing" in str(exc.value.detail)

    @pytest.mark.anyio
    async def test_admin_only_invalid_scheme(self):
        """Test admin_only raises 401 for invalid scheme."""
        # Arrange
        auth_header = "Bearer invalid_token"

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await admin_only(auth_header)
        assert exc.value.status_code == 401
        assert "Invalid authentication scheme" in str(exc.value.detail)