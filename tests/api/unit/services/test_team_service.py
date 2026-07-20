import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from backend.exceptions import NotFound
from backend.models.dtos.team_dto import TeamSearchDTO, TeamDTO
from backend.models.postgis.statuses import TeamJoinMethod, TeamRoles, TeamMemberFunctions
from backend.services.team_service import TeamService, TeamServiceError
from backend.models.postgis.team import Team
from tests.api.helpers.test_helpers import create_canned_team, create_canned_user, create_canned_organisation


@pytest.mark.anyio
class TestTeamService:
    @pytest.fixture(autouse=True)
    async def setup_test_data(self, db_connection_fixture, request):
        """Fixture to set up test data before running tests."""
        assert db_connection_fixture is not None, "Database connection is not available"

        request.cls.test_user = await create_canned_user(db_connection_fixture)
        request.cls.test_team = await create_canned_team(db_connection_fixture)
        request.cls.db = db_connection_fixture

        assert self.test_user is not None, "Failed to create test user"
        assert self.test_team is not None, "Failed to create test team"

    async def test_search_team(self):
        """Test searching for a team."""
        team_search_dto = TeamSearchDTO(
            user_id=self.test_user.id,
            team_name=self.test_team.name,
            # member=self.test_user.id,
            organisation=self.test_team.organisation_id,
        )
        result = await TeamService.get_all_teams(team_search_dto, self.db)

        assert len(result.teams) == 1
        assert result.teams[0].team_id == self.test_team.id
        assert result.teams[0].name == self.test_team.name
        assert result.teams[0].organisation_id == self.test_team.organisation_id

    async def test_get_team_as_dto(self):
        """Test fetching a team as DTO."""
        result = await TeamService.get_team_as_dto(
            self.test_team.id, self.test_user.id, False, self.db
        )
        assert result.team_id == self.test_team.id

    async def test_add_team_project(self, db_connection_fixture):
        """Test adding a user to a team."""
        await TeamService.add_team_member(
            self.test_team.id, self.test_user.id, 1, active=True, db=self.db
        )
        is_active = await TeamService.is_user_an_active_team_member(
            self.test_team.id, self.test_user.id, self.db
        )
        assert is_active

    async def test_delete_team_project(self, db_connection_fixture):
        """Test deleting a team."""
        await TeamService.delete_team(self.test_team.id, self.db)
        with pytest.raises(NotFound):
            await TeamService.get_team_by_id(self.test_team.id, self.db)

    async def test_leave_team(self, db_connection_fixture):
        """Test leaving a team."""
        await TeamService.add_team_member(
            self.test_team.id, self.test_user.id, 1, active=True, db=self.db
        )
        await TeamService.leave_team(
            self.test_team.id, self.test_user.username, self.db
        )
        is_active = await TeamService.is_user_an_active_team_member(
            self.test_team.id, self.test_user.id, self.db
        )
        assert not is_active

    async def test_add_member_unauthorized(self, db_connection_fixture):
        """Valida que un usuario sin privilegios falle al intentar validarse como manager."""
        from backend.services.team_service import TeamService

        # El usuario no forma parte de ningún equipo en el proyecto 1
        is_member = await TeamService.check_team_membership(
            1, [1], self.test_user.id, self.db
        )
        assert not is_member

    async def test_delete_team_relational_integrity(self, db_connection_fixture):
        """Valida protección contra el borrado de equipos vinculados a proyectos."""
        from backend.services.team_service import TeamService
        from tests.api.helpers.test_helpers import create_canned_project

        # Crear proyecto ficticio
        project, user, project_id = await create_canned_project(self.db)

        # Vincular equipo al proyecto
        await TeamService.add_team_project(self.test_team.id, project_id, "MAPPER", self.db)

        # Intentar borrar el equipo, debe retornar JSONResponse con 400
        response = await TeamService.delete_team(self.test_team.id, self.db)
        assert response.status_code == 400
        import json
        body = json.loads(response.body)
        assert "Team has projects, cannot be deleted" in body["Error"]

    @patch.object(Team, "get_team_by_name")
    async def test_get_team_by_name(self, mock_get_team):
        """Valida la obtención de un equipo por nombre."""
        mock_get_team.return_value = {"id": self.test_team.id, "name": self.test_team.name}

        team = await TeamService.get_team_by_name(self.test_team.name)
        assert team["id"] == self.test_team.id

    async def test_is_user_team_manager_as_org_admin(self):
        """Valida que un manager de la organización es manager del equipo."""
        # Hacer al usuario manager de la organización del equipo
        query = "INSERT INTO organisation_managers (organisation_id, user_id) VALUES (:org_id, :user_id)"
        await self.db.execute(query, {"org_id": self.test_team.organisation_id, "user_id": self.test_user.id})

        is_manager = await TeamService.is_user_team_manager(self.test_team.id, self.test_user.id, self.db)
        assert is_manager is True

    async def test_request_to_join_team_auto_approve(self):
        """Valida unión automática para JoinMethod.ANY."""
        # Configurar equipo como ANY
        await self.db.execute("UPDATE teams SET join_method = :jm WHERE id = :id", 
                              {"jm": TeamJoinMethod.ANY.value, "id": self.test_team.id})

        await TeamService.request_to_join_team(self.test_team.id, self.test_user.id, self.db)

        is_active = await TeamService.is_user_an_active_team_member(self.test_team.id, self.test_user.id, self.db)
        assert is_active is True

    async def test_accept_reject_join_request_reject(self):
        """Valida que rechazar una solicitud elimina al miembro."""
        # Crear solicitud (inactiva)
        await TeamService.add_team_member(self.test_team.id, self.test_user.id, 2, False, self.db)

        # Mock de MessageService para evitar envíos reales
        with patch("backend.services.team_service.MessageService.accept_reject_request_to_join_team", new_callable=AsyncMock):
            await TeamService.accept_reject_join_request(
                self.test_team.id, self.test_user.id, self.test_user.username, "member", "reject", self.db
            )

        is_member = await TeamService.is_user_team_member(self.test_team.id, self.test_user.id, self.db)
        assert is_member is False

    async def test_ensure_unlink_allowed_blocks_last_pm(self):
        """Previene dejar un proyecto sin Project Managers."""
        from tests.api.helpers.test_helpers import create_canned_project
        _, _, project_id = await create_canned_project(self.db)

        # Vincular el equipo como único PM
        await TeamService.add_team_project(self.test_team.id, project_id, "PROJECT_MANAGER", self.db)

        # Validar desvinculación
        response = await TeamService.ensure_unlink_allowed(project_id, self.test_team.id, self.db)
        assert response is not None
        assert response.status_code == 403
        assert "requires at least one project manager" in json.loads(response.body)["Error"]

    async def test_change_team_role(self):
        """Valida la actualización de roles de equipo en proyecto."""
        from tests.api.helpers.test_helpers import create_canned_project
        _, _, project_id = await create_canned_project(self.db)
        await TeamService.add_team_project(self.test_team.id, project_id, "MAPPER", self.db)

        await TeamService.change_team_role(self.test_team.id, project_id, "VALIDATOR", self.db)

        query = "SELECT role FROM project_teams WHERE team_id = :tid AND project_id = :pid"
        role = await self.db.fetch_val(query, {"tid": self.test_team.id, "pid": project_id})
        assert role == TeamRoles.VALIDATOR.value

    async def test_get_all_teams_with_pagination(self):
        """TC-TEA-008: Valida búsqueda con paginación y filtros."""
        search_dto = TeamSearchDTO(
            user_id=self.test_user.id,
            paginate=True,
            page=1,
            per_page=10
        )

        result = await TeamService.get_all_teams(search_dto, self.db)
        assert result.pagination is not None
        assert result.pagination.total >= 1

    async def test_update_team_basic(self):
        """Cubre el flujo de actualización de metadatos del equipo."""
        update_dto = TeamDTO(
            team_id=self.test_team.id,
            name="New Team Name",
            organisation_id=self.test_team.organisation_id,
            description="New Description",
            joinMethod="BY_INVITE",
            visibility="PRIVATE"
        )

        await TeamService.update_team(update_dto, self.db)

        updated = await TeamService.get_team_by_id(self.test_team.id, self.db)
        assert updated["name"] == "New Team Name"
        assert updated["join_method"] == TeamJoinMethod.BY_INVITE.value

    @patch("backend.services.team_service.db_connection")
    @patch("backend.services.team_service.MessageService._push_messages", new_callable=AsyncMock)
    async def test_send_message_to_all_team_members(self, mock_push, mock_db_conn):
        """Valida el envío masivo de mensajes a miembros del equipo."""
        mock_db_conn.database.connection.return_value.__aenter__.return_value = self.db

        # Agregar un miembro activo
        await TeamService.add_team_member(self.test_team.id, self.test_user.id, 2, True, self.db)

        from backend.models.dtos.message_dto import MessageDTO
        msg = MessageDTO(subject="Test", message="Hello", fromUserId=self.test_user.id)

        await TeamService.send_message_to_all_team_members(self.test_team.id, "TeamName", msg, self.test_user.id)

        # Verificar que se intentó pushear un mensaje
        assert mock_push.called

    async def test_add_user_to_team_as_manager(self):
        """Cubre add_user_to_team y validación de permisos de manager."""
        # Arrange:
        # Aseguramos que el usuario ejecutor (test_user) sea el MANAGER del equipo.
        await self.db.execute(
            """
            INSERT INTO team_members (team_id, user_id, function, active, join_request_notifications) 
            VALUES (:tid, :uid, 1, true, false)
            ON CONFLICT (team_id, user_id) 
            DO UPDATE SET function = 1, active = true, join_request_notifications = false
            """,
            {"tid": self.test_team.id, "uid": self.test_user.id}
        )

        # Creamos el usuario objetivo (el que será añadido) con todos los campos obligatorios.
        # Nota: mapping_level 1 suele ser el ID del nivel 'BEGINNER' creado por defecto.
        target_user_id = 888888
        target_username = "member_to_invite"

        await self.db.execute(
            """
            INSERT INTO users (
                id, username, role, mapping_level, tasks_mapped, tasks_validated, tasks_invalidated,
                default_editor, mentions_notifications, projects_comments_notifications, 
                projects_notifications, tasks_notifications, task_validation_notification, 
                task_invalidation_notification, tasks_comments_notifications, teams_announcement_notifications,
                is_email_verified, is_expert
            ) VALUES (
                :id, :username, 0, 1, 0, 0, 0, 
                'ID', true, false, true, true, true, true, false, true,
                false, false
            ) ON CONFLICT (id) DO NOTHING
            """,
            {"id": target_user_id, "username": target_username}
        )

        # Act: El manager (test_user) añade al nuevo usuario al equipo.
        # La firma es: add_user_to_team(team_id, requesting_user_id, username_to_add, role, db)
        await TeamService.add_user_to_team(
            self.test_team.id,
            self.test_user.id,
            target_username,
            "MEMBER",
            self.db
        )

        # Assert: Verificamos que el usuario ahora es miembro activo.
        is_member = await TeamService.is_user_an_active_team_member(
            self.test_team.id, target_user_id, self.db
        )
        assert is_member is True

    async def test_is_user_team_manager_as_admin(self):
        """Un Admin global debe ser siempre manager de equipo."""
        # Convertir al usuario en Admin global
        await self.db.execute("UPDATE users SET role = 1 WHERE id = :id", {"id": self.test_user.id})

        is_manager = await TeamService.is_user_team_manager(self.test_team.id, self.test_user.id, self.db)
        assert is_manager is True

    async def test_request_to_join_invite_only_team_fails(self):
        """Validar error al intentar unirse a equipo de solo invitación."""
        await self.db.execute("UPDATE teams SET join_method = :jm WHERE id = :id", 
                              {"jm": TeamJoinMethod.BY_INVITE.value, "id": self.test_team.id})

        with pytest.raises(TeamServiceError, match="Team join method is BY_INVITE"):
            await TeamService.request_to_join_team(self.test_team.id, self.test_user.id, self.db)

    async def test_add_user_to_team_update_existing_role(self):
        """Actualizar rol de un usuario que ya está en el equipo."""
        # Hacer al ejecutor manager
        await self.db.execute("INSERT INTO team_members (team_id, user_id, function, active, join_request_notifications) VALUES (:tid, :uid, 1, true, false)",
                              {"tid": self.test_team.id, "uid": self.test_user.id})

        # El usuario ya es manager, lo "añadimos" de nuevo como MEMBER
        response = await TeamService.add_user_to_team(self.test_team.id, self.test_user.id, self.test_user.username, "MEMBER", self.db)

        assert response.status_code == 200
        # Verificar cambio en DB
        role = await self.db.fetch_val("SELECT function FROM team_members WHERE user_id = :uid", {"uid": self.test_user.id})
        assert role == TeamMemberFunctions.MEMBER.value

    async def test_ensure_unlink_allowed_blocks_only_mapper_team(self):
        """Bloquea desvinculación si es el único equipo de mapeo en proyecto restringido."""
        from tests.api.helpers.test_helpers import create_canned_project
        _, _, project_id = await create_canned_project(self.db)

        # Restringir mapeo a equipos (MappingPermission.TEAMS = 2)
        await self.db.execute("UPDATE projects SET mapping_permission = 2 WHERE id = :id", {"id": project_id})
        # Vincular como equipo mapeador
        await TeamService.add_team_project(self.test_team.id, project_id, "MAPPER", self.db)

        response = await TeamService.ensure_unlink_allowed(project_id, self.test_team.id, self.db)
        assert response.status_code == 403
        assert "is the only mapper team" in json.loads(response.body)["Error"]

    async def test_ensure_unlink_allowed_blocks_only_validator_team(self):
        """Bloquea desvinculación si es el único equipo de validación."""
        from tests.api.helpers.test_helpers import create_canned_project
        _, _, project_id = await create_canned_project(self.db)

        # Restringir validación a equipos (ValidationPermission.TEAMS = 2)
        await self.db.execute("UPDATE projects SET validation_permission = 2 WHERE id = :id", {"id": project_id})
        await TeamService.add_team_project(self.test_team.id, project_id, "VALIDATOR", self.db)

        response = await TeamService.ensure_unlink_allowed(project_id, self.test_team.id, self.db)
        assert response.status_code == 403
        assert "is the only validator team" in json.loads(response.body)["Error"]

    async def test_search_teams_by_member_request(self):
        """Filtrar equipos donde el usuario tiene una solicitud pendiente."""
        # Crear solicitud inactiva
        await TeamService.add_team_member(self.test_team.id, self.test_user.id, 2, False, self.db)

        search_dto = TeamSearchDTO(user_id=self.test_user.id, member_request=self.test_user.id)
        result = await TeamService.get_all_teams(search_dto, self.db)

        assert len(result.teams) == 1
        assert result.teams[0].team_id == self.test_team.id

    async def test_unlink_team_success(self):
        """Valida la desvinculación efectiva de un equipo y un proyecto."""
        from tests.api.helpers.test_helpers import create_canned_project
        _, _, project_id = await create_canned_project(self.db)

        # Vincular
        await TeamService.add_team_project(self.test_team.id, project_id, "MAPPER", self.db)

        # Act: Llamamos al método real del Service
        result = await TeamService.unlink_team(project_id, self.test_team.id, self.db)

        # Assert
        assert result is True
        count = await self.db.fetch_val("SELECT COUNT(*) FROM project_teams WHERE project_id = :pid", {"pid": project_id})
        assert count == 0

    async def test_ensure_unlink_allowed_project_not_found(self):
        """Cubre la rama de error cuando el proyecto no existe."""
        response = await TeamService.ensure_unlink_allowed(99999, self.test_team.id, self.db)
        assert response.status_code == 404
        assert "not found" in json.loads(response.body)["Error"]

    async def test_ensure_unlink_allowed_team_not_linked(self):
        """Cubre la rama de error cuando el equipo no está vinculado al proyecto."""
        from tests.api.helpers.test_helpers import create_canned_project
        _, _, project_id = await create_canned_project(self.db)

        response = await TeamService.ensure_unlink_allowed(project_id, self.test_team.id, self.db)
        assert response.status_code == 404
        assert "no such linked team" in json.loads(response.body)["Error"]

    async def test_activate_team_member_success(self):
        """Ejercita el método activate_team_member."""
        # Crear miembro inactivo
        await TeamService.add_team_member(self.test_team.id, self.test_user.id, 2, False, self.db)

        # Act
        await TeamService.activate_team_member(self.test_team.id, self.test_user.id, self.db)

        # Assert
        is_active = await TeamService.is_user_an_active_team_member(self.test_team.id, self.test_user.id, self.db)
        assert is_active is True

    async def test_get_projects_by_team_id(self):
        """Ejercita la recuperación de proyectos vinculados a un equipo."""
        from tests.api.helpers.test_helpers import create_canned_project
        _, _, project_id = await create_canned_project(self.db)
        await TeamService.add_team_project(self.test_team.id, project_id, "MAPPER", self.db)

        projects = await TeamService.get_projects_by_team_id(self.test_team.id, self.db)
        assert len(projects) > 0
        assert projects[0]["project_id"] == project_id
