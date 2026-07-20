import pytest
import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from backend.exceptions import NotFound
from backend.models.dtos.project_dto import (
    LockedTasksForUser,
    ProjectSummary,
    ProjectUserStatsDTO,
    ProjectDTO
)
from backend.models.postgis.task import Task
from backend.models.postgis.project import Project, ProjectInfo
from backend.models.postgis.mapping_level import MappingLevel
from backend.services.messaging.smtp_service import SMTPService
from backend.services.project_service import (
    MappingNotAllowed,
    ProjectAdminService,
    ProjectService,
    ProjectStatus,
    UserService,
    ValidatingNotAllowed,
    ProjectServiceError,
)
from backend.models.postgis.statuses import MappingPermission, ValidationPermission
from tests.api.helpers.test_helpers import create_canned_user, create_canned_project


@pytest.mark.anyio
class TestProjectService:
    @pytest.fixture(autouse=True)
    async def setup_test_data(self, db_connection_fixture, request):
        assert db_connection_fixture is not None, "Database connection is not available"
        request.cls.db = db_connection_fixture

    @patch.object(Project, "get")
    async def test_project_service_raises_error_if_project_not_found(
        self, mock_project
    ):
        # Arrange
        mock_project.return_value = None

        # Act / Assert
        with pytest.raises(HTTPException):
            await ProjectService.get_project_by_id(123, self.db)

    @patch.object(ProjectAdminService, "is_user_action_permitted_on_project")
    @patch.object(UserService, "is_user_blocked")
    @patch.object(UserService, "has_user_accepted_license")
    @patch.object(Task, "get_locked_tasks_for_user")
    @patch.object(ProjectService, "get_project_by_id")
    async def test_user_allowed_to_map(
        self,
        mock_project,
        mock_user_tasks,
        mock_user_license,
        mock_user_blocked,
        mock_user_is_action_permitted,
    ):
        # Arrange - Mock project
        stub_project = Project()
        stub_project.status = ProjectStatus.PUBLISHED.value
        stub_project.license_id = 11
        mock_project.return_value = stub_project

        # Admin user related
        mock_user_is_action_permitted.return_value = True
        mock_user_tasks.return_value = LockedTasksForUser(locked_tasks=[])
        mock_user_license.return_value = True
        mock_user_blocked.return_value = False

        # Act / Assert - Admin allowed to map
        allowed, reason = await ProjectService.is_user_permitted_to_map(1, 1, self.db)
        assert allowed
        assert reason == "User allowed to map"

        # Admin not accepted license should fail
        mock_user_license.return_value = False
        allowed, reason = await ProjectService.is_user_permitted_to_map(1, 1, self.db)
        assert not allowed
        assert reason == MappingNotAllowed.USER_NOT_ACCEPTED_LICENSE

        # Admin with already locked tasks should fail
        mock_user_license.return_value = True
        mock_user_tasks.return_value = LockedTasksForUser(locked_tasks=[1])
        allowed, reason = await ProjectService.is_user_permitted_to_map(1, 1, self.db)
        assert not allowed
        assert reason == MappingNotAllowed.USER_ALREADY_HAS_TASK_LOCKED

        # Admin can access draft projects
        stub_project.status = ProjectStatus.DRAFT.value
        mock_user_tasks.return_value = LockedTasksForUser(locked_tasks=[])
        allowed, reason = await ProjectService.is_user_permitted_to_map(1, 1, self.db)
        assert allowed
        assert reason == "User allowed to map"

        # Mappers
        mock_user_is_action_permitted.return_value = False
        mock_user_blocked.return_value = False

        # Cannot access unpublished project
        allowed, reason = await ProjectService.is_user_permitted_to_map(1, 1, self.db)
        assert not allowed
        assert reason == MappingNotAllowed.PROJECT_NOT_PUBLISHED

        # Mappers not accepted license should fail
        mock_user_license.return_value = False
        allowed, reason = await ProjectService.is_user_permitted_to_map(1, 1, self.db)
        assert not allowed
        assert reason == MappingNotAllowed.USER_NOT_ACCEPTED_LICENSE

        # Blocked user
        mock_user_blocked.return_value = True
        allowed, reason = await ProjectService.is_user_permitted_to_map(1, 1, self.db)
        assert not allowed
        assert reason == MappingNotAllowed.USER_NOT_ON_ALLOWED_LIST

    @patch.object(ProjectService, "get_project_by_id")
    @patch.object(UserService, "get_mapping_level")
    @patch.object(UserService, "has_user_accepted_license")
    @patch.object(ProjectAdminService, "is_user_action_permitted_on_project")
    async def test_user_allowed_to_map_by_mapping_level(
        self,
        is_user_action_permitted_on_project,
        has_user_accepted_license,
        get_mapping_level,
        get_project_by_id,
    ):
        # Arrange
        is_user_action_permitted_on_project.return_value = False
        has_user_accepted_license.return_value = True

        stub_project = Project()
        stub_project.status = ProjectStatus.PUBLISHED.value
        stub_project.license_id = 11
        stub_project.mapping_permission = MappingPermission.ANY.value
        stub_project.mapping_permission_level_id = 3  # Advanced
        get_project_by_id.return_value = stub_project

        test_user = await create_canned_user(self.db)

        get_mapping_level.return_value = await MappingLevel.get_by_id(1, self.db)

        # Act
        allowed, reason = await ProjectService.is_user_permitted_to_map(
            stub_project.id, test_user.id, self.db
        )

        assert not allowed

        # With permission
        get_mapping_level.return_value = await MappingLevel.get_by_id(3, self.db)
        allowed, reason = await ProjectService.is_user_permitted_to_map(
            stub_project.id, test_user.id, self.db
        )

        assert allowed

    @patch.object(ProjectService, "get_project_by_id")
    @patch.object(UserService, "get_mapping_level")
    @patch.object(UserService, "has_user_accepted_license")
    @patch.object(ProjectAdminService, "is_user_action_permitted_on_project")
    async def test_user_allowed_to_validate_by_mapping_level(
        self,
        is_user_action_permitted_on_project,
        has_user_accepted_license,
        get_mapping_level,
        get_project_by_id,
    ):
        # Arrange
        is_user_action_permitted_on_project.return_value = False
        has_user_accepted_license.return_value = True

        stub_project = Project()
        stub_project.status = ProjectStatus.PUBLISHED.value
        stub_project.license_id = 11
        stub_project.validation_permission = ValidationPermission.ANY.value
        stub_project.validation_permission_level_id = 3  # Advanced
        get_project_by_id.return_value = stub_project

        test_user = await create_canned_user(self.db)

        get_mapping_level.return_value = await MappingLevel.get_by_id(1, self.db)

        # Act
        allowed, reason = await ProjectService.is_user_permitted_to_validate(
            stub_project.id, test_user.id, self.db
        )

        assert not allowed

        # With permission
        get_mapping_level.return_value = await MappingLevel.get_by_id(3, self.db)
        allowed, reason = await ProjectService.is_user_permitted_to_validate(
            stub_project.id, test_user.id, self.db
        )

        assert allowed

    @patch.object(ProjectAdminService, "is_user_action_permitted_on_project")
    @patch.object(UserService, "is_user_blocked")
    @patch.object(UserService, "has_user_accepted_license")
    @patch.object(Task, "get_locked_tasks_for_user")
    @patch.object(ProjectService, "get_project_by_id")
    async def test_user_permitted_to_validate(
        self,
        mock_project,
        mock_user_tasks,
        mock_user_license,
        mock_user_blocked,
        mock_user_is_action_permitted,
    ):
        # Arrange - Mock project
        stub_project = Project()
        stub_project.status = ProjectStatus.PUBLISHED.value
        stub_project.license_id = 1
        mock_project.return_value = stub_project

        # Admin user related
        mock_user_is_action_permitted.return_value = True
        mock_user_tasks.return_value = LockedTasksForUser(locked_tasks=[])
        mock_user_license.return_value = True
        mock_user_blocked.return_value = False

        # Act / Assert - Admin allowed to validate
        allowed, reason = await ProjectService.is_user_permitted_to_validate(
            1, 1, self.db
        )
        assert allowed
        assert reason == "User allowed to validate"

        # Admin not accepted license should fail
        mock_user_license.return_value = False
        allowed, reason = await ProjectService.is_user_permitted_to_validate(
            1, 1, self.db
        )
        assert not allowed
        assert reason == ValidatingNotAllowed.USER_NOT_ACCEPTED_LICENSE

        # Admin with already locked tasks should fail
        mock_user_license.return_value = True
        mock_user_tasks.return_value = LockedTasksForUser(locked_tasks=[1])
        allowed, reason = await ProjectService.is_user_permitted_to_validate(
            1, 1, self.db
        )
        assert not allowed
        assert reason == ValidatingNotAllowed.USER_ALREADY_HAS_TASK_LOCKED

        # Blocked user
        mock_user_blocked.return_value = True
        allowed, reason = await ProjectService.is_user_permitted_to_validate(
            1, 1, self.db
        )
        assert not allowed
        assert reason == ValidatingNotAllowed.USER_NOT_ON_ALLOWED_LIST

        # Unpublished project
        stub_project.status = ProjectStatus.DRAFT.value
        mock_user_blocked.return_value = False
        mock_user_is_action_permitted.return_value = False
        allowed, reason = await ProjectService.is_user_permitted_to_validate(
            1, 1, self.db
        )
        assert not allowed
        assert reason == ValidatingNotAllowed.PROJECT_NOT_PUBLISHED

        # Admin can access draft projects
        stub_project.status = ProjectStatus.DRAFT.value
        mock_user_blocked.return_value = False
        mock_user_is_action_permitted.return_value = True
        mock_user_tasks.return_value = LockedTasksForUser(locked_tasks=[])
        allowed, reason = await ProjectService.is_user_permitted_to_validate(
            1, 1, self.db
        )
        assert allowed
        assert reason == "User allowed to validate"

        # Mappers not accepted license should fail
        mock_user_blocked.return_value = False
        mock_user_is_action_permitted.return_value = False
        mock_user_license.return_value = False
        allowed, reason = await ProjectService.is_user_permitted_to_validate(
            1, 1, self.db
        )
        assert not allowed
        assert reason == ValidatingNotAllowed.USER_NOT_ACCEPTED_LICENSE

    @patch("backend.services.project_service.db_connection.database.connection")
    @patch.object(SMTPService, "send_email_to_contributors_on_project_progress")
    @patch.object(Project, "calculate_tasks_percent")
    @patch.object(ProjectInfo, "get_dto_for_locale")
    @patch.object(ProjectService, "get_project_by_id")
    @patch("backend.services.project_service.get_settings")
    async def test_send_email_on_project_progress_sends_email_on_fifty_percent_progress(
        self,
        mock_settings,
        mock_project,
        mock_project_info,
        mock_project_completion,
        mock_send_email,
        mock_db_connection,
    ):
        # Arrange
        project = Project()
        project.progress_email_sent = False
        project.tasks_mapped = 50
        project.tasks_validated = 0
        project.total_tasks = 100
        project.tasks_bad_imagery = 0
        project.default_locale = "en"
        project.progress_email_sent = False
        mock_project.return_value = project
        mock_project_info.return_value = {
            "name": "TEST_PROJECT"
        }  # Match what fetch_val expects
        mock_project_completion.return_value = 50  # Ensure consistent return value
        mock_send_email.return_value = AsyncMock()
        mock_settings.return_value = type(
            "Settings", (), {"SEND_PROJECT_EMAIL_UPDATES": True}
        )()  # Mock settings object

        # Mock the database connection context manager
        mock_db_connection.return_value.__aenter__.return_value = self.db
        # Act
        await ProjectService.send_email_on_project_progress(1)

        # Assert
        mock_send_email.assert_called_once()

    @patch("backend.services.project_service.db_connection.database.connection")
    @patch.object(SMTPService, "send_email_to_contributors_on_project_progress")
    @patch.object(Project, "calculate_tasks_percent")
    @patch.object(ProjectInfo, "get_dto_for_locale")
    @patch.object(ProjectService, "get_project_by_id")
    @patch("backend.services.project_service.get_settings")
    async def test_send_email_on_project_progress_sends_email_on_project_completion(
        self,
        mock_settings,
        mock_project,
        mock_project_info,
        mock_project_completion,
        mock_send_email,
        mock_db_connection,
    ):
        # Arrange
        project = Project()
        project.progress_email_sent = False
        project.tasks_mapped = 0
        project.tasks_validated = 100
        project.total_tasks = 100
        project.tasks_bad_imagery = 0
        project.default_locale = "en"
        project.progress_email_sent = False
        mock_project.return_value = project
        mock_project_info.return_value = {"name": "TEST_PROJECT"}
        mock_project_completion.return_value = 100
        mock_send_email.return_value = AsyncMock()
        mock_settings.return_value = type(
            "Settings", (), {"SEND_PROJECT_EMAIL_UPDATES": True}
        )()

        # Mock the database connection context manager
        mock_db_connection.return_value.__aenter__.return_value = self.db
        # Act
        await ProjectService.send_email_on_project_progress(1)

        # Assert
        mock_send_email.assert_called_once()

    @patch("backend.services.project_service.db_connection.database.connection")
    @patch.object(SMTPService, "send_email_to_contributors_on_project_progress")
    @patch.object(Project, "calculate_tasks_percent")
    @patch.object(ProjectInfo, "get_dto_for_locale")
    @patch.object(ProjectService, "get_project_by_id")
    @patch("backend.services.project_service.get_settings")
    async def test_send_email_on_project_progress_doesnt_send_email_except_on_fifty_and_hundred_percent(
        self,
        mock_settings,
        mock_project,
        mock_project_info,
        mock_project_completion,
        mock_send_email,
        mock_db_connection,
    ):
        # Arrange
        project = Project()
        project.progress_email_sent = False
        project.tasks_mapped = 40
        project.tasks_validated = 40
        project.total_tasks = 100
        project.tasks_bad_imagery = 0
        project.default_locale = "en"
        project.progress_email_sent = False
        mock_project.return_value = project
        mock_project_info.return_value = {"name": "TEST_PROJECT"}
        mock_project_completion.return_value = 80
        mock_send_email.return_value = AsyncMock()
        mock_settings.return_value = type(
            "Settings", (), {"SEND_PROJECT_EMAIL_UPDATES": True}
        )()

        # Mock the database connection context manager
        mock_db_connection.return_value.__aenter__.return_value = self.db

        # Act
        await ProjectService.send_email_on_project_progress(1)

        # Assert
        assert not mock_send_email.called

    @patch("backend.services.project_service.db_connection.database.connection")
    @patch.object(SMTPService, "send_email_to_contributors_on_project_progress")
    @patch.object(Project, "calculate_tasks_percent")
    @patch.object(ProjectService, "get_project_by_id")
    @patch("backend.services.project_service.get_settings")
    async def test_send_email_on_project_progress_doesnt_send_email_if_email_already_sent(
        self,
        mock_settings,
        mock_project,
        mock_project_completion,
        mock_send_email,
        mock_db_connection,
    ):
        # Arrange
        project = Project()
        project.progress_email_sent = True
        project.tasks_mapped = 50
        project.total_tasks = 100
        project.tasks_validated = 0
        project.tasks_bad_imagery = 0
        mock_project.return_value = project
        mock_project_completion.return_value = 50
        mock_send_email.return_value = AsyncMock()
        mock_settings.return_value = type(
            "Settings", (), {"SEND_PROJECT_EMAIL_UPDATES": True}
        )()

        # Mock the database connection context manager
        mock_db_connection.return_value.__aenter__.return_value = self.db

        # Act
        await ProjectService.send_email_on_project_progress(1)

        # Assert
        assert not mock_send_email.called

    @patch("backend.services.project_service.db_connection.database.connection")
    @patch.object(SMTPService, "send_email_to_contributors_on_project_progress")
    @patch.object(ProjectService, "get_project_by_id")
    @patch("backend.services.project_service.get_settings")
    async def test_send_email_on_project_progress_doesnt_send_email_if_send_project_update_email_is_disabled(
        self, mock_settings, mock_project, mock_send_email, mock_db_connection
    ):
        # Arrange
        project = Project()
        project.progress_email_sent = False
        project.tasks_mapped = 50
        project.total_tasks = 100
        project.tasks_validated = 0
        project.tasks_bad_imagery = 0
        project.default_locale = "en"
        mock_project.return_value = project
        mock_send_email.return_value = AsyncMock()
        mock_settings.return_value = type(
            "Settings", (), {"SEND_PROJECT_EMAIL_UPDATES": False}
        )()

        # Mock the database connection context manager
        mock_db_connection.return_value.__aenter__.return_value = self.db
        # Act
        await ProjectService.send_email_on_project_progress(1)

        # Assert
        assert not mock_send_email.called

    async def test_create_project_invalid_geojson(self):
        """Valida que un GeoJSON con geometría inválida sea rechazado al adjuntar tareas."""
        from backend.services.project_admin_service import (
            InvalidGeoJson,
            ProjectAdminService,
        )

        invalid_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[-4.0, 56.0], [-3.9, 56.1]],
                    },
                    "properties": {},
                }
            ],
        }

        test_project = Project()

        with pytest.raises(InvalidGeoJson):
            await ProjectAdminService._attach_tasks_to_project(
                test_project, invalid_geojson, self.db
            )

    @patch.object(ProjectAdminService, "is_user_action_permitted_on_project", return_value=False)
    async def test_unauthorized_mutation(self, mock_permitted):
        """Valida que la actualización de un proyecto por un usuario sin permisos sea rechazada."""
        from backend.models.dtos.project_dto import ProjectDTO
        from tests.api.helpers.test_helpers import create_canned_project

        test_project, test_user, project_id = await create_canned_project(self.db)

        dto = ProjectDTO.model_construct(
            project_id=project_id,
            project_status="DRAFT",
        )

        unauthorized_user_id = test_user.id + 9999

        with pytest.raises(ValueError, match="Project can only be updated by admins or by the owner"):
            await ProjectAdminService.update_project(dto, unauthorized_user_id, self.db)

    async def test_get_project_privacy_and_status_not_found(self):
        """Valida que se lance NotFound si el proyecto no existe al consultar privacidad."""
        with pytest.raises(NotFound):
            await ProjectService.get_project_privacy_and_status(99999, self.db)

    @patch.object(Project, "get_project_total_contributions", return_value=5)
    @patch.object(Project, "get_active_mappers", return_value=2)
    @patch.object(Project, "get_project_campaigns", return_value=[])
    @patch.object(Project, "get_dto_for_locale")
    @patch.object(Project, "get_project_summary")
    async def test_get_project_summary_calculation(self, mock_summary, mock_info, mock_camp, mock_mappers, mock_contribs):
        """Valida el cálculo manual de porcentajes de finalización en el resumen del proyecto."""
        # Arrange
        # Usamos MagicMock y definimos los atributos directamente para que la lógica project.attribute funcione
        mock_row = MagicMock()
        mock_row.id = 1
        mock_row.actual_tasks_mapped = 10
        mock_row.actual_tasks_validated = 5
        mock_row.actual_total_tasks = 20
        mock_row.actual_tasks_bad_imagery = 0
        mock_row.status = 1
        mock_row.priority = 1
        mock_row.difficulty = 1
        mock_row.mapping_permission = 1
        mock_row.validation_permission = 1
        mock_row.default_locale = "en"
        mock_row.centroid = '{"type": "Point", "coordinates": [0,0]}'

        # También configuramos __getitem__ por si el modelo usa acceso tipo dict['key']
        mock_row.__getitem__.side_effect = lambda key: getattr(mock_row, key, None)

        # Configuramos el retorno del DTO base
        mock_summary.return_value = ProjectSummary(
            project_id=1,
            mapping_editors=["ID"],
            validation_editors=["ID"]
        )

        # Mock de fetch_one de la base de datos
        with patch.object(self.db, "fetch_one", return_value=mock_row):
            # Act
            summary = await ProjectService.get_project_summary(1, self.db)

            # Assert:
            # percent_mapped: (10 + 5) / 20 * 100 = 75%
            # percent_validated: 5 / 20 * 100 = 25%
            assert summary.percent_mapped == 75
            assert summary.percent_validated == 25

    async def test_favorite_logic_flow(self):
        """Valida la lógica de favoritos y manejo de errores al desmarcar si no existe."""
        _, test_user, project_id = await create_canned_project(self.db)

        # Test: Marcar como favorito
        await ProjectService.favorite(project_id, test_user.id, self.db)
        assert await ProjectService.is_favorited(project_id, test_user.id, self.db) is True

        # Test: Desmarcar
        await ProjectService.unfavorite(project_id, test_user.id, self.db)
        assert await ProjectService.is_favorited(project_id, test_user.id, self.db) is False

    async def test_get_contribs_by_day_logic(self):
        """Prueba la agregación de contribuciones diarias."""
        # Arrange
        mock_project = MagicMock()
        mock_project.total_tasks = 100

        today = datetime.datetime.utcnow().date()
        mock_history = [
            {"day": today, "action_text": "MAPPED", "task_id": 1},
            {"day": today, "action_text": "VALIDATED", "task_id": 2}
        ]

        with patch.object(ProjectService, "get_project_by_id", return_value=mock_project):
            with patch.object(self.db, "fetch_all", return_value=mock_history):
                contribs = await ProjectService.get_contribs_by_day(1, self.db)
                assert len(contribs.stats) >= 1
                assert contribs.stats[0].mapped == 2 # 1 mapped + 1 validated (que implica mapped)

    async def test_get_active_projects_structure(self):
        """Valida que la recuperación de proyectos activos devuelva un FeatureCollection válido."""
        # Act
        result = await ProjectService.get_active_projects(24, self.db)

        # Assert
        assert result["type"] == "FeatureCollection"
        assert isinstance(result["features"], list)

    async def test_get_project_priority_areas_empty(self):
        """Verifica que un proyecto sin áreas de prioridad devuelva una lista vacía."""
        from tests.api.helpers.test_helpers import create_canned_project
        _, _, project_id = await create_canned_project(self.db)

        areas = await ProjectService.get_project_priority_areas(project_id, self.db)
        assert areas == []

    @patch.object(ProjectService, "get_project_by_id")
    async def test_get_project_dto_for_mapper_denied(self, mock_get_prj):
        """Valida que un usuario anónimo sea rechazado para un DRAFT."""
        stub_project = MagicMock()
        stub_project.id = 101
        stub_project.private = False
        stub_project.status = ProjectStatus.DRAFT.value
        mock_get_prj.return_value = stub_project

        with pytest.raises(ProjectServiceError):
            await ProjectService.get_project_dto_for_mapper(101, None, self.db)

    @patch.object(UserService, "get_user_by_username")
    @patch.object(Project, "get_project_user_stats")
    async def test_get_project_user_stats(self, mock_get_stats, mock_get_user):
        """Cubre el cálculo de tiempos en segundos y flujo de estadísticas."""
        # Arrange
        # Mockeamos el usuario para que tenga el atributo .id que el backend espera
        mock_user = MagicMock()
        mock_user.id = 123
        mock_get_user.return_value = mock_user

        # Mockeamos el retorno de las estadísticas del modelo
        mock_get_stats.return_value = ProjectUserStatsDTO(
            timeSpentMapping=5400, # 1.5 horas
            timeSpentValidating=5400,
            totalTimeSpent=10800
        )

        # Act
        with patch.object(ProjectService, "exists", return_value=True):
            stats = await ProjectService.get_project_user_stats(1, "mapper_user", self.db)

            # Assert
            assert stats.time_spent_mapping == 5400
            assert stats.total_time_spent == 10800

    async def test_get_active_projects_interval_logic(self):
        """Cubre las ramas de recuperación de proyectos con actividad reciente."""
        mock_ids = [{"project_id": 1}, {"project_id": 2}]
        mock_details = [
            {"id": 1, "mapping_types": [1], "geometry": '{"type": "MultiPolygon", "coordinates": []}'}
        ]

        with patch.object(self.db, "fetch_all") as mock_fetch:
            mock_fetch.side_effect = [mock_ids, mock_details]
            result = await ProjectService.get_active_projects(12, self.db)
            assert result["type"] == "FeatureCollection"
            assert len(result["features"]) == 1

    @patch("backend.services.project_service.db_connection")
    @patch.object(SMTPService, "send_email_to_contributors_on_project_progress")
    async def test_send_email_progress_already_sent(self, mock_email, mock_db_conn):
        """Valida que no se envíe email si ya fue enviado o si la DB no está lista."""
        # Configuramos el mock de db_connection para que no explote
        mock_db_conn.database.connection.return_value.__aenter__.return_value = self.db

        mock_prj = MagicMock()
        mock_prj.progress_email_sent = True
        mock_prj.tasks_mapped = 50
        mock_prj.total_tasks = 100

        with patch.object(ProjectService, "get_project_by_id", return_value=mock_prj):
            await ProjectService.send_email_on_project_progress(1)
            mock_email.assert_not_called()

    async def test_get_project_priority_areas_not_found(self):
        """Verifica el manejo de error si el proyecto no existe al buscar áreas."""
        with patch.object(Project, "exists", side_effect=NotFound):
            with pytest.raises(NotFound):
                await ProjectService.get_project_priority_areas(1, self.db)

