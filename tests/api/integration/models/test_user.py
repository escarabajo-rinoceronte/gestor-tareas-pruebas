import pytest
from tests.api.helpers.test_helpers import create_canned_user, create_canned_project


@pytest.mark.anyio
class TestUser:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture

        self.test_user = await create_canned_user(self.db)

        await self.db.execute(
            """
            UPDATE users
            SET username = :username,
                email_address = :email
            WHERE id = :user_id
            """,
            {
                "username": "mrtest",
                "email": "test@test.com",
                "user_id": self.test_user.id,
            },
        )

        self.test_user.username = "mrtest"
        self.test_user.email_address = "test@test.com"

    async def test_as_dto_will_not_return_email_if_not_owner(self):
        # Act
        user_dto = await self.test_user.as_dto("mastertest", self.db)

        # Assert
        assert not user_dto.email_address

    async def test_as_dto_will_return_email_if_owner(self):
        # Act
        user_dto = await self.test_user.as_dto("mrtest", self.db)

        # Assert
        assert user_dto.email_address

@pytest.mark.anyio
class TestUserMappedProjects:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        self.test_user = await create_canned_user(self.db)
        self.test_project, _, self.test_project_id = await create_canned_project(self.db)

    async def test_upsert_mapped_projects_adds_new_project(self):
        from backend.models.postgis.user import User
        await User.upsert_mapped_projects(self.test_user.id, self.test_project_id, self.db)
        user = await User.get_by_id(self.test_user.id, self.db)
        assert user.projects_mapped is not None
        assert self.test_project_id in user.projects_mapped

    async def test_upsert_mapped_projects_ignores_duplicate(self):
        from backend.models.postgis.user import User
        await User.upsert_mapped_projects(self.test_user.id, self.test_project_id, self.db)
        await User.upsert_mapped_projects(self.test_user.id, self.test_project_id, self.db)
        user = await User.get_by_id(self.test_user.id, self.db)
        assert user.projects_mapped.count(self.test_project_id) == 1

    async def test_get_mapped_projects_returns_dto(self):
        from backend.models.postgis.user import User
        await User.upsert_mapped_projects(self.test_user.id, self.test_project_id, self.db)
        dto = await User.get_mapped_projects(self.test_user.id, "en", self.db)
        assert dto is not None
        assert hasattr(dto, "mapped_projects")


@pytest.mark.anyio
class TestUserStatsModel:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        self.test_user = await create_canned_user(self.db)

    async def test_update_user_stats(self):
        from backend.models.postgis.user import UserStats
        stats_payload = {
            "result": {
                "topics": {
                    "buildings": {"added": 150},
                    "roads": {"value": 300}
                }
            }
        }
        new_stats = await UserStats.update(self.test_user.id, stats_payload, self.db)
        assert new_stats["buildings"] == 150
        assert new_stats["roads"] == 300
        
        saved_stats = await UserStats.get_for_user(self.test_user.id, self.db)
        assert saved_stats is not None
        assert saved_stats.user_id == self.test_user.id
        
        stats_payload_2 = {"result": {"topics": {"buildings": {"added": 500}}}}
        updated_stats = await UserStats.update(self.test_user.id, stats_payload_2, self.db)
        assert updated_stats["buildings"] == 500