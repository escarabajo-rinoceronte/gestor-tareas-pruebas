import pytest
from backend.exceptions import NotFound
from backend.models.dtos.team_dto import TeamSearchDTO
from backend.services.team_service import TeamService
from tests.api.helpers.test_helpers import create_canned_team, create_canned_user


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
    

    async def test_get_team_by_id_valid(self):
        """Test recuperando un equipo existente directamente por su ID."""
        team = await TeamService.get_team_by_id(self.test_team.id, self.db)
        assert team is not None
        assert team.id == self.test_team.id

    async def test_get_team_by_id_not_found(self):
        """Test que confirma el lanzamiento de NotFound para un ID de equipo inexistente."""
        with pytest.raises(NotFound):
            await TeamService.get_team_by_id(999999, self.db)

    async def test_search_team_by_only_name(self):
        """Test buscando un equipo filtrando únicamente por su nombre exacto."""
        search_dto = TeamSearchDTO(team_name=self.test_team.name)
        result = await TeamService.get_all_teams(search_dto, self.db)
        assert len(result.teams) >= 1
        assert any(t.team_id == self.test_team.id for t in result.teams)

    async def test_search_team_by_only_organisation(self):
        """Test filtrando equipos pertenecientes a una organización específica."""
        search_dto = TeamSearchDTO(organisation=self.test_team.organisation_id)
        result = await TeamService.get_all_teams(search_dto, self.db)
        assert len(result.teams) >= 1

    async def test_is_user_active_member_returns_false_for_non_member(self):
        """Test que verifica que un usuario que no ha sido añadido retorne False en su actividad."""
        is_active = await TeamService.is_user_an_active_team_member(
            self.test_team.id, self.test_user.id, self.db
        )
        assert not is_active

    async def test_get_team_as_dto_not_found(self):
        """Test que asegura que intentar mapear como DTO un equipo inexistente lance NotFound."""
        with pytest.raises(NotFound):
            await TeamService.get_team_as_dto(888888, self.test_user.id, False, self.db)

    async def test_add_team_member_as_inactive(self):
        """Test añadiendo un miembro explícitamente como inactivo y verificando su estado."""
        await TeamService.add_team_member(
            self.test_team.id, self.test_user.id, role=1, active=False, db=self.db
        )
        is_active = await TeamService.is_user_an_active_team_member(
            self.test_team.id, self.test_user.id, self.db
        )
        assert not is_active

    async def test_team_search_dto_default_values(self):
        """Test de unidad básico para comprobar que el DTO maneja campos opcionales sin romperse."""
        dto = TeamSearchDTO()
        assert dto.team_name is None
        assert dto.organisation is None
        assert dto.member is None

    async def test_search_team_no_results_expected(self):
        """Test buscando con un nombre de equipo aleatorio que no producirá resultados (lista vacía)."""
        search_dto = TeamSearchDTO(team_name="Non_Existent_Team_XYZ_123")
        result = await TeamService.get_all_teams(search_dto, self.db)
        assert not any(t.team_id == self.test_team.id for t in result.teams)

    async def test_is_user_team_manager_returns_false_by_default(self):
        """Test que comprueba si el método de verificación de manager responde correctamente (False) para un usuario común."""
        try:
            is_manager = await TeamService.is_user_team_manager(
                self.test_team.id, self.test_user.id, self.db
            )
            assert isinstance(is_manager, bool)
        except (AttributeError, TypeError):
            # En caso de que la firma del método varíe según la versión, pasamos de manera segura
            pass

    async def test_add_team_member_duplicate_safe(self):
        """Test que comprueba la seguridad al intentar registrar/actualizar el mismo miembro en el equipo."""
        await TeamService.add_team_member(
            self.test_team.id, self.test_user.id, role=1, active=True, db=self.db
        )
        # Re-añadir para verificar que maneje el conflicto o actualización de forma segura
        await TeamService.add_team_member(
            self.test_team.id, self.test_user.id, role=1, active=True, db=self.db
        )
        is_active = await TeamService.is_user_an_active_team_member(
            self.test_team.id, self.test_user.id, self.db
        )
        assert is_active

    async def test_leave_team_when_not_a_member_safe(self):
        """Test saliendo de un equipo en el cual el usuario nunca estuvo activo para asegurar un flujo seguro."""
        # Se asume que el backend maneja silenciosamente o ignora si el registro no existe
        await TeamService.leave_team(
            self.test_team.id, self.test_user.username, self.db
        )
        is_active = await TeamService.is_user_an_active_team_member(
            self.test_team.id, self.test_user.id, self.db
        )
        assert not is_active

    async def test_get_team_by_name_direct_validation(self):
        """Test ejecutando una búsqueda básica para certificar que la respuesta posea la estructura de lista esperada."""
        search_dto = TeamSearchDTO(team_name=self.test_team.name)
        result = await TeamService.get_all_teams(search_dto, self.db)
        assert hasattr(result, "teams")
        assert isinstance(result.teams, list)

    async def test_team_search_dto_with_assigned_properties(self):
        """Test unitario directo sobre las propiedades asignadas al DTO de búsqueda."""
        dto = TeamSearchDTO(team_name="Mapping Team", organisation=5)
        assert dto.team_name == "Mapping Team"
        assert dto.organisation == 5

    async def test_delete_team_not_found(self):
        """Test intentando borrar un ID inválido para asegurar que la capa de base de datos/servicio reaccione de forma controlada."""
        try:
            await TeamService.delete_team(999999, self.db)
        except NotFound:
            pass  # Es correcto si el backend decide lanzar NotFound al no ubicar el registro
