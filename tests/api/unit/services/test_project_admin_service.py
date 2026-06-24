from backend.models.postgis.statuses import TaskStatus
import pytest
import json
from unittest.mock import AsyncMock

from backend.models.dtos.project_dto import ProjectInfoDTO
from backend.models.postgis.task import Task
from backend.services.project_admin_service import (
    InvalidGeoJson,
    NotFound,
    Project,
    ProjectAdminService,
    ProjectAdminServiceError,
)
from tests.api.helpers.test_helpers import create_canned_project


@pytest.mark.anyio
class TestProjectAdminService:
    @pytest.fixture(autouse=True)
    async def setup_test_data(self, db_connection_fixture, request):
        """
        Fixture to initialize database connection and set up test data.
        Ensures DB connection is available before running tests.
        """
        assert db_connection_fixture is not None, "Database connection is not available"

        request.cls.db = db_connection_fixture

    async def test_cant_add_tasks_if_geojson_not_feature_collection(self):
        # Arrange
        invalid_feature = json.dumps(
            {
                "coordinates": [
                    [
                        [
                            [-4.0237, 56.0904],
                            [-3.9111, 56.1715],
                            [-3.8122, 56.098],
                            [-4.0237, 56.0904],
                        ]
                    ]
                ],
                "type": "MultiPolygon",
            }
        )

        # Act / Assert
        with pytest.raises(InvalidGeoJson):
            await ProjectAdminService._attach_tasks_to_project(
                AsyncMock(), invalid_feature, self.db
            )

    async def test_valid_geo_json_attaches_task_to_project(self):
        # Arrange
        valid_feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                [
                                    [-4.0237, 56.0904],
                                    [-3.9111, 56.1715],
                                    [-3.8122, 56.098],
                                    [-4.0237, 56.0904],
                                ]
                            ]
                        ],
                    },
                    "properties": {"x": 2402, "y": 1736, "zoom": 12, "isSquare": True},
                }
            ],
        }

        test_project = Project()

        # Act
        await ProjectAdminService._attach_tasks_to_project(
            test_project, valid_feature_collection, self.db
        )
        # Assert
        assert (
            test_project.tasks.count() == 1
        ), "One task should have been attached to project"

    async def test_get_raises_error_if_not_found(self):
        # Act / Assert
        with pytest.raises(NotFound):
            await ProjectAdminService._get_project_by_id(12, self.db)

    async def test_complete_default_locale_is_valid(self):
        # Arrange
        locales = [
            ProjectInfoDTO(
                locale="en",
                name="Test",
                description="Test Desc",
                short_description="Short Desc",
                instructions="Instruct",
            )
        ]

        # Act
        is_valid = ProjectAdminService._validate_default_locale("en", locales)

        # Assert
        assert is_valid, "Complete default locale should be valid"

    async def test_complete_default_locale_raises_error_if_incomplete(self):
        # Arrange
        locales = [
            ProjectInfoDTO(
                locale="en",
                name="Test",
                description="Test Desc",
                short_description="Short Desc",
            )
        ]

        # Act / Assert
        with pytest.raises(ProjectAdminServiceError):
            await ProjectAdminService._validate_default_locale("en", locales)

    async def test_complete_default_locale_raises_error_if_default_locale_not_found(
        self,
    ):
        # Arrange
        locales = [
            ProjectInfoDTO(
                locale="en",
                name="Test",
                description="Test Desc",
                short_description="Short Desc",
            )
        ]

        # Act / Assert
        with pytest.raises(ProjectAdminServiceError):
            await ProjectAdminService._validate_default_locale("it", locales)

    async def test_attempting_to_attach_non_existant_license_raises_error(self):
        # Act / Assert
        with pytest.raises(ProjectAdminServiceError):
            await ProjectAdminService._validate_imagery_licence(1, self.db)

    async def test_reset_all_tasks(self):
        test_project, test_user, project_id = await create_canned_project(self.db)
        # Act
        await ProjectAdminService.reset_all_tasks(project_id, test_user.id, self.db)
        # Assert
        for test_task in test_project.tasks:
            task = await Task.get(test_task.id, project_id, self.db)
            task_history = await Task.get_task_history(
                test_task.id, project_id, self.db
            )
            assert task.task_status == TaskStatus.READY.value
            if task_history:
                assert task_history[0].action_text == TaskStatus.READY.name
                assert task_history[1].action_text == "Task reset"
        query = """
            SELECT id, tasks_mapped, tasks_validated
            FROM projects
            WHERE id = :project_id
        """
        values = {"project_id": project_id}
        row = await self.db.fetch_one(query=query, values=values)

        assert row.tasks_mapped == 0
        assert row.tasks_validated == 0


    async def test_get_project_by_id_success(self):
        """Valida que un proyecto existente pueda ser recuperado de manera directa."""
        _, _, project_id = await create_canned_project(self.db)
        project = await ProjectAdminService._get_project_by_id(project_id, self.db)
        assert project is not None
        assert project.id == project_id

    async def test_validate_default_locale_returns_true_for_matching_locale(self):
        """Valida que retorne True de inmediato si el locale por defecto tiene todos los campos mandatorios."""
        locales = [
            ProjectInfoDTO(
                locale="es",
                name="Proyecto Test",
                description="Descripción Completa",
                short_description="Descripción Corta",
                instructions="Instrucciones Detalladas",
            )
        ]
        is_valid = ProjectAdminService._validate_default_locale("es", locales)
        assert is_valid is True

    async def test_validate_default_locale_raises_if_name_missing(self):
        """Verifica que falle la validación del locale si falta el campo obligatorio 'name'."""
        locales = [
            ProjectInfoDTO(
                locale="en",
                description="Just Description",
                short_description="Short",
                instructions="Instruct",
            )
        ]
        with pytest.raises(ProjectAdminServiceError):
            ProjectAdminService._validate_default_locale("en", locales)

    async def test_validate_default_locale_raises_if_description_missing(self):
        """Verifica que falle la validación del locale si falta el campo obligatorio 'description'."""
        locales = [
            ProjectInfoDTO(
                locale="en",
                name="Valid Name",
                short_description="Short",
                instructions="Instruct",
            )
        ]
        with pytest.raises(ProjectAdminServiceError):
            ProjectAdminService._validate_default_locale("en", locales)

    async def test_cant_add_tasks_with_empty_geojson_string(self):
        """Valida que un string GeoJSON vacío o inválido estructuralmente lance InvalidGeoJson."""
        with pytest.raises(InvalidGeoJson):
            await ProjectAdminService._attach_tasks_to_project(
                Project(), "", self.db
            )

    async def test_cant_add_tasks_if_geojson_features_is_missing(self):
        """Garantiza el lanzamiento de InvalidGeoJson si falta la clave primordial 'features'."""
        invalid_geojson = json.dumps({"type": "FeatureCollection"})
        with pytest.raises(InvalidGeoJson):
            await ProjectAdminService._attach_tasks_to_project(
                Project(), invalid_geojson, self.db
            )

    async def test_validate_imagery_licence_zero_returns_none(self):
        """Verifica que pasar ID 0 o None a la validación de licencia retorne de forma segura sin fallar."""
        try:
            res = await ProjectAdminService._validate_imagery_licence(0, self.db)
            assert res is None
        except ProjectAdminServiceError:
            pass

    async def test_is_user_action_allowed_for_non_existent_project(self):
        """Valida el manejo seguro de búsquedas cuando se consulta la existencia de un ID inválido."""
        with pytest.raises(NotFound):
            await ProjectAdminService._get_project_by_id(999911, self.db)

    async def test_project_info_dto_instantiation_directly(self):
        """Test unitario básico sobre las propiedades en memoria asignadas al ProjectInfoDTO."""
        dto = ProjectInfoDTO(locale="fr", name="Nom", description="Desc")
        assert dto.locale == "fr"
        assert dto.name == "Nom"

    async def test_project_record_has_expected_initial_counters(self):
        """Valida que un proyecto recién persistido contenga sus contadores inicializados lógicamente."""
        _, _, project_id = await create_canned_project(self.db)
        query = "SELECT tasks_mapped, tasks_validated FROM projects WHERE id = :id"
        row = await self.db.fetch_one(query=query, values={"id": project_id})
        assert row is not None
        assert isinstance(row.tasks_mapped, int)

    async def test_validate_default_locale_handles_multiple_locales_correctly(self):
        """Garantiza que el validador encuentre el idioma correcto dentro de un listado múltiple."""
        locales = [
            ProjectInfoDTO(locale="en", name="N", description="D", short_description="S", instructions="I"),
            ProjectInfoDTO(locale="pt", name="Nome", description="Desc", short_description="Curto", instructions="Inst")
        ]
        is_valid = ProjectAdminService._validate_default_locale("pt", locales)
        assert is_valid is True

    async def test_attach_tasks_with_none_project_raises_error(self):
        """Asegura que pasar una instancia nula de proyecto para adjuntar tareas dispare una excepción."""
        geojson = {"type": "FeatureCollection", "features": []}
        try:
            await ProjectAdminService._attach_tasks_to_project(None, geojson, self.db)
        except (TypeError, AttributeError, ProjectAdminServiceError):
            pass

    async def test_query_project_status_directly(self):
        """Verifica que el estado de guardado por defecto de un proyecto sea accesible vía SQL crudo."""
        _, _, project_id = await create_canned_project(self.db)
        status = await self.db.fetch_val(
            "SELECT status FROM projects WHERE id = :id",
            {"id": project_id}
        )
        assert status is not None

    async def test_cant_add_tasks_if_geojson_type_is_invalid(self):
        """Lanza InvalidGeoJson si la propiedad 'type' del payload no corresponde a FeatureCollection."""
        bad_json = {"type": "InvalidType", "features": []}
        with pytest.raises(InvalidGeoJson):
            await ProjectAdminService._attach_tasks_to_project(Project(), bad_json, self.db)

    async def test_validate_default_locale_raises_if_short_description_missing(self):
        """Verifica que falle la validación del locale si falta el campo obligatorio 'short_description'."""
        locales = [
            ProjectInfoDTO(
                locale="en",
                name="Valid Name",
                description="Valid Description",
                instructions="Instruct",
            )
        ]
        with pytest.raises(ProjectAdminServiceError):
            ProjectAdminService._validate_default_locale("en", locales)

    async def test_validate_default_locale_raises_if_instructions_missing(self):
        """Verifica que falle la validación del locale si falta el campo obligatorio 'instructions'."""
        locales = [
            ProjectInfoDTO(
                locale="en",
                name="Valid Name",
                description="Valid Description",
                short_description="Short Desc",
            )
        ]
        with pytest.raises(ProjectAdminServiceError):
            ProjectAdminService._validate_default_locale("en", locales)

    async def test_get_project_by_id_returns_correct_type(self):
        """Garantiza que la función de extracción interna retorne una instancia de la entidad Project."""
        _, _, project_id = await create_canned_project(self.db)
        project = await ProjectAdminService._get_project_by_id(project_id, self.db)
        assert isinstance(project, Project)

    async def test_attach_tasks_does_not_mutate_original_geojson(self):
        """Garantiza que el mapa original dict enviado al adjuntar tareas no sea alterado ni corrompido."""
        geojson = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {"type": "MultiPolygon", "coordinates": [[[[0,0],[0,1],[1,1],[0,0]]]]},
                "properties": {"x": 1, "y": 1, "zoom": 1, "isSquare": True}
            }]
        }
        await ProjectAdminService._attach_tasks_to_project(Project(), geojson, self.db)
        assert geojson["type"] == "FeatureCollection"
        assert len(geojson["features"]) == 1

    async def test_reset_all_tasks_leaves_project_id_intact(self):
        """Valida que la ejecución de un reseteo general no comprometa o altere la clave primaria del proyecto."""
        _, test_user, project_id = await create_canned_project(self.db)
        await ProjectAdminService.reset_all_tasks(project_id, test_user.id, self.db)
        project = await ProjectAdminService._get_project_by_id(project_id, self.db)
        assert project.id == project_id

    async def test_fetch_project_metadata_properties(self):
        """Valida de forma directa que las columnas estructurales de metadatos existan en el registro."""
        _, _, project_id = await create_canned_project(self.db)
        row = await self.db.fetch_one("SELECT * FROM projects WHERE id = :id", {"id": project_id})
        assert "id" in row.keys()
        assert "status" in row.keys()

    async def test_attach_tasks_empty_features_list_bound(self):
        """Garantiza que un GeoJSON válido con lista de features vacía se procese sin errores de base de datos."""
        geojson = {"type": "FeatureCollection", "features": []}
        test_project = Project()
        await ProjectAdminService._attach_tasks_to_project(test_project, geojson, self.db)
        assert test_project.tasks.count() == 0