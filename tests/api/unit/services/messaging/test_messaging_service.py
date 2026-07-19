import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime
from backend.models.postgis.message import Message, MessageType
from backend.models.postgis.statuses import TaskStatus
from backend.services.messaging.message_service import MessageService, MessageServiceError
from backend.exceptions import NotFound
from tests.api.helpers.test_helpers import create_canned_user, return_canned_user, create_canned_project

MESSAGE_TYPES = "3,2,1"

@pytest.mark.anyio
class TestMessagingService:
    @pytest.fixture(autouse=True)
    async def setup_test_data(self, db_connection_fixture, request):
        request.cls.db = db_connection_fixture

    async def test_message_service_generates_correct_task_link(self):
        link = MessageService.get_task_link(1, 1, "http://test.com")
        assert 'href="http://test.com/projects/1/tasks/?search=1"' in link

    @patch.object(Message, "delete_multiple_messages", new_callable=AsyncMock)
    async def test_delete_multiple_messages_delegation(self, mock_del):
        await MessageService.delete_multiple_messages([1, 2], 1, self.db)
        mock_del.assert_called_once()

    async def test_send_welcome_message_persists_system_message(self):
        user_obj = await return_canned_user(self.db, username="welcome_test", id=888)
        user = await create_canned_user(self.db, user_obj)
        
        await MessageService.send_welcome_message(user, self.db)
        
        count = await self.db.fetch_val(
            "SELECT COUNT(*) FROM messages WHERE to_user_id = :uid AND message_type = 1",
            {"uid": user.id}
        )
        assert count == 1

    async def test_has_user_new_messages_returns_correct_counts(self):
        # Corregido: Uso correcto de helpers
        user_obj = await return_canned_user(self.db, username="count_test", id=555)
        user = await create_canned_user(self.db, user_obj)
        
        await self.db.execute(
            "INSERT INTO notifications (user_id, unread_count, date) VALUES (:uid, 1, :d)",
            {"uid": user.id, "d": datetime.utcnow()}
        )
        await self.db.execute(
            "INSERT INTO messages (message, subject, to_user_id, read, date) VALUES ('m', 's', :uid, false, :d)",
            {"uid": user.id, "d": datetime.utcnow()}
        )
        
        result = await MessageService.has_user_new_messages(user.id, self.db)
        assert result["newMessages"] is True
        assert result["unread"] >= 1

    async def test_resend_email_validation_raises_error_if_no_email(self):
        # Corregido: Uso correcto de helpers
        user_obj = await return_canned_user(self.db, id=444, username="no_email")
        user = await create_canned_user(self.db, user_obj)
        
        with pytest.raises(ValueError, match="EmailNotSet"):
            await MessageService.resend_email_validation(user.id, self.db)

    async def test_parse_message_for_username_extracts_correct_handles(self):
        comment = "Hi @test_user and [another_user]"
        with patch.object(MessageService, "_parse_message_for_bulk_mentions", return_value=[]):
            usernames = await MessageService._parse_message_for_username(comment, 1, 1, self.db)
            assert "test_user" in usernames
            assert "another_user" in usernames

    @patch("backend.services.messaging.message_service.SMTPService.send_email_alert", new_callable=AsyncMock)
    async def test_push_messages_checks_user_preferences(self, mock_email):
        user_obj = await return_canned_user(self.db, id=111, username="pref_test")
        user = await create_canned_user(self.db, user_obj)
        
        # 1. Actualizar Base de Datos
        await self.db.execute("UPDATE users SET mentions_notifications = False WHERE id = 111")
        # 2. Actualizar el objeto en memoria para que el servicio vea el cambio
        user.mentions_notifications = False 
        
        msg = Message()
        msg.message_type = 3 # MENTION_NOTIFICATION
        msg.to_user_id = user.id
        msg.from_user_id = user.id
        msg.id = 1
        msg.subject = "Test"
        msg.message = "Body"
        
        # Act
        await MessageService._push_messages([{"message": msg, "user": user, "project_name": "P1"}], self.db)
        
        # Assert: Ahora sí debe ser False, porque el servicio verá user.mentions_notifications como False
        assert mock_email.called is False

    async def test_parse_message_for_bulk_mentions_author(self):
        """Valida que #author sea identificado correctamente."""
        project, author, project_id = await create_canned_project(self.db)
        
        # Usar el prefijo # que es el formato esperado por el backend para menciones especiales
        message = "Calling the #author"
        usernames = await MessageService._parse_message_for_bulk_mentions(message, project_id, db=self.db)
        
        assert author.username in usernames
        assert len(usernames) == 1

    async def test_get_all_messages_pagination_logic(self):
        """Valida la recuperación de mensajes con filtros de estado."""
        user_obj = await return_canned_user(self.db, id=1010, username="msg_test")
        user = await create_canned_user(self.db, user_obj)
        
        # Insertar 1 leido, 1 no leido
        await self.db.execute(
            "INSERT INTO messages (message, subject, to_user_id, read, date) VALUES ('m1', 's1', :uid, true, :d)",
            {"uid": user.id, "d": datetime.utcnow()}
        )
        await self.db.execute(
            "INSERT INTO messages (message, subject, to_user_id, read, date) VALUES ('m2', 's2', :uid, false, :d)",
            {"uid": user.id, "d": datetime.utcnow()}
        )
        
        # Act: Pedir solo unread
        res = await MessageService.get_all_messages(self.db, user.id, "en", 1, status="unread")
        
        assert len(res.user_messages) == 1
        assert res.user_messages[0].subject == "s2"
        assert res.pagination.total == 1


    async def test_link_generators(self):
        assert "href=" in MessageService.get_project_link(1, "Proj", highlight=True, include_chat_section=True)
        assert "href=" in MessageService.get_user_profile_link("test")
        assert "href=" in MessageService.get_user_settings_link("section")
        assert "href=" in MessageService.get_organisation_link(1, "org")
        assert "href=" in MessageService.get_team_link("team", 1, False)
        assert "href=" in MessageService.get_team_link("team", 1, True)

    @patch("backend.services.messaging.message_service.MessageService._push_messages")
    @patch("backend.services.messaging.message_service.UserService.get_user_by_id")
    @patch("backend.services.messaging.message_service.Project.get")
    async def test_send_message_after_validation(self, mock_get_project, mock_get_user, mock_push):
        mock_get_project.return_value = MagicMock(default_locale="en")
        mock_get_user.return_value = MagicMock(username="test")
        
        # Act: Distinct mapper and validator
        await MessageService.send_message_after_validation(TaskStatus.VALIDATED, 1, 2, 1, 1, self.db)
        mock_push.assert_called_once()
        
        # Act: Same mapper and validator (shortcut)
        mock_push.reset_mock()
        await MessageService.send_message_after_validation(TaskStatus.VALIDATED, 1, 1, 1, 1, self.db)
        mock_push.assert_not_called()

    async def test_get_message_raises_errors(self):
        with patch.object(self.db, "fetch_one", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = None
            with pytest.raises(NotFound):
                await MessageService.get_message(99, 1, self.db)
            
            mock_fetch.return_value = {"id": 99, "to_user_id": 2}
            with pytest.raises(MessageServiceError, match="AccessOtherUserMessage"):
                await MessageService.get_message(99, 1, self.db)

    async def test_get_message_as_dto(self):
        with patch.object(self.db, "fetch_one", new_callable=AsyncMock) as mock_fetch:
            with patch.object(self.db, "execute", new_callable=AsyncMock) as mock_exec:
                mock_fetch.return_value = {
                    "message_id": 99, "to_user_id": 1, "message_type": 1, "id": 99,
                    "subject": "s", "message": "m", "from_user_id": 2, "task_id": 1,
                    "sent_date": datetime.utcnow(), "read": False, "project_id": 1,
                    "from_username": "u", "display_picture_url": "p", "project_title": "t"
                }
                res = await MessageService.get_message_as_dto(99, 1, self.db)
                assert res["message_id"] == 99
                assert res["message_type"] == "SYSTEM"
                mock_exec.assert_called_once()

    @patch("backend.services.messaging.message_service.Message.delete_all_messages", new_callable=AsyncMock)
    async def test_delete_all_messages(self, mock_del):
        await MessageService.delete_all_messages(1, self.db, "1,2")
        mock_del.assert_called_once_with(1, self.db, [1, 2])

    @patch("backend.services.messaging.message_service.Message.mark_all_messages_read", new_callable=AsyncMock)
    async def test_mark_all_messages_read(self, mock_mark):
        await MessageService.mark_all_messages_read(1, self.db, "1,2")
        mock_mark.assert_called_once_with(1, self.db, [1, 2])

    @patch("backend.services.messaging.message_service.MessageService._push_messages")
    @patch("backend.services.messaging.message_service.UserService.get_user_by_id")
    async def test_team_notifications(self, mock_get_user, mock_push):
        mock_get_user.return_value = MagicMock(id=2)
        
        await MessageService.send_team_join_notification(1, "user1", 2, "team", 1, "MEMBER", self.db)
        mock_push.assert_called_once()
        
        mock_push.reset_mock()
        await MessageService.send_request_to_join_team(1, "user1", 2, "team", 1, self.db)
        mock_push.assert_called_once()

        mock_push.reset_mock()
        await MessageService.accept_reject_request_to_join_team(1, "user1", 2, "team", 1, "accept", self.db)
        mock_push.assert_called_once()

        mock_push.reset_mock()
        await MessageService.accept_reject_invitation_request_for_team(1, "user1", 2, "sender", "team", 1, "accept", self.db)
        mock_push.assert_called_once()

    @patch("backend.services.messaging.message_service.SMTPService.send_verification_email")
    @patch("backend.services.messaging.message_service.UserService.get_user_by_id")
    async def test_resend_email_validation_success(self, mock_get_user, mock_smtp):
        mock_user = MagicMock(email_address="test@test.com", username="test")
        mock_get_user.return_value = mock_user
        await MessageService.resend_email_validation(1, self.db)
        mock_smtp.assert_called_once_with("test@test.com", "test")
    
    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_get_all_messages_filters(self, mock_fetch_one, mock_fetch_all):
        mock_fetch_all.return_value = []
        mock_fetch_one.return_value = {"total_count": 0}
        
        res = await MessageService.get_all_messages(
            self.db, 1, "en", 1, 
            project=1, task_id=1, status="unread", message_type="1", from_username="test"
        )
        
        assert len(res.user_messages) == 0
        assert res.pagination.total == 0

    @patch("backend.services.messaging.message_service.MessageService.get_message")
    async def test_delete_message(self, mock_get_message):
        with patch.object(self.db, "execute", new_callable=AsyncMock) as mock_exec:
            await MessageService.delete_message(1, 1, self.db)
            mock_get_message.assert_called_once_with(1, 1, self.db)
            mock_exec.assert_called_once()


    @patch("backend.services.messaging.message_service.SMTPService.send_email_alert")
    @patch("backend.services.messaging.message_service.UserService.get_user_by_id")
    async def test_push_messages_with_different_notification_preferences(
        self, mock_get_user, mock_send_email
    ):
        """Test _push_messages handles different notification preferences."""
        # Crear usuario con diferentes preferencias
        user = MagicMock()
        user.id = 1
        user.email_address = "test@example.com"
        user.is_email_verified = True
        user.username = "testuser"
        user.mentions_notifications = False
        user.projects_notifications = False
        user.teams_announcement_notifications = False
        user.projects_comments_notifications = False
        user.tasks_comments_notifications = False
        user.task_validation_notification = False
        user.task_invalidation_notification = False
        
        mock_get_user.return_value = MagicMock(username="sender")
        
        msg = Message()
        msg.id = 1
        msg.message_type = MessageType.BROADCAST.value
        msg.from_user_id = 2
        msg.project_id = 1
        msg.task_id = None
        msg.subject = "Test"
        msg.message = "Body"
        
        await MessageService._push_messages(
            [{"message": msg, "user": user, "project_name": "Test"}], 
            self.db
        )
        
        # Verificar que no se envió email porque notifications están desactivadas
        mock_send_email.assert_not_called()

    @patch("backend.services.messaging.message_service.db_connection.database.connection")
    @patch("backend.services.messaging.message_service.Project.get")
    @patch("backend.services.messaging.message_service.User.get_by_username")
    @patch("backend.services.messaging.message_service.OrganisationService.get_organisation_by_id_as_dto")
    @patch("backend.services.messaging.message_service.get_template")
    @patch("backend.services.messaging.message_service.SMTPService._send_message")
    @patch("backend.services.messaging.message_service.UserService.get_user_by_username")
    async def test_send_project_transfer_message(
        self, mock_get_user_by_username, mock_smtp_send, mock_get_template,
        mock_get_org, mock_get_user, mock_get_project, mock_connection
    ):
        """Test send_project_transfer_message sends transfer notification."""
        mock_conn = AsyncMock()
        mock_connection.return_value.__aenter__.return_value = mock_conn
        
        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.organisation_id = 1
        mock_project.default_locale = "en"
        mock_project.get_project_title = AsyncMock(return_value="Test Project")
        mock_get_project.return_value = mock_project
        
        mock_get_user.return_value = MagicMock(id=1)
        
        mock_org = MagicMock()
        mock_org.name = "Test Org"
        mock_org.managers = [MagicMock(username="manager1")]
        mock_get_org.return_value = mock_org
        
        mock_get_template.return_value = "<html>Template</html>"
        
        mock_manager = MagicMock()
        mock_manager.id = 2
        mock_manager.email_address = "manager@test.com"
        mock_manager.is_email_verified = True
        mock_manager.username = "manager1"
        mock_get_user_by_username.return_value = mock_manager
        
        await MessageService.send_project_transfer_message(
            1, "new_owner", "old_owner"
        )
        
        mock_smtp_send.assert_called()

    @patch("backend.services.messaging.message_service.db_connection.database.connection")
    @patch("backend.services.messaging.message_service.MessageService._parse_message_for_username")
    @patch("backend.services.messaging.message_service.UserService.get_user_by_username")
    @patch("backend.services.messaging.message_service.UserService.get_user_by_id")
    @patch("backend.services.messaging.message_service.MessageService._push_messages")
    async def test_send_message_after_chat_with_mentions(
        self, mock_push, mock_get_user_by_id, mock_get_user_by_username,
        mock_parse_mentions, mock_connection
    ):
        """Test send_message_after_chat handles mentions in chat."""
        mock_conn = AsyncMock()
        mock_connection.return_value.__aenter__.return_value = mock_conn
        
        # Mock para fetch_all
        mock_conn.fetch_all = AsyncMock(return_value=[])
        
        # Mock para menciones
        mock_parse_mentions.return_value = ["mentioned_user"]
        
        mock_user = MagicMock()
        mock_user.id = 2
        mock_user.username = "mentioned_user"
        mock_get_user_by_username.return_value = mock_user
        
        await MessageService.send_message_after_chat(
            chat_from=1,
            chat="Hey @mentioned_user check this",
            project_id=1,
            project_name="Test Project"
        )
        
        mock_push.assert_called()

    @patch("backend.services.messaging.message_service.db_connection.database.connection")
    @patch("backend.services.messaging.message_service.MessageService._parse_message_for_username")
    @patch("backend.services.messaging.message_service.UserService.get_user_by_username")
    async def test_send_message_after_chat_username_not_found(
        self, mock_get_user_by_username, mock_parse_mentions, mock_connection
    ):
        """Test send_message_after_chat handles non-existent username gracefully."""
        mock_conn = AsyncMock()
        mock_connection.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetch_all = AsyncMock(return_value=[])
        
        mock_parse_mentions.return_value = ["nonexistent_user"]
        mock_get_user_by_username.side_effect = NotFound("User not found")
        
        # No debe levantar excepción
        await MessageService.send_message_after_chat(
            chat_from=1,
            chat="Hey @nonexistent_user",
            project_id=1,
            project_name="Test Project"
        )

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    @patch("backend.services.messaging.message_service.Project.get_project_title")
    async def test_get_all_messages_with_sort_and_filters(
        self, mock_get_title, mock_fetch_one, mock_fetch_all
    ):
        """Test get_all_messages with various sort and filter options."""
        # Mock con mensajes
        mock_fetch_all.return_value = [
            {
                "message_id": 1,
                "subject": "Test",
                "message": "Body",
                "from_user_id": 2,
                "to_user_id": 1,
                "task_id": None,
                "message_type": 1,
                "sent_date": datetime.utcnow(),
                "read": False,
                "project_id": 1,
                "from_username": "sender",
                "display_picture_url": None
            }
        ]
        mock_fetch_one.return_value = {"total_count": 1}
        mock_get_title.return_value = "Test Project"
        
        # Probar diferentes combinaciones de filtros
        res = await MessageService.get_all_messages(
            db=self.db,
            user_id=1,
            locale="en",
            page=1,
            page_size=10,
            sort_by="date",
            sort_direction="DESC",
            project=1,
            task_id=1,
            status="unread",
            message_type="1",
            from_username="test"
        )
        
        assert len(res.user_messages) > 0
        assert res.pagination.total == 1

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_all_tasks_mappers_with_data(self, mock_fetch_all):
        """Test get_all_tasks_mappers returns list of mappers."""
        mock_fetch_all.return_value = [
            {"username": "mapper1"},
            {"username": "mapper2"}
        ]
        
        mappers = await MessageService.get_all_tasks_mappers(1, 1, self.db)
        
        assert len(mappers) == 2
        assert "mapper1" in mappers
        assert "mapper2" in mappers

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_all_project_mappers_with_data(self, mock_fetch_all):
        """Test get_all_project_mappers returns list of all project mappers."""
        mock_fetch_all.return_value = [
            {"username": "mapper1"},
            {"username": "mapper2"},
            {"username": "mapper3"}
        ]
        
        mappers = await MessageService.get_all_project_mappers(1, self.db)
        
        assert len(mappers) == 3
        assert "mapper1" in mappers


    @patch("backend.services.messaging.message_service.ProjectInfo.get_dto_for_locale")
    async def test_send_message_after_comment_with_mention_self_removed(
        self, mock_get_dto
    ):
        """Test send_message_after_comment removes self-mention."""
        mock_get_dto.return_value = MagicMock(name="Test Project")

        canned_project, canned_author, canned_project_id = await create_canned_project(
            self.db
        )

        with patch("backend.services.messaging.message_service.MessageService._push_messages", new_callable=AsyncMock) as mock_push:
            await MessageService.send_message_after_comment(
                canned_author.id,
                f"Hey @{canned_author.username} check this",
                1,
                int(canned_project_id),
                db=self.db,
            )

            # Self-mention should be removed, no exception raised

    @patch("backend.services.messaging.message_service.db_connection.database.connection")
    @patch("backend.services.messaging.message_service.MessageService._parse_message_for_username")
    @patch("backend.services.messaging.message_service.UserService.get_user_by_username")
    async def test_send_message_after_chat_username_not_found_handled(
        self, mock_get_user_by_username, mock_parse_mentions, mock_connection
    ):
        """Test send_message_after_chat handles non-existent username gracefully."""
        mock_conn = AsyncMock()
        mock_connection.return_value.__aenter__.return_value = mock_conn
        mock_conn.fetch_all = AsyncMock(return_value=[])

        mock_parse_mentions.return_value = ["nonexistent_user"]
        mock_get_user_by_username.side_effect = NotFound("User not found")

        await MessageService.send_message_after_chat(
            chat_from=1,
            chat="Hey @nonexistent_user",
            project_id=1,
            project_name="Test Project"
        )

        # No exception should be raised

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    @patch("backend.services.messaging.message_service.Project.get_project_title")
    async def test_get_all_messages_with_project_filter(
        self, mock_get_title, mock_fetch_one, mock_fetch_all
    ):
        """Test get_all_messages with project filter."""
        mock_fetch_all.return_value = [
            {
                "message_id": 1,
                "subject": "Test",
                "message": "Body",
                "from_user_id": 2,
                "to_user_id": 1,
                "task_id": None,
                "message_type": 1,
                "sent_date": datetime.utcnow(),
                "read": False,
                "project_id": 1,
                "from_username": "sender",
                "display_picture_url": None
            }
        ]
        mock_fetch_one.return_value = {"total_count": 1}
        mock_get_title.return_value = "Test Project"

        res = await MessageService.get_all_messages(
            db=self.db,
            user_id=1,
            locale="en",
            page=1,
            project=1,
        )

        assert len(res.user_messages) == 1
        assert res.pagination.total == 1

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    @patch("backend.services.messaging.message_service.Project.get_project_title")
    async def test_get_all_messages_with_message_type_filter(
        self, mock_get_title, mock_fetch_one, mock_fetch_all
    ):
        """Test get_all_messages with message_type filter."""
        mock_fetch_all.return_value = [
            {
                "message_id": 1,
                "subject": "Test",
                "message": "Body",
                "from_user_id": 2,
                "to_user_id": 1,
                "task_id": None,
                "message_type": 1,
                "sent_date": datetime.utcnow(),
                "read": False,
                "project_id": 1,
                "from_username": "sender",
                "display_picture_url": None
            }
        ]
        mock_fetch_one.return_value = {"total_count": 1}
        mock_get_title.return_value = "Test Project"

        res = await MessageService.get_all_messages(
            db=self.db,
            user_id=1,
            locale="en",
            page=1,
            message_type="1",
        )

        assert len(res.user_messages) == 1
        assert res.pagination.total == 1

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    @patch("backend.services.messaging.message_service.Project.get_project_title")
    async def test_get_all_messages_with_from_username_filter(
        self, mock_get_title, mock_fetch_one, mock_fetch_all
    ):
        """Test get_all_messages with from_username filter."""
        mock_fetch_all.return_value = [
            {
                "message_id": 1,
                "subject": "Test",
                "message": "Body",
                "from_user_id": 2,
                "to_user_id": 1,
                "task_id": None,
                "message_type": 1,
                "sent_date": datetime.utcnow(),
                "read": False,
                "project_id": 1,
                "from_username": "sender",
                "display_picture_url": None
            }
        ]
        mock_fetch_one.return_value = {"total_count": 1}
        mock_get_title.return_value = "Test Project"

        res = await MessageService.get_all_messages(
            db=self.db,
            user_id=1,
            locale="en",
            page=1,
            from_username="sender",
        )

        assert len(res.user_messages) == 1
        assert res.pagination.total == 1

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_all_tasks_mappers_empty(self, mock_fetch_all):
        """Test get_all_tasks_mappers returns empty list when no mappers."""
        mock_fetch_all.return_value = []

        mappers = await MessageService.get_all_tasks_mappers(1, 1, self.db)

        assert mappers == []

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_all_project_mappers_empty(self, mock_fetch_all):
        """Test get_all_project_mappers returns empty list when no mappers."""
        mock_fetch_all.return_value = []

        mappers = await MessageService.get_all_project_mappers(1, self.db)

        assert mappers == []

    @patch("backend.services.messaging.message_service.db_connection.database.connection")
    @patch("backend.services.messaging.message_service.Message.get_all_contributors")
    @patch("backend.services.messaging.message_service.Project.get")
    @patch("backend.services.messaging.message_service.ProjectInfo.get_dto_for_locale")
    @patch("backend.services.messaging.message_service.Message.from_dto")
    @patch("backend.services.messaging.message_service.UserService.get_user_by_id")
    @patch("backend.services.messaging.message_service.MessageService._push_messages")
    async def test_send_message_to_all_contributors_success(
        self, mock_push, mock_get_user, mock_from_dto, mock_project_info,
        mock_project_get, mock_get_contributors, mock_connection
    ):
        """Test send_message_to_all_contributors sends message to all contributors."""
        mock_conn = AsyncMock()
        mock_connection.return_value.__aenter__.return_value = mock_conn

        mock_get_contributors.return_value = [1, 2, 3]
        mock_project_get.return_value = MagicMock(default_locale="en")
        mock_project_info.return_value = MagicMock(name="Test Project")
        mock_from_dto.return_value = MagicMock(
            message_type=MessageType.BROADCAST.value,
            project_id=1
        )
        mock_get_user.return_value = MagicMock(id=1)

        with patch("backend.services.messaging.message_service.MessageDTO") as mock_message_dto:
            mock_message_dto.return_value = MagicMock()
            message_dto = MagicMock()
            message_dto.message = "Test message"

            await MessageService.send_message_to_all_contributors(1, message_dto)

            mock_push.assert_called()


