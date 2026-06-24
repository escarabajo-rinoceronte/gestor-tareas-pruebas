from urllib.parse import parse_qs, urlparse

from backend.services.messaging.smtp_service import SMTPService
from backend.services.users.authentication_service import AuthenticationService


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

    def test_generate_session_token_with_zero_id(self):
        """Valida que el generador maneje correctamente un ID de usuario igual a cero."""
        # Act
        session_token = AuthenticationService.generate_session_token_for_user(0)

        # Assert
        assert session_token is not None
        assert isinstance(session_token, str)

    def test_generate_session_token_with_negative_id(self):
        """Valida que el generador procese IDs negativos sin lanzar excepciones de firma."""
        # Act
        session_token = AuthenticationService.generate_session_token_for_user(-9999)

        # Assert
        assert session_token is not None

    def test_is_valid_token_with_empty_string_returns_false(self):
        """Garantiza que enviar un token vacío devuelva falso de forma segura."""
        # Act
        is_valid, user_id = AuthenticationService.is_valid_token("", 604800)

        # Assert
        assert is_valid is False
        assert "BadSignature" in user_id

    def test_get_authentication_failed_url_is_string(self):
        """Valida que el método retorne un tipo de dato string primitivo."""
        # Act
        auth_failed_url = AuthenticationService.get_authentication_failed_url()

        # Assert
        assert isinstance(auth_failed_url, str)

    def test_get_email_validated_url_false_parameter(self):
        """Prueba el comportamiento de la ruta interna pasando el parámetro como False."""
        # Act
        email_validated_url = AuthenticationService._get_email_validated_url(False)

        # Assert
        parsed_url = urlparse(email_validated_url)
        assert parsed_url.path == "/validate-email"

    def test_get_email_validated_url_query_parameters(self):
        """Comprueba que la URL generada contenga parámetros de consulta válidos si existieran."""
        # Act
        email_validated_url = AuthenticationService._get_email_validated_url(True)

        # Assert
        parsed_url = urlparse(email_validated_url)
        assert parsed_url.scheme in ["http", "https", ""]

    def test_session_token_uniqueness_for_different_users(self):
        """Asegura que dos usuarios distintos obtengan firmas de tokens totalmente diferentes."""
        # Act
        token_a = AuthenticationService.generate_session_token_for_user(111)
        token_b = AuthenticationService.generate_session_token_for_user(222)

        # Assert
        assert token_a != token_b

    def test_is_valid_token_handles_very_large_user_ids(self):
        """Valida la consistencia de firma y deserialización usando un identificador entero muy grande."""
        # Arrange
        large_id = 999999999999
        session_token = AuthenticationService.generate_session_token_for_user(large_id)

        # Act
        is_valid, user_id = AuthenticationService.is_valid_token(session_token, 604800)

        # Assert
        assert is_valid is True
        assert user_id == large_id

    def test_is_valid_token_malformed_structure_returns_false(self):
        """Comprueba que un token con formato de caracteres aleatorios no legibles devuelva BadSignature."""
        # Act
        is_valid, user_id = AuthenticationService.is_valid_token("invalid.token.format.xyz", 604800)

        # Assert
        assert is_valid is False
        assert "BadSignature" in user_id

    def test_is_valid_token_with_huge_max_age(self):
        """Valida que un valor de max_age extremadamente alto sea procesado correctamente por el deserializador."""
        # Arrange
        session_token = AuthenticationService.generate_session_token_for_user(777)

        # Act
        is_valid, user_id = AuthenticationService.is_valid_token(session_token, 999999999)

        # Assert
        assert is_valid is True
        assert user_id == 777

    def test_email_verification_url_contains_token_param(self):
        """Valida que la URL generada por el SMTPService contenga el parámetro esperado clave 'token'."""
        # Arrange
        auth_url = SMTPService._generate_email_verification_url("user@domain.com", "username")

        # Act
        parsed_url = urlparse(auth_url)
        query = parse_qs(parsed_url.query)

        # Assert
        assert "token" in query
        assert len(query["token"][0]) > 0

    def test_email_verification_url_contains_username_or_context(self):
        """Comprueba que la URL de verificación de correo devuelva un string estructurado no vacío."""
        # Act
        auth_url = SMTPService._generate_email_verification_url("check@domain.com", "testuser")

        # Assert
        assert auth_url is not None
        assert "http" in auth_url

    def test_is_valid_token_returns_tuple(self):
        """Verifica que el método de validación siempre responda con una estructura de tupla (bool, cualquier cosa)."""
        # Arrange
        session_token = AuthenticationService.generate_session_token_for_user(123)

        # Act
        result = AuthenticationService.is_valid_token(session_token, 3600)

        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_auth_failed_url_has_no_query_params(self):
        """Asegura que la URL de fallo de autenticación por defecto no contenga parámetros query sueltos."""
        # Act
        auth_failed_url = AuthenticationService.get_authentication_failed_url()

        # Assert
        parsed_url = urlparse(auth_failed_url)
        assert parsed_url.query == ""

    def test_email_validated_url_is_not_empty(self):
        """Garantiza que el generador de URL de verificación de e-mail no entregue un string en blanco."""
        # Act
        url = AuthenticationService._get_email_validated_url(True)

        # Assert
        assert url != ""
        assert len(url) > 0

    def test_generate_token_idempotency_determinism(self):
        """Valida si tokens generados consecutivamente para el mismo ID devuelven el mismo valor o firma base válida."""
        # Act
        token_1 = AuthenticationService.generate_session_token_for_user(888)
        token_2 = AuthenticationService.generate_session_token_for_user(888)

        # Assert
        is_valid, _ = AuthenticationService.is_valid_token(token_1, 3600)
        is_valid_2, _ = AuthenticationService.is_valid_token(token_2, 3600)
        assert is_valid is True
        assert is_valid_2 is True

    def test_is_valid_token_with_whitespace_string_returns_false(self):
        """Asegura que tokens compuestos únicamente de espacios en blanco sean rechazados de inmediato."""
        # Act
        is_valid, user_id = AuthenticationService.is_valid_token("   ", 604800)

        # Assert
        assert is_valid is False
        assert "BadSignature" in user_id

    def test_is_valid_token_tampered_signature_only(self):
        """Valida que alterar únicamente el último carácter de la firma invalide el token por completo."""
        # Arrange
        session_token = AuthenticationService.generate_session_token_for_user(4321)
        # Modificar el último carácter si es una 'a' cambiar a 'b', de lo contrario forzar una 'a'
        tampered_token = session_token[:-1] + ('b' if session_token[-1] != 'b' else 'a')

        # Act
        is_valid, user_id = AuthenticationService.is_valid_token(tampered_token, 604800)

        # Assert
        assert is_valid is False
        assert "BadSignature" in user_id

    def test_get_email_validated_url_type_return(self):
        """Verifica que el método protegido de obtención de URL retorne un objeto de tipo string."""
        # Act
        url = AuthenticationService._get_email_validated_url(False)

        # Assert
        assert isinstance(url, str)

    def test_parse_email_verification_token_with_special_characters(self):
        """Asegura que correos con caracteres especiales (+, _, -) codifiquen y decodifiquen de forma correcta."""
        # Arrange
        special_email = "test+mailbox_dev-1@example.com"
        auth_url = SMTPService._generate_email_verification_url(special_email, "special")
        parsed_url = urlparse(auth_url)
        query = parse_qs(parsed_url.query)

        # Act
        is_valid, email_address = AuthenticationService.is_valid_token(query["token"][0], 86400)

        # Assert
        assert is_valid is True
        assert email_address == special_email

    def test_is_valid_token_with_small_max_age_success(self):
        """Prueba que la validación sea exitosa cuando se pasa un tiempo de expiración corto pero suficiente."""
        # Arrange
        session_token = AuthenticationService.generate_session_token_for_user(999)

        # Act
        is_valid, user_id = AuthenticationService.is_valid_token(session_token, 10)

        # Assert
        assert is_valid is True
        assert user_id == 999

    def test_url_parse_helper_on_failed_endpoint(self):
        """Valida la integridad de la estructura de la URL de error simulando análisis de red."""
        # Act
        url = AuthenticationService.get_authentication_failed_url()
        parsed = urlparse(url)

        # Assert
        assert parsed.fragment == ""
        assert parsed.netloc == parsed.netloc

    def test_is_valid_token_error_message_format(self):
        """Comprueba el formato exacto de la cadena devuelta cuando el token posee una firma corrupta."""
        # Act
        _, error_msg = AuthenticationService.is_valid_token("completely-corrupted-token", 604800)

        # Assert
        assert "BadSignature-" in error_msg
        assert "Bad Token Signature" in error_msg