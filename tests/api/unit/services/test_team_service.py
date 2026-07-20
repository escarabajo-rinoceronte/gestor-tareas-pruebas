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
