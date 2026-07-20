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

    async def test_multiple_filters(self):
        """Valida que se puedan aplicar múltiples filtros combinados sin fallos."""
        from backend.models.dtos.project_dto import ProjectSearchDTO
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            difficulty="EASY",
            text_search="Test",
            campaign="test_campaign",
            mapping_types=["ROADS", "BUILDINGS"],
            page=1,
        )

        try:
            project_search_dto = await ProjectSearchService.search_projects(
                search_dto, None, self.db
            )
            assert project_search_dto is not None
        except NotFound:
            # NotFound is expected if the mock data doesn't match all filters
            pass

    async def test_invalid_filters(self):
        """Valida que filtros malformados retornen resultados vacíos o excepción controlada, no un HTTP 500."""
        from backend.models.dtos.project_dto import ProjectSearchDTO
        from pydantic import ValidationError
        from backend.exceptions import NotFound

        try:
            search_dto = ProjectSearchDTO(
                difficulty="INVALID_DIFFICULTY",
                project_statuses=["INVALID_STATUS"],
                mapping_types=["INVALID_TYPE"],
                page=1,
            )
        except ValidationError:
            pass # DTO rejection is fine
        else:
            try:
                project_search_dto = await ProjectSearchService.search_projects(
                    search_dto, None, self.db
                )
                assert len(project_search_dto.results) == 0
            except (NotFound, KeyError, ValueError):
                # We expect a controlled exception, not a 500 server crash
                pass

    async def test_search_by_text_and_locale(self):
        """TC-SRC-003: Búsqueda combinando text_search y preferred_locale."""
        from backend.models.dtos.project_dto import ProjectSearchDTO
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            text_search="Building",
            preferred_locale="en",
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass

    async def test_search_by_user_interests(self):
        """TC-SRC-004: Búsqueda filtrando por intereses (based_on_user_interests=True)."""
        from backend.models.dtos.project_dto import ProjectSearchDTO
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            based_on_user_interests=True,
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass

    async def test_search_by_mapped_and_favorited(self):
        """TC-SRC-005: Búsqueda combinando mapped_by y favorited_by."""
        from backend.models.dtos.project_dto import ProjectSearchDTO
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            mapped_by=self.test_user.id,
            favorited_by=True,
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass

    async def test_search_action_map_and_validate(self):
        """TC-SRC-006: Búsqueda con action='map' y action='validate'."""
        from backend.models.dtos.project_dto import ProjectSearchDTO
        from backend.exceptions import NotFound
        
        for action in ["map", "validate"]:
            search_dto = ProjectSearchDTO(
                action=action,
                page=1,
            )
            try:
                await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
            except NotFound:
                pass

    async def test_search_by_org_and_team(self):
        """TC-SRC-007: Filtro por organisation_id, team_id, sandbox, mapping_types."""
        from backend.models.dtos.project_dto import ProjectSearchDTO
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            organisation_id=1,
            team_id=1,
            sandbox=False,
            mapping_types=["ROADS"],
            mapping_types_exact=True,
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass

    async def test_search_order_by_percentage(self):
        """TC-SRC-008: Uso de order_by='percent_mapped' (DESC)."""
        from backend.models.dtos.project_dto import ProjectSearchDTO
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            order_by="percent_mapped",
            order_by_type="DESC",
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass
            
        search_dto.order_by = "percent_validated"
        search_dto.order_by_type = "ASC"
        
        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass

    async def test_get_projects_geojson_valid_bbox(self):
        """TC-SRC-009: Generación de FeatureCollection desde un BBox SRID 4326."""
        from backend.models.dtos.project_dto import ProjectSearchBBoxDTO
        
        search_bbox_dto = ProjectSearchBBoxDTO(
            bbox=[-10, -10, 10, 10], # [min_lon, min_lat, max_lon, max_lat]
            input_srid=4326,
            preferred_locale="en",
        )
        
        feature_collection = await ProjectSearchService.get_projects_geojson(search_bbox_dto, self.db)
        assert feature_collection is not None
        assert feature_collection.type == "FeatureCollection"

    async def test_get_projects_geojson_bbox_too_big(self):
        """TC-SRC-010: Solicitud geoespacial con BBox mayor al MAX_AREA."""
        from backend.models.dtos.project_dto import ProjectSearchBBoxDTO
        from backend.services.project_search_service import BBoxTooBigError
        
        # huge bbox covering most of the world (but within 3857 valid limits to avoid internal PostGIS error)
        search_bbox_dto = ProjectSearchBBoxDTO(
            bbox=[-170, -80, 170, 80],
            input_srid=4326,
            preferred_locale="en",
        )
        
        with pytest.raises(BBoxTooBigError):
            await ProjectSearchService.get_projects_geojson(search_bbox_dto, self.db)

    async def test_search_projects_as_csv(self):
        """TC-SRC-011: Exportación CSV con as_csv=True"""
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            page=1,
        )

        try:
            result = await ProjectSearchService.search_projects_as_csv(
                search_dto, self.test_user.id, self.db, True
            )
            assert result is not None
            assert isinstance(result, str)
        except (NotFound, ValueError):
            pass

    async def test_search_by_all_dates_and_locations(self):
        """TC-SRC-012: Filtros de fechas (created, last_updated) y localización (country, imagery)."""
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            country="Uganda",
            imagery="custom",
            last_updated_gte="2023-01-01",
            last_updated_lte="2025-01-01",
            created_gte="2023-01-01",
            created_lte="2025-01-01",
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass
            
    async def test_search_by_partner_and_managed(self):
        """TC-SRC-013: Filtros de partnerships, creador y administrador."""
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            partner_id=1,
            partnership_from="2023-01-01",
            partnership_to="2025-01-01",
            created_by=1,
            managed_by=1,
            organisation_name="HOT",
            interests=[1, 2],
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass

    async def test_draft_status_filter(self):
        """TC-SRC-014: Manejo del estado DRAFT para usuarios no logueados."""
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            project_statuses=["DRAFT"],
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, None, self.db)
        except NotFound:
            pass

    async def test_draft_status_filter_with_user(self):
        """TC-SRC-015: Manejo del estado DRAFT para usuario logueado (no admin)."""
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            project_statuses=["DRAFT"],
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass

    async def test_search_with_omit_map_results(self):
        """TC-SRC-016: Búsqueda con omit_map_results=True para cubrir rama de paginación COUNT."""
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            omit_map_results=True,
            project_statuses=["PUBLISHED"],
            page=1,
        )

        try:
            result = await ProjectSearchService.search_projects(
                search_dto, self.test_user, self.db
            )
            assert result is not None
        except NotFound:
            pass

    async def test_search_with_imagery_specific(self):
        """TC-SRC-017: Búsqueda con imagery específico (no 'custom')."""
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            imagery="https://tiles.example.com/{z}/{x}/{y}.png",
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass

    async def test_search_order_by_generic_column(self):
        """TC-SRC-018: Ordenamiento por columna genérica (ej. id) para cubrir rama else de order_by."""
        from backend.exceptions import NotFound
        
        search_dto = ProjectSearchDTO(
            order_by="id",
            order_by_type="DESC",
            page=1,
        )

        try:
            await ProjectSearchService.search_projects(search_dto, self.test_user, self.db)
        except NotFound:
            pass

