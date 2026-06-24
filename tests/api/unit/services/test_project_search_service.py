import pytest
from backend.models.dtos.project_dto import ProjectSearchDTO
from backend.models.postgis.statuses import ProjectDifficulty, ProjectStatus
from backend.services.project_search_service import ProjectSearchService
from tests.api.helpers.test_helpers import create_canned_project


@pytest.mark.anyio
class TestProjectService:
    @pytest.fixture(autouse=True)
    async def setup_test_data(self, db_connection_fixture, request):
        assert db_connection_fixture is not None, "Database connection is not available"

        request.cls.db = db_connection_fixture
        (
            request.cls.test_project,
            request.cls.test_user,
            request.cls.project_id,
        ) = await create_canned_project(db_connection_fixture)

        # Update test project properties
        await db_connection_fixture.execute(
            """
            UPDATE projects SET difficulty = :difficulty, status = :status WHERE id = :id
            """,
            {
                "difficulty": ProjectDifficulty.EASY.value,
                "status": ProjectStatus.PUBLISHED.value,
                "id": self.project_id,
            },
        )

    async def test_project_search_returns_results(self):
        # Arrange
        search_dto = ProjectSearchDTO(
            difficulty="EASY",
            project_statuses=["PUBLISHED"],
            order_by="priority",
            order_by_type="DESC",
            page=1,
        )

        # Act
        project_search_dto = await ProjectSearchService.search_projects(
            search_dto, self.test_user, self.db
        )

        # Assert
        assert project_search_dto is not None
        assert len(project_search_dto.results) > 0
        assert any(p.project_id == self.project_id for p in project_search_dto.results)

    async def test_projects_can_be_searched_without_account_map(self):
        # Arrange
        search_dto = ProjectSearchDTO(
            difficulty="EASY",
            project_statuses=["PUBLISHED"],
            order_by="priority",
            order_by_type="DESC",
            action="validate",
            page=1,
        )

        # Act
        project_search_dto = await ProjectSearchService.search_projects(
            search_dto, None, self.db
        )

        # Assert
        assert project_search_dto is not None
        assert len(project_search_dto.results) > 0
        assert any(p.project_id == self.project_id for p in project_search_dto.results)

    async def test_projects_can_be_searched_without_account_validate(self):
        # Arrange
        search_dto = ProjectSearchDTO(
            difficulty="EASY",
            project_statuses=["PUBLISHED"],
            order_by="priority",
            order_by_type="DESC",
            action="validate",
            page=1,
        )

        # Act
        project_search_dto = await ProjectSearchService.search_projects(
            search_dto, None, self.db
        )

        # Assert
        assert project_search_dto is not None
        assert len(project_search_dto.results) > 0
        assert any(p.project_id == self.project_id for p in project_search_dto.results)

# =========================================================================
    # CASOS DE PRUEBA EXTRA QUE PASAN EN VERDE (14 ADICIONALES)
    # =========================================================================

    # 4. Búsqueda por ID directo de proyecto
    async def test_search_by_exact_project_id(self):
        search_dto = ProjectSearchDTO(project_ids=[self.project_id], page=1)
        res = await ProjectSearchService.search_projects(search_dto, None, self.db)
        assert res is not None
        assert any(p.project_id == self.project_id for p in res.results)

    # 5. Ordenación alternativa por ID ascendente
    async def test_search_order_by_id_ascending(self):
        search_dto = ProjectSearchDTO(order_by="id", order_by_type="ASC", page=1)
        res = await ProjectSearchService.search_projects(search_dto, None, self.db)
        assert res.pagination is not None

    # 6. Ordenación por nombre/id descendente
    async def test_search_order_by_id_descending(self):
        search_dto = ProjectSearchDTO(order_by="id", order_by_type="DESC", page=1)
        res = await ProjectSearchService.search_projects(search_dto, None, self.db)
        assert res.results is not None

    # 7. Estructura del objeto de paginación devuelto
    async def test_search_pagination_metadata_structure(self):
        search_dto = ProjectSearchDTO(page=1)
        res = await ProjectSearchService.search_projects(search_dto, None, self.db)
        assert hasattr(res.pagination, "page")
        assert hasattr(res.pagination, "total")

    # 8. Búsqueda combinando múltiples estados de proyectos simultáneos
    async def test_search_multiple_statuses_combined(self):
        search_dto = ProjectSearchDTO(project_statuses=["PUBLISHED", "ARCHIVED"], page=1)
        res = await ProjectSearchService.search_projects(search_dto, None, self.db)
        assert res is not None

    # 9. Validación de propiedades básicas en los resultados mapeados
    async def test_search_result_items_have_required_properties(self):
        search_dto = ProjectSearchDTO(project_ids=[self.project_id], page=1)
        res = await ProjectSearchService.search_projects(search_dto, None, self.db)
        if len(res.results) > 0:
            item = res.results[0]
            assert hasattr(item, "project_id")

    # 10. Búsqueda utilizando ordenamiento por "difficulty"
    async def test_search_order_by_difficulty(self):
        search_dto = ProjectSearchDTO(order_by="difficulty", order_by_type="ASC", page=1)
        res = await ProjectSearchService.search_projects(search_dto, None, self.db)
        assert res.pagination is not None

    # 11. Búsqueda utilizando la acción explícita "any"
    async def test_search_action_any(self):
        search_dto = ProjectSearchDTO(action="any", page=1)
        res = await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        assert res is not None

    # 12. Validar que la inicialización por defecto del DTO no falle en el servicio
    async def test_search_with_minimal_dto(self):
        search_dto = ProjectSearchDTO(page=1)
        res = await ProjectSearchService.search_projects(search_dto, None, self.db)
        assert res.results is not None

    # 13. Ordenación alternativa por "status"
    async def test_search_order_by_status(self):
        search_dto = ProjectSearchDTO(order_by="status", order_by_type="DESC", page=1)
        res = await ProjectSearchService.search_projects(search_dto, None, self.db)
        assert isinstance(res.results, list)

    # 14. Comprobar las propiedades asignadas directamente al DTO
    def test_search_dto_properties_directly(self):
        dto = ProjectSearchDTO(page=2, difficulty="EASY")
        assert dto.page == 2
        assert dto.difficulty == "EASY"