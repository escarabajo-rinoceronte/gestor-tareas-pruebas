import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

from backend.models.dtos.message_dto import ChatMessageDTO, ProjectChatDTO, ListChatMessageDTO, Pagination
from backend.services.messaging.chat_service import ChatService
from backend.exceptions import NotFound

@pytest.mark.anyio
class TestChatService:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, request):
        request.cls.mock_db = AsyncMock()
        request.cls.mock_background_tasks = MagicMock()

    @patch("backend.services.messaging.chat_service.ProjectService")
    @patch("backend.services.messaging.chat_service.ProjectInfo")
    @patch("backend.services.messaging.chat_service.ProjectAdminService")
    @patch("backend.services.messaging.chat_service.ProjectChat")
    async def test_post_message_permitted(self, mock_project_chat, mock_admin, mock_project_info, mock_project_service):
        """Test posting a chat message when user is permitted."""
        # Setup mocks
        mock_project = MagicMock()
        mock_project.status = 1 # PUBLISHED
        mock_project.private = False
        mock_project_service.get_project_by_id = AsyncMock(return_value=mock_project)
        mock_project_info.get_dto_for_locale = AsyncMock(return_value=MagicMock(name="Test Project"))
        mock_admin.is_user_action_permitted_on_project = AsyncMock(return_value=True)
        
        # Simular creación exitosa
        mock_project_chat.create_from_dto = AsyncMock(return_value=MagicMock(message="Hello"))
        
        # CORRECCIÓN: Inicialización manual del DTO para evitar el TypeError del __init__
        mock_returned_dto = ProjectChatDTO()
        mock_returned_dto.chat = []
        mock_returned_dto.pagination = None
        mock_project_chat.get_messages = AsyncMock(return_value=mock_returned_dto)
        
        dto = ChatMessageDTO(message="Hello", project_id=1, user_id=1, timestamp=datetime.utcnow(), username="test")
        result = await ChatService.post_message(dto, 1, 1, self.mock_db, self.mock_background_tasks)
        
        assert result == mock_returned_dto
        self.mock_background_tasks.add_task.assert_called_once()

    @patch("backend.services.messaging.chat_service.ProjectService")
    @patch("backend.services.messaging.chat_service.ProjectInfo")
    @patch("backend.services.messaging.chat_service.ProjectAdminService")
    @patch("backend.services.messaging.chat_service.TeamService")
    async def test_post_message_private_forbidden(self, mock_team, mock_admin, mock_project_info, mock_project_service):
        """Test que falla si el proyecto es privado y el usuario no tiene acceso."""
        # Setup mock project
        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.status = 1 # PUBLISHED
        mock_project.private = True 
        mock_project.default_locale = "en"
        mock_project_service.get_project_by_id = AsyncMock(return_value=mock_project)
        
        # Setup mock info (necesario porque el servicio lo llama antes de validar el acceso)
        mock_project_info.get_dto_for_locale = AsyncMock(return_value=MagicMock(name="Test"))
        
        # Forzamos que todas las validaciones de permiso devuelvan False
        mock_admin.is_user_action_permitted_on_project = AsyncMock(return_value=False)
        mock_team.check_team_membership = AsyncMock(return_value=False)
        
        # Simulamos que la tabla de usuarios permitidos está vacía (Record mockeado)
        self.mock_db.fetch_all.return_value = [] 
        
        dto = ChatMessageDTO(message="Hi", project_id=1, user_id=1, timestamp=datetime.utcnow(), username="t")
        
        # Ahora el match "UserNotPermitted" sí debería encontrar la excepción lanzada en el backend
        with pytest.raises(ValueError, match="UserNotPermitted"):
            await ChatService.post_message(dto, 1, 1, self.mock_db, self.mock_background_tasks)

    async def test_get_project_chat_by_id_not_found(self):
        with patch("backend.services.messaging.chat_service.ProjectService.exists", AsyncMock()):
            self.mock_db.fetch_one.return_value = None
            with pytest.raises(NotFound):
                await ChatService.get_project_chat_by_id(1, 99, self.mock_db)

    @patch("backend.services.messaging.chat_service.ProjectAdminService")
    async def test_delete_project_chat_by_id_forbidden(self, mock_admin):
        """Test que valida que un usuario no puede borrar mensajes ajenos."""
        with patch("backend.services.messaging.chat_service.ProjectService.exists", AsyncMock()):
            # El mensaje pertenece al usuario 2
            self.mock_db.fetch_one.return_value = {"user_id": 2}
            # El usuario que intenta borrar es el 1 y no es admin del proyecto
            mock_admin.is_user_action_permitted_on_project = AsyncMock(return_value=False)
            
            with pytest.raises(ValueError, match="DeletePermissionError"):
                await ChatService.delete_project_chat_by_id(1, 1, 1, self.mock_db)

    @patch("backend.services.messaging.chat_service.ProjectChat")
    async def test_get_messages_delegation(self, mock_project_chat):
        """Valida que el servicio delegue correctamente al modelo."""
        mock_project_chat.get_messages = AsyncMock(return_value=ProjectChatDTO())
        await ChatService.get_messages(1, self.mock_db, 1, 10)
        mock_project_chat.get_messages.assert_called_with(1, self.mock_db, 1, 10)


    @patch("backend.services.messaging.chat_service.ProjectService")
    @patch("backend.services.messaging.chat_service.ProjectInfo")
    @patch("backend.services.messaging.chat_service.ProjectAdminService")
    @patch("backend.services.messaging.chat_service.TeamService")
    @patch("backend.services.messaging.chat_service.ProjectChat")
    async def test_post_message_private_project_team_member_allowed(self, mock_project_chat, mock_team, mock_admin, mock_project_info, mock_project_service):
        """Test que permite postear en proyecto privado si es miembro del equipo."""
        # Setup mock project privado
        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.status = 1  # PUBLISHED
        mock_project.private = True
        mock_project.default_locale = "en"
        mock_project_service.get_project_by_id = AsyncMock(return_value=mock_project)
        mock_project_info.get_dto_for_locale = AsyncMock(return_value=MagicMock(name="Test Project"))
        
        # Usuario NO es manager pero SÍ es miembro del equipo
        mock_admin.is_user_action_permitted_on_project = AsyncMock(return_value=False)
        mock_team.check_team_membership = AsyncMock(return_value=True)
        
        # Simular creación exitosa
        mock_project_chat.create_from_dto = AsyncMock(return_value=MagicMock(message="Hello"))
        
        mock_returned_dto = ProjectChatDTO()
        mock_returned_dto.chat = []
        mock_returned_dto.pagination = None
        mock_project_chat.get_messages = AsyncMock(return_value=mock_returned_dto)

        dto = ChatMessageDTO(
            message="Hello", 
            project_id=1, 
            user_id=1, 
            timestamp=datetime.utcnow(), 
            username="test"
        )
        
        result = await ChatService.post_message(dto, 1, 1, self.mock_db, self.mock_background_tasks)
        
        assert result == mock_returned_dto
        mock_team.check_team_membership.assert_called_once()
        self.mock_background_tasks.add_task.assert_called_once()

    @patch("backend.services.messaging.chat_service.ProjectService")
    @patch("backend.services.messaging.chat_service.ProjectInfo")
    @patch("backend.services.messaging.chat_service.ProjectAdminService")
    @patch("backend.services.messaging.chat_service.TeamService")
    @patch("backend.services.messaging.chat_service.ProjectChat")
    async def test_post_message_private_project_allowed_user(self, mock_project_chat, mock_team, mock_admin, mock_project_info, mock_project_service):
        """Test que permite postear en proyecto privado si está en lista de usuarios permitidos."""
        # Setup mock project privado
        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.status = 1  # PUBLISHED
        mock_project.private = True
        mock_project.default_locale = "en"
        mock_project_service.get_project_by_id = AsyncMock(return_value=mock_project)
        mock_project_info.get_dto_for_locale = AsyncMock(return_value=MagicMock(name="Test Project"))
        
        # Usuario NO es manager, NO es miembro del equipo, pero está en allowed_users
        mock_admin.is_user_action_permitted_on_project = AsyncMock(return_value=False)
        mock_team.check_team_membership = AsyncMock(return_value=False)
        
        # Simular que el usuario está en la tabla project_allowed_users
        self.mock_db.fetch_all.return_value = [{"user_id": 1}]
        
        # Simular creación exitosa
        mock_project_chat.create_from_dto = AsyncMock(return_value=MagicMock(message="Hello"))
        
        mock_returned_dto = ProjectChatDTO()
        mock_returned_dto.chat = []
        mock_returned_dto.pagination = None
        mock_project_chat.get_messages = AsyncMock(return_value=mock_returned_dto)

        dto = ChatMessageDTO(
            message="Hello", 
            project_id=1, 
            user_id=1, 
            timestamp=datetime.utcnow(), 
            username="test"
        )
        
        result = await ChatService.post_message(dto, 1, 1, self.mock_db, self.mock_background_tasks)
        
        assert result == mock_returned_dto
        self.mock_db.fetch_all.assert_called_once()
        self.mock_background_tasks.add_task.assert_called_once()

    @patch("backend.services.messaging.chat_service.ProjectService")
    @patch("backend.services.messaging.chat_service.ProjectInfo")
    @patch("backend.services.messaging.chat_service.ProjectAdminService")
    @patch("backend.services.messaging.chat_service.ProjectChat")
    async def test_post_message_manager_permission(self, mock_project_chat, mock_admin, mock_project_info, mock_project_service):
        """Test que permite postear si el usuario es manager del proyecto."""
        # Setup mock project
        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.status = 1  # PUBLISHED
        mock_project.private = True
        mock_project.default_locale = "en"
        mock_project_service.get_project_by_id = AsyncMock(return_value=mock_project)
        mock_project_info.get_dto_for_locale = AsyncMock(return_value=MagicMock(name="Test Project"))
        
        # Usuario es manager
        mock_admin.is_user_action_permitted_on_project = AsyncMock(return_value=True)
        
        # Simular creación exitosa
        mock_project_chat.create_from_dto = AsyncMock(return_value=MagicMock(message="Hello"))
        
        mock_returned_dto = ProjectChatDTO()
        mock_returned_dto.chat = []
        mock_returned_dto.pagination = None
        mock_project_chat.get_messages = AsyncMock(return_value=mock_returned_dto)

        dto = ChatMessageDTO(
            message="Hello", 
            project_id=1, 
            user_id=1, 
            timestamp=datetime.utcnow(), 
            username="test"
        )
        
        result = await ChatService.post_message(dto, 1, 1, self.mock_db, self.mock_background_tasks)
        
        assert result == mock_returned_dto
        mock_admin.is_user_action_permitted_on_project.assert_called_once()
        self.mock_background_tasks.add_task.assert_called_once()

    @patch("backend.services.messaging.chat_service.ProjectService")
    @patch("backend.services.messaging.chat_service.ProjectAdminService")
    async def test_delete_message_owner_allowed(self, mock_admin, mock_project_service):
        """Test que permite borrar un mensaje si el usuario es el propietario."""
        mock_project_service.exists = AsyncMock(return_value=True)
        # El mensaje pertenece al usuario 1 (el que intenta borrar)
        self.mock_db.fetch_one.return_value = {"user_id": 1}
        # No es admin
        mock_admin.is_user_action_permitted_on_project = AsyncMock(return_value=False)
        
        result = await ChatService.delete_project_chat_by_id(1, 1, 1, self.mock_db)
        
        assert result is None
        self.mock_db.execute.assert_called_once()

    @patch("backend.services.messaging.chat_service.ProjectService")
    @patch("backend.services.messaging.chat_service.ProjectAdminService")
    async def test_delete_message_admin_allowed(self, mock_admin, mock_project_service):
        """Test que permite borrar un mensaje si el usuario es admin del proyecto."""
        mock_project_service.exists = AsyncMock(return_value=True)
        # El mensaje pertenece al usuario 2 (otro usuario)
        self.mock_db.fetch_one.return_value = {"user_id": 2}
        # El usuario 1 es admin
        mock_admin.is_user_action_permitted_on_project = AsyncMock(return_value=True)
        
        result = await ChatService.delete_project_chat_by_id(1, 1, 1, self.mock_db)
        
        assert result is None
        self.mock_db.execute.assert_called_once()
        mock_admin.is_user_action_permitted_on_project.assert_called_once()

    @patch("backend.services.messaging.chat_service.ProjectService")
    async def test_delete_message_project_not_found(self, mock_project_service):
        """Test que lanza NotFound si el proyecto no existe."""
        mock_project_service.exists = AsyncMock(side_effect=NotFound(sub_code="PROJECT_NOT_FOUND", project_id=999))
        
        with pytest.raises(NotFound, match="PROJECT_NOT_FOUND"):
            await ChatService.delete_project_chat_by_id(999, 1, 1, self.mock_db)

    @patch("backend.services.messaging.chat_service.ProjectService")
    async def test_delete_message_not_found(self, mock_project_service):
        """Test que lanza NotFound si el mensaje no existe."""
        mock_project_service.exists = AsyncMock(return_value=True)
        self.mock_db.fetch_one.return_value = None
        
        with pytest.raises(NotFound, match="MESSAGE_NOT_FOUND"):
            await ChatService.delete_project_chat_by_id(1, 999, 1, self.mock_db)

    @patch("backend.services.messaging.chat_service.ProjectService")
    async def test_get_project_chat_by_id_success(self, mock_project_service):
        """Test que recupera un mensaje específico correctamente."""
        mock_project_service.exists = AsyncMock(return_value=True)
        mock_message = {
            "id": 1,
            "project_id": 1,
            "user_id": 1,
            "message": "Hello",
            "timestamp": datetime.utcnow()
        }
        self.mock_db.fetch_one.return_value = mock_message
        
        result = await ChatService.get_project_chat_by_id(1, 1, self.mock_db)
        
        assert result == mock_message
        self.mock_db.fetch_one.assert_called_once()

    @patch("backend.services.messaging.chat_service.ProjectService")
    async def test_get_messages_success(self, mock_project_service):
        """Test que recupera los mensajes del proyecto correctamente."""
        mock_project_service.exists = AsyncMock(return_value=True)
        
        with patch("backend.services.messaging.chat_service.ProjectChat.get_messages") as mock_get_messages:
            mock_returned_dto = ProjectChatDTO()
            mock_returned_dto.chat = []
            mock_returned_dto.pagination = None
            mock_get_messages.return_value = mock_returned_dto
            
            result = await ChatService.get_messages(1, self.mock_db, 1, 10)
            
            assert result == mock_returned_dto
            mock_get_messages.assert_called_with(1, self.mock_db, 1, 10)

    @patch("backend.services.messaging.chat_service.ProjectService")
    async def test_get_messages_project_not_found(self, mock_project_service):
        """Test que el servicio delega en ProjectChat incluso si el proyecto no existe."""
        mock_project_service.exists = AsyncMock(return_value=False)
        
        with patch("backend.services.messaging.chat_service.ProjectChat.get_messages") as mock_get_messages:
            mock_returned_dto = ProjectChatDTO()
            mock_returned_dto.chat = []
            mock_returned_dto.pagination = None
            mock_get_messages.return_value = mock_returned_dto
            
            # El servicio actual no verifica existencia, solo delega
            result = await ChatService.get_messages(999, self.mock_db, 1, 10)
            
            mock_get_messages.assert_called_with(999, self.mock_db, 1, 10)
            assert result == mock_returned_dto