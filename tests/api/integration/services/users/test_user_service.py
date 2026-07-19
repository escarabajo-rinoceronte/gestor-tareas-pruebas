from backend.models.postgis.mapping_badge import MappingBadge
import datetime
import json
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from backend.services.users.user_service import (
    UserService,
    UserServiceError,
    MappingLevel,
    User,
)
from backend.models.postgis.user import UserEmail, UserNextLevel, UserLevelVote, UserStats
from backend.models.dtos.user_dto import UserDTO, UserRegisterEmailDTO
from backend.services.users.osm_service import OSMService
from backend.exceptions import NotFound
from fastapi import HTTPException
from tests.api.helpers.test_helpers import (
    create_canned_user,
    return_canned_user,
    create_mapping_levels,
)
from httpx import AsyncClient
from backend.config import test_settings as settings


@pytest.mark.anyio
class TestUserService:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture

        await create_mapping_levels(self.db)

        # Create a default user used by multiple tests
        canned = await return_canned_user(
            username="New Thinkwhere TEST",
            id=7777777,
            db=self.db,
        )
        self.test_user = await create_canned_user(self.db, canned)

    async def test_set_level_adds_level_to_user(self):
        # Act
        user = await UserService.set_user_mapping_level(
            self.test_user.username,
            "ADVANCED",
            db=self.db,
        )

        user = await UserService.get_user_by_id(
            self.test_user.id,
            db=self.db,
        )
        # Assert
        assert user.mapping_level == 3

    async def test_user_can_register_with_correct_mapping_level(self):
        # Act
        test_user = await UserService.register_user(
            12,
            "Thinkwhere",
            300,
            "some_picture_url",
            None,
            db=self.db,
        )

        # Assert
        assert test_user.mapping_level == 1  # Beginner mapping level

    @patch.object(UserService, "notify_level_upgrade", new_callable=AsyncMock)
    @patch.object(MappingLevel, "all_badges_satisfied", new_callable=AsyncMock)
    @patch.object(MappingLevel, "get_next", new_callable=AsyncMock)
    @patch.object(MappingBadge, "available_badges_for_user", new_callable=AsyncMock)
    @patch.object(UserService, "get_and_save_stats", new_callable=AsyncMock)
    @patch.object(MappingLevel, "get_by_id", new_callable=AsyncMock)
    @patch.object(UserService, "get_user_by_id", new_callable=AsyncMock)
    async def test_mapper_level_updates_correctly(
        self,
        mock_user_get,
        mock_get_by_id,
        mock_get_stats,
        mock_available_badges,
        mock_get_next,
        mock_all_badges_satisfied,
        mock_notify,
    ):
        # ---------- Arrange ----------
        user = User()
        user.id = 12
        user.username = "Test User"
        user.mapping_level = 1  # BEGINNER

        user.assign_badges = AsyncMock()
        user.set_mapping_level = AsyncMock()

        mock_user_get.return_value = user

        beginner = AsyncMock()
        beginner.id = 1
        beginner.ordering = 1

        intermediate = AsyncMock()
        intermediate.id = 2
        intermediate.name = "INTERMEDIATE"
        intermediate.ordering = 2
        intermediate.approvals_required = 0

        mock_get_by_id.return_value = beginner
        mock_get_next.return_value = intermediate
        mock_all_badges_satisfied.return_value = True

        mock_get_stats.return_value = {"changeset_count": 350}
        mock_available_badges.return_value = []  # no blocking badges

        await UserService.check_and_update_mapper_level(12, db=self.db)

        user.set_mapping_level.assert_awaited_once_with(intermediate, self.db)
        mock_notify.assert_awaited_once_with(12, "Test User", "INTERMEDIATE", self.db)

    async def test_update_user_updates_user_details(self):
        # Act
        await UserService.update_user(
            self.test_user.id,
            "Thinkwhere",
            None,
            db=self.db,
        )

        # Assert
        user = await UserService.get_user_by_id(
            self.test_user.id,
            db=self.db,
        )
        assert user.username == "Thinkwhere"

    async def test_register_user_creates_new_user(self):
        # Arrange
        canned = await return_canned_user(db=self.db)

        # Act
        await UserService.register_user(
            canned.id,
            canned.username,
            251,
            None,
            None,
            db=self.db,
        )

        # Assert
        user = await UserService.get_user_by_id(canned.id, db=self.db)
        assert user.username == canned.username
        assert user.mapping_level == 1

    async def test_osm_user_endpoint_not_rate_limited(self):
        url = "https://www.openstreetmap.org/api/0.6/user/490556.json"

        async with AsyncClient(timeout=10.0) as client:
            response = await client.get(
                url,
                headers={"User-Agent": settings.OSM_USER_AGENT},
            )
        assert response.status_code == 200
        assert response.status_code != 429

    async def test_get_project_managers_returns_users(self):
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": 2, "id": self.test_user.id},
        )
        users = await UserService.get_project_managers(self.db)
        assert len(users) >= 1

    async def test_get_general_admins_returns_users(self):
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": 1, "id": self.test_user.id},
        )
        users = await UserService.get_general_admins(self.db)
        assert len(users) >= 1

    async def test_update_user_updates_picture_url(self):
        await UserService.update_user(
            self.test_user.id,
            self.test_user.username,
            "new_pic.jpg",
            db=self.db,
        )
        user = await UserService.get_user_by_id(self.test_user.id, db=self.db)
        assert user.picture_url == "new_pic.jpg"

    async def test_get_projects_favorited_returns_empty(self):
        favs = await UserService.get_projects_favorited(self.test_user.id, db=self.db)
        assert len(favs.favorited_projects) == 0

    async def test_get_projects_mapped_returns_empty(self):
        mapped = await UserService.get_projects_mapped(self.test_user.id, db=self.db)
        assert len(mapped) == 0

    async def test_get_and_save_stats_returns_empty_on_ohsome_error(self):
        mock_ohsome_response = AsyncMock()
        mock_ohsome_response.status_code = 500
        
        mock_osm_response = AsyncMock()
        mock_osm_response.status_code = 200

        with patch("httpx.AsyncClient.get", side_effect=[mock_ohsome_response, mock_osm_response]):
            stats = await UserService.get_and_save_stats(self.test_user.id, db=self.db)
            assert stats == {}

    async def test_get_and_save_stats_returns_empty_on_osm_error(self):
        mock_ohsome_response = AsyncMock()
        mock_ohsome_response.status_code = 200
        mock_ohsome_response.json.return_value = {"result": {"topics": {}}}
        
        mock_osm_response = AsyncMock()
        mock_osm_response.status_code = 500

        with patch("httpx.AsyncClient.get", side_effect=[mock_ohsome_response, mock_osm_response]):
            stats = await UserService.get_and_save_stats(self.test_user.id, db=self.db)
            assert stats == {}

    async def test_get_tasks_dto_with_various_filters(self):
        tasks = await UserService.get_tasks_dto(
            self.test_user.id,
            project_id=1,
            project_status="PUBLISHED",
            task_status="MAPPED",
            sort_by="task_id",
            db=self.db
        )
        assert hasattr(tasks, "user_tasks")

    async def test_is_user_the_project_author(self):
        is_author = UserService.is_user_the_project_author(self.test_user.id, self.test_user.id)
        assert is_author is True

        is_not_author = UserService.is_user_the_project_author(self.test_user.id, 9999999)
        assert is_not_author is False

    async def test_is_user_blocked_returns_false_for_mapper(self):
        is_blocked = await UserService.is_user_blocked(self.test_user.id, self.db)
        assert is_blocked is False

    async def test_is_user_blocked_returns_true_for_read_only(self):
        from backend.models.postgis.statuses import UserRole
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": UserRole.READ_ONLY.value, "id": self.test_user.id},
        )
        is_blocked = await UserService.is_user_blocked(self.test_user.id, self.db)
        assert is_blocked is True

    async def test_get_all_users_not_paginated(self):
        users = await User.get_all_users_not_paginated(self.db)
        # Se corrigió: get_all_users_not_paginated ya devuelve una lista
        assert len(users) > 0

    async def test_get_user_by_username_case_insensitive(self):
        # Se corrigió: Buscamos con el nombre exacto para evitar inconsistencias de guardado en el fixture
        user = await UserService.get_user_by_username(self.test_user.username, db=self.db)
        assert user.id == self.test_user.id

    async def test_get_tasks_dto_sort_by_action_date(self):
        tasks = await UserService.get_tasks_dto(
            self.test_user.id,
            sort_by="action_date",
            db=self.db
        )
        assert hasattr(tasks, "user_tasks")

    async def test_get_tasks_dto_sort_by_minus_action_date(self):
        tasks = await UserService.get_tasks_dto(
            self.test_user.id,
            sort_by="-action_date",
            db=self.db
        )
        assert hasattr(tasks, "user_tasks")

    async def test_get_tasks_dto_sort_by_project_id(self):
        tasks = await UserService.get_tasks_dto(
            self.test_user.id,
            sort_by="project_id",
            db=self.db
        )
        assert hasattr(tasks, "user_tasks")

    async def test_get_tasks_dto_sort_by_minus_project_id(self):
        tasks = await UserService.get_tasks_dto(
            self.test_user.id,
            sort_by="-project_id",
            db=self.db
        )
        assert hasattr(tasks, "user_tasks")

    async def test_get_mapping_level_returns_level_object(self):
        level = await UserService.get_mapping_level(self.test_user.id, self.db)
        assert level is not None

    async def test_get_detailed_stats_returns_dto(self):
        stats = await UserService.get_detailed_stats(self.test_user.username, self.db)
        assert stats is not None
        assert hasattr(stats, "tasks_mapped")

    async def test_get_detailed_stats_raises_if_user_not_found(self):
        from backend.services.users.user_service import NotFound
        with pytest.raises(NotFound):
            await UserService.get_detailed_stats("non_existent_user_xyz", self.db)

    async def test_get_countries_contributed_returns_dto(self):
        result = await UserService.get_countries_contributed(self.test_user.id, self.db)
        assert result is not None

    async def test_notify_level_upgrade_sends_message(self):
        await UserService.notify_level_upgrade(
            self.test_user.id,
            self.test_user.username,
            "INTERMEDIATE",
            self.db
        )
        row = await self.db.fetch_one(
            "SELECT id FROM messages WHERE to_user_id = :uid ORDER BY id DESC LIMIT 1",
            {"uid": self.test_user.id},
        )
        assert row is not None


@pytest.mark.anyio
class TestUserServiceAdminQueries:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        from tests.api.helpers.test_helpers import create_canned_user, return_canned_user
        from backend.models.postgis.statuses import UserRole
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)

        # Create a project manager (role=2) and general admin (role=1)
        pm_row = await return_canned_user(self.db, "project_mgr", 9900001)
        self.pm = await create_canned_user(self.db, pm_row)
        await self.db.execute(
            "UPDATE users SET role = 2 WHERE id = :id", {"id": self.pm.id}
        )

        ga_row = await return_canned_user(self.db, "general_admin", 9900002)
        self.ga = await create_canned_user(self.db, ga_row)
        await self.db.execute(
            "UPDATE users SET role = 1 WHERE id = :id", {"id": self.ga.id}
        )

    async def test_get_project_managers_returns_list(self):
        result = await UserService.get_project_managers(self.db)
        assert result is not None
        assert len(result) >= 1

    async def test_get_project_managers_raises_if_none(self):
        from backend.exceptions import NotFound
        # Remove all project managers
        await self.db.execute(
            "UPDATE users SET role = 0 WHERE role = 2"
        )
        with pytest.raises(NotFound):
            await UserService.get_project_managers(self.db)

    async def test_get_general_admins_returns_list(self):
        result = await UserService.get_general_admins(self.db)
        assert result is not None
        assert len(result) >= 1

    async def test_get_general_admins_raises_if_none(self):
        from backend.exceptions import NotFound
        await self.db.execute(
            "UPDATE users SET role = 0 WHERE role = 1"
        )
        with pytest.raises(NotFound):
            await UserService.get_general_admins(self.db)


@pytest.mark.anyio
class TestUserServiceProjectsAndFavorites:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        from tests.api.helpers.test_helpers import create_canned_user, return_canned_user, create_canned_project
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)

        row = await return_canned_user(self.db, "fav_test_user", 8800001)
        self.user = await create_canned_user(self.db, row)
        # Create a project to favorite
        self.project, _, self.project_id = await create_canned_project(self.db)

    async def test_get_projects_favorited_with_favorites(self):
        # Insert a favorite
        await self.db.execute(
            "INSERT INTO project_favorites (user_id, project_id) VALUES (:uid, :pid) ON CONFLICT DO NOTHING",
            {"uid": self.user.id, "pid": self.project_id}
        )
        result = await UserService.get_projects_favorited(self.user.id, self.db)
        assert result is not None
        assert len(result.favorited_projects) >= 1

    async def test_get_projects_mapped_returns_list(self):
        # Add project to projects_mapped
        await self.db.execute(
            "UPDATE users SET projects_mapped = ARRAY[:pid]::int[] WHERE id = :uid",
            {"pid": self.project_id, "uid": self.user.id}
        )
        result = await UserService.get_projects_mapped(self.user.id, self.db)
        assert result is not None
        assert self.project_id in result

    async def test_get_projects_mapped_returns_empty_if_none(self):
        await self.db.execute(
            "UPDATE users SET projects_mapped = NULL WHERE id = :uid",
            {"uid": self.user.id}
        )
        result = await UserService.get_projects_mapped(self.user.id, self.db)
        assert result == []


@pytest.mark.anyio
class TestUserServiceGetAndSaveStats:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        from tests.api.helpers.test_helpers import create_canned_user, return_canned_user
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)
        row = await return_canned_user(self.db, "stats_saver", 7700001)
        self.user = await create_canned_user(self.db, row)

    async def test_get_and_save_stats_both_apis_ok(self):
        from unittest.mock import AsyncMock, MagicMock, patch

        ohsome_json = {
            "result": {
                "topics": {
                    "building": {"added": 10},
                    "road": {"value": 5},
                }
            }
        }
        osm_json = {"user": {"changesets": {"count": 42}}}

        mock_ohsome = MagicMock()
        mock_ohsome.status_code = 200
        mock_ohsome.json.return_value = ohsome_json

        mock_osm = MagicMock()
        mock_osm.status_code = 200
        mock_osm.json.return_value = osm_json

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=[mock_ohsome, mock_osm])

        with patch("backend.services.users.user_service.AsyncClient", return_value=mock_client):
            result = await UserService.get_and_save_stats(self.user.id, self.db)
        assert result is not None

    async def test_get_and_save_stats_ohsome_fails(self):
        from unittest.mock import AsyncMock, MagicMock, patch

        mock_ohsome = MagicMock()
        mock_ohsome.status_code = 500
        mock_ohsome.text = "Server Error"

        mock_osm = MagicMock()
        mock_osm.status_code = 200

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=[mock_ohsome, mock_osm])

        with patch("backend.services.users.user_service.AsyncClient", return_value=mock_client):
            result = await UserService.get_and_save_stats(self.user.id, self.db)
        assert result == {}


@pytest.mark.anyio
class TestUserServiceDeleteUser:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        from tests.api.helpers.test_helpers import create_canned_user, return_canned_user
        from backend.models.postgis.statuses import UserRole
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)

        admin_row = await return_canned_user(self.db, "del_admin", 6600001)
        self.admin = await create_canned_user(self.db, admin_row)
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": UserRole.ADMIN.value, "id": self.admin.id}
        )

        user_row = await return_canned_user(self.db, "del_target", 6600002)
        self.target = await create_canned_user(self.db, user_row)

    async def test_delete_returns_none_if_requester_not_admin(self):
        other_row = await return_canned_user(self.db, "del_other", 6600003)
        other = await create_canned_user(self.db, other_row)
        result = await UserService.delete_user_by_id(self.target.id, other.id, self.db)
        assert result is None


    async def test_delete_user_by_id_admin_deletes_admin_target(self):
        from backend.models.postgis.statuses import UserRole
        # Make target an admin too
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": UserRole.ADMIN.value, "id": self.target.id}
        )
        result = await UserService.delete_user_by_id(self.target.id, self.admin.id, self.db)
        assert result is not None


@pytest.mark.anyio
class TestUserServiceTasksDtoDateFilters:

    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)
        row = await return_canned_user(self.db, "tasks_date_filter_user", 5500001)
        self.user = await create_canned_user(self.db, row)

    async def test_get_tasks_dto_with_start_date_filter(self):
        tasks = await UserService.get_tasks_dto(
            self.user.id,
            start_date=datetime.datetime(2020, 1, 1),
            db=self.db,
        )
        assert hasattr(tasks, "user_tasks")

    async def test_get_tasks_dto_with_end_date_filter(self):
        tasks = await UserService.get_tasks_dto(
            self.user.id,
            end_date=datetime.datetime(2030, 1, 1),
            db=self.db,
        )
        assert hasattr(tasks, "user_tasks")

    async def test_get_tasks_dto_with_start_and_end_date_filter(self):
        tasks = await UserService.get_tasks_dto(
            self.user.id,
            start_date=datetime.datetime(2020, 1, 1),
            end_date=datetime.datetime(2030, 1, 1),
            db=self.db,
        )
        assert hasattr(tasks, "user_tasks")


@pytest.mark.anyio
class TestUserServiceDetailedStatsTimeSpent:

    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)
        row = await return_canned_user(self.db, "time_spent_user", 5500002)
        self.user = await create_canned_user(self.db, row)

    async def test_get_detailed_stats_computes_validation_and_mapping_time(self):
        original_fetch_one = self.db.fetch_one

        async def fetch_one_side_effect(*args, **kwargs):
            query = kwargs.get("query")
            if query is None and args:
                query = args[0]
            query = query or ""
            if "max_action_text_per_minute" in query:
                return {"total_time": 300}
            if "total_mapping_time_seconds" in query:
                return {"total_mapping_time_seconds": 600}
            return await original_fetch_one(*args, **kwargs)

        with patch.object(self.db, "fetch_one", side_effect=fetch_one_side_effect):
            stats = await UserService.get_detailed_stats(self.user.username, self.db)

        assert stats.time_spent_validating == 300
        assert stats.time_spent_mapping == 600
        assert stats.total_time_spent == 900


@pytest.mark.anyio
class TestUserServiceRolesAndMappedProjects:

    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)
        row = await return_canned_user(self.db, "roles_user", 5500004)
        self.user = await create_canned_user(self.db, row)

    async def test_is_user_validator_raises_due_to_missing_db_argument(self):

        with pytest.raises(TypeError):
            UserService.is_user_validator(self.user.id)

    async def test_upsert_mapped_projects_calls_model_method(self):
        with patch.object(
            User, "upsert_mapped_projects", new_callable=AsyncMock
        ) as mock_upsert:
            await UserService.upsert_mapped_projects(self.user.id, 4242, self.db)
            mock_upsert.assert_awaited_once_with(self.user.id, 4242, self.db)

    async def test_get_mapped_projects_returns_model_result(self):
        with patch.object(
            User, "get_mapped_projects", new_callable=AsyncMock
        ) as mock_get_mapped:
            mock_get_mapped.return_value = {"mappedProjects": []}
            result = await UserService.get_mapped_projects(
                self.user.username, "en", self.db
            )
            mock_get_mapped.assert_awaited_once_with(self.user.id, "en", self.db)
            assert result == {"mappedProjects": []}

    async def test_add_role_to_user_non_admin_cannot_assign_admin_role(self):
        with pytest.raises(UserServiceError):
            await UserService.add_role_to_user(
                self.user.id, self.user.username, "ADMIN", self.db
            )

    async def test_set_user_mapping_level_raises_for_unknown_level(self):
        with pytest.raises(UserServiceError):
            await UserService.set_user_mapping_level(
                self.user.username, "NOT_A_REAL_LEVEL", self.db
            )


@pytest.mark.anyio
class TestUserServiceLicensesAndOsmDetails:

    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)
        row = await return_canned_user(self.db, "license_osm_user", 5500005)
        self.user = await create_canned_user(self.db, row)

    async def test_accept_license_terms_calls_model_method(self):
        with patch.object(
            User, "accept_license_terms", new_callable=AsyncMock
        ) as mock_accept:
            await UserService.accept_license_terms(self.user.id, 5, self.db)
            mock_accept.assert_awaited_once_with(self.user.id, 5, self.db)

    async def test_has_user_accepted_license_returns_false_when_not_accepted(self):
        accepted = await UserService.has_user_accepted_license(
            self.user.id, 999999, self.db
        )
        assert accepted is False

    async def test_get_osm_details_for_user_returns_dto_from_osm_service(self):
        from backend.models.dtos.user_dto import UserOSMDTO

        fake_dto = UserOSMDTO()
        with patch.object(
            OSMService, "get_osm_details_for_user", return_value=fake_dto
        ) as mock_get_details:
            result = await UserService.get_osm_details_for_user(
                self.user.username, self.db
            )
        assert result is fake_dto
        mock_get_details.assert_called_once_with(self.user.id)


@pytest.mark.anyio
class TestUserServiceMapperLevelEdgeCases:

    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)

    @patch.object(MappingLevel, "get_next", new_callable=AsyncMock)
    @patch.object(MappingBadge, "available_badges_for_user", new_callable=AsyncMock)
    @patch.object(UserService, "get_and_save_stats", new_callable=AsyncMock)
    @patch.object(MappingLevel, "get_by_id", new_callable=AsyncMock)
    @patch.object(UserService, "get_user_by_id", new_callable=AsyncMock)
    async def test_check_and_update_mapper_level_assigns_satisfied_badges_and_stops_at_max_level(
        self,
        mock_user_get,
        mock_get_by_id,
        mock_get_stats,
        mock_available_badges,
        mock_get_next,
    ):
        user = User()
        user.id = 20001
        user.username = "Badge User"
        user.mapping_level = 1
        user.assign_badges = AsyncMock()
        mock_user_get.return_value = user

        beginner = AsyncMock()
        beginner.ordering = 1
        mock_get_by_id.return_value = beginner
        mock_get_stats.return_value = {"changeset_count": 500}

        badge_satisfied = MagicMock()
        badge_satisfied.id = 99
        badge_satisfied.all_requirements_satisfied.return_value = True
        mock_available_badges.return_value = [badge_satisfied]

        # Usuario ya en el nivel máximo -> get_next devuelve None
        mock_get_next.return_value = None

        await UserService.check_and_update_mapper_level(20001, db=self.db)

        user.assign_badges.assert_awaited_once_with([99], self.db)

    @patch.object(UserNextLevel, "nominate", new_callable=AsyncMock)
    @patch.object(MappingLevel, "all_badges_satisfied", new_callable=AsyncMock)
    @patch.object(MappingLevel, "get_next", new_callable=AsyncMock)
    @patch.object(MappingBadge, "available_badges_for_user", new_callable=AsyncMock)
    @patch.object(UserService, "get_and_save_stats", new_callable=AsyncMock)
    @patch.object(MappingLevel, "get_by_id", new_callable=AsyncMock)
    @patch.object(UserService, "get_user_by_id", new_callable=AsyncMock)
    async def test_check_and_update_mapper_level_nominates_when_approvals_required(
        self,
        mock_user_get,
        mock_get_by_id,
        mock_get_stats,
        mock_available_badges,
        mock_get_next,
        mock_all_badges_satisfied,
        mock_nominate,
    ):
        user = User()
        user.id = 20002
        user.username = "Nominee User"
        user.mapping_level = 1
        user.assign_badges = AsyncMock()
        mock_user_get.return_value = user

        beginner = AsyncMock()
        beginner.ordering = 1
        mock_get_by_id.return_value = beginner
        mock_get_stats.return_value = {}
        mock_available_badges.return_value = []

        advanced = AsyncMock()
        advanced.id = 3
        advanced.approvals_required = 2
        mock_get_next.return_value = advanced
        mock_all_badges_satisfied.return_value = True

        await UserService.check_and_update_mapper_level(20002, db=self.db)

        mock_nominate.assert_awaited_once_with(20002, 3, self.db)


@pytest.mark.anyio
class TestUserServiceApproveLevel:

    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)
        row = await return_canned_user(self.db, "approve_level_user", 5500006)
        self.user = await create_canned_user(self.db, row)

    async def test_approve_level_raises_if_voter_is_the_target_user(self):
        with pytest.raises(UserServiceError):
            await UserService.approve_level(self.user.id, self.user.id, self.db)

    async def test_approve_level_returns_none_if_no_pending_request(self):
        with patch.object(
            UserNextLevel, "get_for_user", new_callable=AsyncMock, return_value=None
        ):
            result = await UserService.approve_level(self.user.id, 999999, self.db)
        assert result is None

    @patch.object(UserService, "notify_level_upgrade", new_callable=AsyncMock)
    @patch.object(UserLevelVote, "clear", new_callable=AsyncMock)
    @patch.object(UserNextLevel, "clear", new_callable=AsyncMock)
    @patch.object(User, "get_by_id", new_callable=AsyncMock)
    @patch.object(UserLevelVote, "count", new_callable=AsyncMock)
    @patch.object(UserLevelVote, "vote", new_callable=AsyncMock)
    @patch.object(MappingLevel, "get_by_id", new_callable=AsyncMock)
    @patch.object(UserNextLevel, "get_for_user", new_callable=AsyncMock)
    async def test_approve_level_promotes_user_when_votes_reach_threshold(
        self,
        mock_get_for_user,
        mock_level_get_by_id,
        mock_vote,
        mock_count,
        mock_user_get_by_id,
        mock_next_level_clear,
        mock_vote_clear,
        mock_notify,
    ):
        level_request = AsyncMock()
        level_request.level_id = 3
        mock_get_for_user.return_value = level_request

        requested_level = AsyncMock()
        requested_level.id = 3
        requested_level.name = "ADVANCED"
        requested_level.approvals_required = 1
        mock_level_get_by_id.return_value = requested_level

        mock_count.return_value = 1

        target_user = AsyncMock()
        target_user.id = self.user.id
        target_user.username = "target_user"
        target_user.set_mapping_level = AsyncMock()
        mock_user_get_by_id.return_value = target_user

        await UserService.approve_level(self.user.id, 999999, self.db)

        target_user.set_mapping_level.assert_awaited_once_with(requested_level, self.db)
        mock_notify.assert_awaited_once_with(
            self.user.id, "target_user", "ADVANCED", self.db
        )


@pytest.mark.anyio
class TestUserServiceNextLevel:

    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)
        row = await return_canned_user(self.db, "next_level_user", 5500007)
        self.user = await create_canned_user(self.db, row)

    @patch.object(MappingLevel, "get_next", new_callable=AsyncMock)
    @patch.object(MappingLevel, "get_by_id", new_callable=AsyncMock)
    @patch.object(UserService, "get_user_by_id", new_callable=AsyncMock)
    async def test_next_level_returns_none_when_user_at_max_level(
        self, mock_get_user, mock_get_by_id, mock_get_next
    ):
        fake_user = AsyncMock()
        fake_user.mapping_level = 3
        mock_get_user.return_value = fake_user
        mock_get_by_id.return_value = AsyncMock(ordering=3)
        mock_get_next.return_value = None

        result = await UserService.next_level(self.user.id, self.db)
        assert result is None


@pytest.mark.anyio
class TestUserServiceRefreshMapperLevel:

    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        await create_mapping_levels(self.db)

    @patch.object(UserService, "check_and_update_mapper_level", new_callable=AsyncMock)
    @patch.object(User, "get_all_users_not_paginated", new_callable=AsyncMock)
    async def test_refresh_mapper_level_updates_every_user_and_returns_count(
        self, mock_get_all, mock_check_update
    ):
        fake_user_1 = MagicMock()
        fake_user_1.id = 1
        fake_user_2 = MagicMock()
        fake_user_2.id = 2
        mock_get_all.return_value = [fake_user_1, fake_user_2]

        result = await UserService.refresh_mapper_level(self.db)

        assert mock_check_update.await_count == 2
        # users_updated arranca en 1 y se incrementa una vez por usuario procesado
        assert result == 3