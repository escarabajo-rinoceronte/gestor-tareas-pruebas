import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from backend.services.messaging.smtp_service import SMTPService, html_to_text

@pytest.mark.anyio
class TestSMTPService:
    def test_html_to_text(self):
        """Test conversion of HTML to plain text."""
        html = "<html><body><h1>Hello</h1><p>This is a <b>test</b>.</p><br/></body></html>"
        text = html_to_text(html)
        assert "Hello\nThis is a test." in text

    @patch("backend.services.messaging.smtp_service.SMTPService._send_message")
    @patch("backend.services.messaging.smtp_service.get_template")
    async def test_send_verification_email(self, mock_get_template, mock_send_message):
        """Test sending verification email."""
        mock_get_template.return_value = "<html>Template</html>"
        
        result = await SMTPService.send_verification_email("test@example.com", "testuser")
        
        assert result is True
        mock_get_template.assert_called_once()
        mock_send_message.assert_called_once_with("test@example.com", "Confirm your email address", "<html>Template</html>")

    @patch("backend.services.messaging.smtp_service.SMTPService._send_message")
    @patch("backend.services.messaging.smtp_service.get_template")
    async def test_send_welcome_email(self, mock_get_template, mock_send_message):
        """Test sending welcome email."""
        mock_get_template.return_value = "<html>Welcome</html>"
        
        result = await SMTPService.send_welcome_email("test@example.com", "testuser")
        
        assert result is True
        mock_send_message.assert_called_once_with("test@example.com", "Welcome to Tasking Manager", "<html>Welcome</html>")

    @patch("backend.services.messaging.smtp_service.SMTPService._send_message")
    async def test_send_contact_admin_email(self, mock_send_message):
        """Test sending contact admin email."""
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "content": "Need help"
        }
        
        with patch("backend.services.messaging.smtp_service.settings") as mock_settings:
            mock_settings.EMAIL_CONTACT_ADDRESS = "admin@example.com"
            await SMTPService.send_contact_admin_email(data)
            
            mock_send_message.assert_called_once()
            args, _ = mock_send_message.call_args
            assert args[0] == "admin@example.com"
            assert args[1] == "New contact from Test User"

    @patch("backend.services.messaging.smtp_service.SMTPService._send_message")
    @patch("backend.services.messaging.smtp_service.get_template")
    async def test_send_email_alert(self, mock_get_template, mock_send_message):
        """Test sending email alert for a new message."""
        mock_get_template.return_value = "<html>Alert</html>"
        
        result = await SMTPService.send_email_alert(
            to_address="test@example.com",
            username="testuser",
            user_email_verified=True,
            message_id=1,
            from_username="sender",
            project_id=1,
            task_id=1,
            subject="New Message",
            content="Hello",
            message_type=1,
            project_name="Test Project"
        )
        
        assert result is True
        mock_send_message.assert_called_once_with("test@example.com", "New Message", "<html>Alert</html>")

    async def test_send_email_alert_unverified(self):
        """Test email alert is not sent if email is unverified."""
        result = await SMTPService.send_email_alert(
            to_address="test@example.com",
            username="testuser",
            user_email_verified=False,
            message_id=1,
            from_username="sender",
            project_id=1,
            task_id=1,
            subject="New Message",
            content="Hello",
            message_type=1,
            project_name="Test Project"
        )
        
        assert result is False


    @patch("backend.services.messaging.smtp_service.SMTPService._send_message")
    async def test_send_contact_admin_email_no_contact_address(self, mock_send_message):
        """Test that error is raised if EMAIL_CONTACT_ADDRESS is not set."""
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "content": "Need help"
        }
        
        with patch("backend.services.messaging.smtp_service.settings") as mock_settings:
            mock_settings.EMAIL_CONTACT_ADDRESS = None
            
            with pytest.raises(ValueError, match="This feature is not implemented"):
                await SMTPService.send_contact_admin_email(data)
            
            mock_send_message.assert_not_called()

    @patch("backend.services.messaging.smtp_service.SMTPService._send_message")
    @patch("backend.services.messaging.smtp_service.get_template")
    async def test_send_email_alert_no_email_address(self, mock_get_template, mock_send_message):
        """Test email alert is not sent if no email address provided."""
        mock_get_template.return_value = "<html>Alert</html>"
        
        result = await SMTPService.send_email_alert(
            to_address="",  # Empty email
            username="testuser",
            user_email_verified=True,
            message_id=1,
            from_username="sender",
            project_id=1,
            task_id=1,
            subject="New Message",
            content="Hello",
            message_type=1,
            project_name="Test Project"
        )
        
        assert result is False
        mock_send_message.assert_not_called()

    @patch("backend.services.messaging.smtp_service.SMTPService._send_message")
    @patch("backend.services.messaging.smtp_service.get_template")
    async def test_send_email_alert_without_message_id(self, mock_get_template, mock_send_message):
        """Test email alert when message_id is None."""
        mock_get_template.return_value = "<html>Alert</html>"
        
        result = await SMTPService.send_email_alert(
            to_address="test@example.com",
            username="testuser",
            user_email_verified=True,
            message_id=None,  # No message ID
            from_username="sender",
            project_id=1,
            task_id=None,
            subject="New Message",
            content="Hello",
            message_type=1,
            project_name="Test Project"
        )
        
        assert result is True
        mock_send_message.assert_called_once()

    @patch("backend.services.messaging.smtp_service.SMTPService._send_message")
    @patch("backend.services.messaging.smtp_service.get_template")
    async def test_send_email_alert_without_task_id(self, mock_get_template, mock_send_message):
        """Test email alert when task_id is None."""
        mock_get_template.return_value = "<html>Alert</html>"
        
        result = await SMTPService.send_email_alert(
            to_address="test@example.com",
            username="testuser",
            user_email_verified=True,
            message_id=1,
            from_username="sender",
            project_id=1,
            task_id=None,  # No task ID
            subject="New Message",
            content="Hello",
            message_type=1,
            project_name="Test Project"
        )
        
        assert result is True
        mock_send_message.assert_called_once()

    @patch("backend.services.messaging.smtp_service.mail.send_message")
    async def test_send_message_log_level_debug(self, mock_mail_send):
        """Test _send_message when LOG_LEVEL is DEBUG."""
        with patch("backend.services.messaging.smtp_service.settings") as mock_settings:
            mock_settings.LOG_LEVEL = "DEBUG"
            mock_settings.MAIL_DEFAULT_SENDER = "test@example.com"
            
            # Mock the MessageSchema to avoid actual email sending
            with patch("backend.services.messaging.smtp_service.MessageSchema") as mock_msg_schema:
                mock_msg = MagicMock()
                mock_msg.as_string.return_value = "Debug email content"
                mock_msg_schema.return_value = mock_msg
                
                await SMTPService._send_message(
                    to_address="test@example.com",
                    subject="Test",
                    html_message="<html>Test</html>",
                    text_message="Test"
                )
                
                mock_mail_send.assert_not_called()

    @patch("backend.services.messaging.smtp_service.mail.send_message")
    async def test_send_message_success(self, mock_mail_send):
        """Test _send_message sends email successfully."""
        with patch("backend.services.messaging.smtp_service.settings") as mock_settings:
            mock_settings.LOG_LEVEL = "INFO"
            mock_settings.MAIL_DEFAULT_SENDER = "test@example.com"
            
            # Mock the MessageSchema to avoid actual email sending
            with patch("backend.services.messaging.smtp_service.MessageSchema") as mock_msg_schema:
                mock_msg = MagicMock()
                mock_msg_schema.return_value = mock_msg
                
                await SMTPService._send_message(
                    to_address="test@example.com",
                    subject="Test",
                    html_message="<html>Test</html>",
                    text_message="Test"
                )
                
                mock_mail_send.assert_called_once_with(mock_msg)


    def test_html_to_text_with_empty_content(self):
        """Test html_to_text returns empty string for empty content."""
        text = html_to_text("")
        assert text == ""

    def test_html_to_text_with_style_and_script(self):
        """Test html_to_text removes style and script tags."""
        html = """
        <html>
            <head>
                <style>body { color: red; }</style>
                <script>alert('test');</script>
            </head>
            <body>
                <h1>Hello</h1>
                <p>This is a <b>test</b>.</p>
            </body>
        </html>
        """
        text = html_to_text(html)
        assert "Hello" in text
        assert "This is a test" in text
        assert "style" not in text
        assert "script" not in text

    def test_html_to_text_with_multiple_newlines(self):
        """Test html_to_text collapses multiple newlines."""
        html = "<p>Line 1</p><br/><br/><p>Line 2</p>"
        text = html_to_text(html)
        assert "Line 1" in text
        assert "Line 2" in text
        assert "\n" in text

    def test_html_to_text_with_links(self):
        """Test html_to_text handles links correctly."""
        html = '<a href="http://example.com">Link</a>'
        text = html_to_text(html)
        assert "Link" in text


    @patch("backend.services.messaging.smtp_service.mail.send_message")
    async def test_send_message_smtp_error(self, mock_mail_send):
        """Test _send_message handles SMTP error gracefully."""
        with patch("backend.services.messaging.smtp_service.settings") as mock_settings:
            mock_settings.LOG_LEVEL = "INFO"
            mock_settings.MAIL_DEFAULT_SENDER = "test@example.com"

            mock_mail_send.side_effect = Exception("SMTP connection failed")

            with patch("backend.services.messaging.smtp_service.MessageSchema") as mock_msg_schema:
                mock_msg = MagicMock()
                mock_msg_schema.return_value = mock_msg

                await SMTPService._send_message(
                    to_address="test@example.com",
                    subject="Test",
                    html_message="<html>Test</html>",
                    text_message="Test"
                )

                mock_mail_send.assert_called_once_with(mock_msg)

    @patch("backend.services.messaging.smtp_service.mail.send_message")
    async def test_send_message_missing_from_address(self, mock_mail_send):
        """Test _send_message raises error when MAIL_DEFAULT_SENDER is not set."""
        with patch("backend.services.messaging.smtp_service.settings") as mock_settings:
            mock_settings.MAIL_DEFAULT_SENDER = None

            with pytest.raises(ValueError, match="Missing TM_EMAIL_FROM_ADDRESS"):
                await SMTPService._send_message(
                    to_address="test@example.com",
                    subject="Test",
                    html_message="<html>Test</html>",
                    text_message="Test"
                )

    @patch("backend.services.messaging.smtp_service.mail.send_message")
    async def test_send_message_uses_html_to_text(self, mock_mail_send):
        """Test _send_message uses html_to_text when text_message is None."""
        with patch("backend.services.messaging.smtp_service.settings") as mock_settings:
            mock_settings.LOG_LEVEL = "INFO"
            mock_settings.MAIL_DEFAULT_SENDER = "test@example.com"

            with patch("backend.services.messaging.smtp_service.MessageSchema") as mock_msg_schema:
                mock_msg = MagicMock()
                mock_msg_schema.return_value = mock_msg

                with patch("backend.services.messaging.smtp_service.html_to_text") as mock_html_to_text:
                    mock_html_to_text.return_value = "Plain text version"

                    await SMTPService._send_message(
                        to_address="test@example.com",
                        subject="Test",
                        html_message="<html>Test</html>",
                        text_message=None
                    )

                    mock_html_to_text.assert_called_once_with("<html>Test</html>")
                    mock_mail_send.assert_called_once_with(mock_msg)