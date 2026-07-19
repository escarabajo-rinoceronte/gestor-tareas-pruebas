from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient

from backend.services.users.user_service import (
    NotFound,
    UserRole,
    UserService,
    UserServiceError,
)
from tests.api.helpers.test_helpers import (
    create_canned_user,
    return_canned_user,
)
from backend.models.postgis.user import (
    User,
    UserNextLevel,
    UserStats,
    UserLevelVote,
)
from backend.models.postgis.mapping_level import MappingLevel
from backend.models.postgis.mapping_badge import MappingBadge
from backend.models.dtos.mapping_badge_dto import MappingBadgeCreateDTO
from backend.models.dtos.mapping_level_dto import MappingLevelCreateDTO, AssociatedBadge


@pytest.mark.anyio
class TestUserService:
    @pytest.fixture(autouse=True)
    async def setup_test_data(self, db_connection_fixture, request):
        assert db_connection_fixture is not None, "Database connection is not available"
        request.cls.db = db_connection_fixture
        request.cls.test_user = await create_canned_user(db_connection_fixture)

    async def test_get_user_by_id_returns_user(self):
        # Act
        user = await UserService.get_user_by_id(self.test_user.id, self.db)

        # Assert
        assert user.username == self.test_user.username

    async def test_get_user_by_id_raises_error_if_user_not_found(self):
        with pytest.raises(NotFound):
            await UserService.get_user_by_id(123456, self.db)

    async def test_get_user_by_username_returns_user(self):
        # Act
        user = await UserService.get_user_by_username(self.test_user.username, self.db)

        # Assert
        assert user.id == self.test_user.id

    async def test_get_user_by_username_raises_error_if_user_not_found(self):
        with pytest.raises(NotFound):
            await UserService.get_user_by_username("Thinkwhere", self.db)

    async def test_is_user_admin_returns_true_for_admin(self):
        query = """
            UPDATE users
            SET role = :role
            WHERE id = :user_id
        """
        await self.db.execute(
            query, values={"user_id": self.test_user.id, "role": UserRole.ADMIN.value}
        )

        # Act
        result = await UserService.is_user_an_admin(self.test_user.id, self.db)

        # Assert
        assert result is True

    async def test_is_user_admin_returns_false_for_non_admin(self):
        # Assert
        assert await UserService.is_user_an_admin(self.test_user.id, self.db) is False

    async def test_unknown_role_raise_error_when_setting_role(self):
        with pytest.raises(UserServiceError):
            await UserService.add_role_to_user(1, "test", "TEST", self.db)

    async def test_get_mapping_level(self):
        # Assert
        level = await UserService.get_mapping_level(self.test_user.id, self.db)

        assert level.name == "BEGINNER"

    async def test_set_user_mapping_level(self):
        # Act
        await UserService.set_user_mapping_level(
            self.test_user.username, "ADVANCED", self.db
        )

        # Assert
        level = await UserService.get_mapping_level(self.test_user.id, self.db)

        assert level.name == "ADVANCED"
        assert not level.is_beginner

    async def test_unknown_level_raise_error_when_setting_level(self):
        with pytest.raises(UserServiceError):
            await UserService.set_user_mapping_level("test", "TEST", self.db)

    async def test_register_user_beginner(self):
        # Act
        registered_user = await UserService.register_user(
            1, "foo", 0, None, "foo@example.com", self.db
        )

        # Assert
        assert (
            registered_user.mapping_level
            == (await MappingLevel.get_by_name("BEGINNER", self.db)).id
        )

    @patch.object(AsyncClient, "get")
    async def test_get_and_save_stats(self, mock_get):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(
            return_value={
                "result": {
                    "topics": {"changeset": {"value": 251.0}},
                },
                "user": {
                    "changesets": {"count": 251.0},
                },
            },
        )
        mock_get.return_value = mock_response

        # Act
        await UserService.get_and_save_stats(self.test_user.id, self.db)

        # Assert
        stats = await UserStats.get_for_user(self.test_user.id, self.db)
        assert stats.stats == '{"changeset": 251.0}'

    async def test_get_and_save_stats_handles_ohsome_500(self):
        # Arrange: prepare an OHsome error response (500) and a harmless OSM response (200)
        ohsome_resp = AsyncMock()
        ohsome_resp.status_code = 500
        ohsome_resp.text = "Internal Server Error"
        ohsome_resp.json = MagicMock(
            return_value={
                "status": 500,
                "error": "Internal Server Error",
                "path": "/api/stats/user",
            }
        )

        changeset_resp = AsyncMock()
        changeset_resp.status_code = 200
        changeset_resp.json = MagicMock(
            return_value={"user": {"changesets": {"count": 0}}}
        )

        # Patch AsyncClient.get and UserStats.update
        with (
            patch.object(AsyncClient, "get", new_callable=AsyncMock) as mock_get,
            patch.object(UserStats, "update", new_callable=AsyncMock) as mock_update,
        ):
            # The function does two gets in sequence: ohsome then changeset
            mock_get.side_effect = [ohsome_resp, changeset_resp]

            # Act
            result = await UserService.get_and_save_stats(self.test_user.id, self.db)

            # Assert
            # function should return empty dict on OHsome 500
            assert result == {}

            # Ensure we tried the external calls (at least awaited once)
            mock_get.assert_awaited()

            # And we must NOT call UserStats.update when an upstream failed
            mock_update.assert_not_awaited()

    @patch.object(AsyncClient, "get")
    async def test_check_and_update_mapper_level_happy_path(self, mock_get):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(
            return_value={
                "result": {
                    "topics": {"changeset": {"value": 251.0}},
                },
                "user": {
                    "changesets": {"count": 251.0},
                },
            }
        )
        mock_get.return_value = mock_response

        # Act
        await UserService.check_and_update_mapper_level(self.test_user.id, self.db)

        # Assert
        # one badge is assigned
        badges = await MappingBadge.get_related_to_user(self.test_user.id, self.db)
        assert len(badges) == 1
        assert badges[0].name == "INTERMEDIATE_internal"
        # intermediate level is assigned
        user = await User.get_by_id(self.test_user.id, self.db)
        new_level = await MappingLevel.get_by_id(user.mapping_level, self.db)
        assert new_level.id == 2
        assert new_level.name == "INTERMEDIATE"
        # Message is sent
        message_count = await self.db.execute(
            "select count(*) from messages where to_user_id = :user_id",
            {
                "user_id": self.test_user.id,
            },
        )
        assert message_count == 1

    @patch.object(AsyncClient, "get")
    async def test_check_and_update_mapper_level_no_level_upgrade(self, mock_get):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(
            return_value={
                "result": {
                    "topics": {"changeset": {"value": 249.0}},
                },
                "user": {
                    "changesets": {"count": 249.0},
                },
            }
        )
        mock_get.return_value = mock_response

        # Act
        await UserService.check_and_update_mapper_level(self.test_user.id, self.db)

        # Assert
        # no badge is assigned
        badges = await MappingBadge.get_related_to_user(self.test_user.id, self.db)
        assert len(badges) == 0
        # no level is upgraded
        user = await User.get_by_id(self.test_user.id, self.db)
        new_level = await MappingLevel.get_by_id(user.mapping_level, self.db)
        assert new_level.id == 1
        assert new_level.name == "BEGINNER"

    @patch.object(AsyncClient, "get")
    async def test_check_and_update_mapper_level_pool_of_approval(self, mock_get):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(
            return_value={
                "result": {
                    "topics": {"changeset": {"value": 251.0}},
                },
                "user": {
                    "changesets": {"count": 251.0},
                },
            }
        )
        mock_get.return_value = mock_response
        await self.db.execute(
            "UPDATE mapping_levels SET approvals_required = 1 WHERE id = 2"
        )

        # Act
        await UserService.check_and_update_mapper_level(self.test_user.id, self.db)

        # Assert
        # a badge is assigned
        badges = await MappingBadge.get_related_to_user(self.test_user.id, self.db)
        assert len(badges) == 1
        # no level is upgraded
        user = await User.get_by_id(self.test_user.id, self.db)
        new_level = await MappingLevel.get_by_id(user.mapping_level, self.db)
        assert new_level.id == 1
        assert new_level.name == "BEGINNER"
        # user is added to the waiting queue
        assert await UserNextLevel.is_nominated(user.id, 2, self.db)

    @patch.object(AsyncClient, "get")
    async def test_check_and_update_mapper_level_max_level(self, mock_get):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(
            return_value={
                "result": {
                    "topics": {"changeset": {"value": 2000.0}},
                },
                "user": {
                    "changesets": {"count": 2000.0},
                },
            }
        )
        mock_get.return_value = mock_response
        await self.test_user.set_mapping_level(
            await MappingLevel.get_by_id(3, self.db), self.db
        )

        # Act
        await UserService.check_and_update_mapper_level(self.test_user.id, self.db)

        # Assert
        # no level is upgraded
        user = await User.get_by_id(self.test_user.id, self.db)
        new_level = await MappingLevel.get_by_id(user.mapping_level, self.db)
        assert new_level.id == 3
        assert new_level.name == "ADVANCED"

    @patch.object(AsyncClient, "get")
    async def test_check_and_update_mapper_level_assignes_badges_on_top_level(
        self, mock_get
    ):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(
            return_value={
                "result": {
                    "topics": {"changeset": {"value": 2000.0}},
                },
                "user": {
                    "changesets": {"count": 251.0},
                },
            }
        )
        mock_get.return_value = mock_response
        await self.test_user.set_mapping_level(
            await MappingLevel.get_by_id(3, self.db), self.db
        )
        badges = await MappingBadge.get_related_to_user(self.test_user.id, self.db)
        assert len(badges) == 0

        # Act
        await UserService.check_and_update_mapper_level(self.test_user.id, self.db)

        # Assert
        # no level is upgraded
        user = await User.get_by_id(self.test_user.id, self.db)
        new_level = await MappingLevel.get_by_id(user.mapping_level, self.db)
        assert new_level.id == 3
        assert new_level.name == "ADVANCED"
        # The badge is assigned
        badges = await MappingBadge.get_related_to_user(self.test_user.id, self.db)
        assert len(badges) == 1

    @patch.object(AsyncClient, "get")
    async def test_get_user_dto_by_username(self, mock_get):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = MagicMock(
            return_value={
                "result": {
                    "topics": {"changeset": {"value": 2000.0}},
                },
                "user": {
                    "changesets": {"count": 2000.0},
                },
            }
        )
        mock_get.return_value = mock_response
        # Act
        dto = await UserService.get_user_dto_by_username(
            self.test_user.username, self.test_user.id, self.db
        )

        # Assert
        assert dto.mapping_level == "BEGINNER"

    async def test_approve_level_needs_one_more(self):
        # Arrange
        badge = await MappingBadge.create(
            MappingBadgeCreateDTO(
                name="a badge",
                description="...",
                imagePath="/",
                requirements='{"roads": 10}',
            ),
            self.db,
        )
        level = await MappingLevel.create(
            MappingLevelCreateDTO(
                name="Super Mapper",
                approvalsRequired=2,
                color="#acabad",
                isBeginner=False,
                requiredBadges=[AssociatedBadge(id=badge.id)],
            ),
            self.db,
        )
        await UserNextLevel.nominate(self.test_user.id, level.id, self.db)

        other_user = await create_canned_user(
            self.db, await return_canned_user(self.db, id=24934, username="foo")
        )

        # Act
        await UserService.approve_level(self.test_user.id, other_user.id, self.db)

        # Assert
        user = await UserService.get_user_by_id(self.test_user.id, self.db)
        assert user.mapping_level != level.id
        assert await UserNextLevel.is_nominated(self.test_user.id, level.id, self.db)

    async def test_approve_level(self):
        # Arrange
        badge = await MappingBadge.create(
            MappingBadgeCreateDTO(
                name="a badge",
                description="...",
                imagePath="/",
                requirements='{"roads": 10}',
            ),
            self.db,
        )
        level = await MappingLevel.create(
            MappingLevelCreateDTO(
                name="Super Mapper",
                approvalsRequired=1,
                color="#acabad",
                isBeginner=False,
                requiredBadges=[AssociatedBadge(id=badge.id)],
            ),
            self.db,
        )
        await UserNextLevel.nominate(self.test_user.id, level.id, self.db)

        other_user = await create_canned_user(
            self.db, await return_canned_user(self.db, id=24934, username="foo")
        )

        # Act
        await UserService.approve_level(self.test_user.id, other_user.id, self.db)

        # Assert
        user = await UserService.get_user_by_id(self.test_user.id, self.db)
        # Level is upgraded
        assert user.mapping_level == level.id
        # user_next_level table is cleared
        assert not await UserNextLevel.is_nominated(
            self.test_user.id, level.id, self.db
        )
        # votes are cleared
        assert await UserLevelVote.count(self.test_user.id, level.id, self.db) == 0
        # Message is sent
        message_count = await self.db.execute(
            "select count(*) from messages where to_user_id = :user_id",
            {
                "user_id": self.test_user.id,
            },
        )
        assert message_count == 1

    async def test_next_level(self):
        next_level = await UserService.next_level(self.test_user.id, self.db)

        assert next_level.next_level == "INTERMEDIATE"
        assert next_level.aggregated_goal == 250
        assert next_level.aggregated_progress == 0
        assert next_level.metrics == ["changeset"]

    async def test_next_level_empy(self):
        await UserService.set_user_mapping_level(
            self.test_user.username, "ADVANCED", self.db
        )

        next_level = await UserService.next_level(self.test_user.id, self.db)

        assert next_level is None

    async def test_approve_level_raises_error_if_self_voting(self):
        with pytest.raises(UserServiceError, match="PermisisonError"):
            await UserService.approve_level(1, 1, self.db)

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_project_managers_raises_not_found(self, mock_fetch):
        mock_fetch.return_value = []
        with pytest.raises(NotFound):
            await UserService.get_project_managers(self.db)

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_general_admins_raises_not_found(self, mock_fetch):
        mock_fetch.return_value = []
        with pytest.raises(NotFound):
            await UserService.get_general_admins(self.db)

    async def test_is_user_the_project_author(self):
        assert UserService.is_user_the_project_author(1, 1) is True
        assert UserService.is_user_the_project_author(1, 2) is False

    @patch("backend.services.users.user_service.UserService.get_user_by_id")
    def test_is_user_validator(self, mock_get_user):
        mock_user = MagicMock()
        mock_user.role = UserRole.ADMIN.value
        mock_get_user.return_value = mock_user
        assert UserService.is_user_validator(1) is True

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=MagicMock)
    async def test_is_user_validator(self, mock_get_user):
        mock_user = MagicMock()
        mock_user.role = UserRole.ADMIN.value
        mock_get_user.return_value = mock_user
        
        assert UserService.is_user_validator(1) is True

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_register_user_with_email_raises_error_if_exists(self, mock_fetch):
        mock_fetch.return_value = MagicMock()
        mock_dto = MagicMock()
        mock_dto.email = "test@test.com"
        with pytest.raises(ValueError, match="already exists"):
            await UserService.register_user_with_email(mock_dto, self.db)

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    @patch("backend.services.messaging.smtp_service.SMTPService.send_verification_email", new_callable=AsyncMock)
    @patch("backend.models.postgis.user.User.set_email_verified_status", new_callable=AsyncMock)
    @patch("backend.models.postgis.user.User.update", new_callable=AsyncMock)
    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_update_user_details_sends_email(self, mock_fetch, mock_update, mock_set_email, mock_send, mock_get_user):
        mock_user = MagicMock()
        mock_user.email_address = "old@test.com"
        mock_get_user.return_value = mock_user
        
        mock_dto = MagicMock()
        mock_dto.email_address = "new@test.com"
        
        res = await UserService.update_user_details(1, mock_dto, self.db)
        assert res["verificationEmailSent"] is True
        mock_send.assert_awaited_once()

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_has_user_accepted_license(self, mock_fetch):
        mock_fetch.return_value = [True]
        res = await UserService.has_user_accepted_license(1, 1, self.db)
        assert res is True

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_projects_favorited_empty(self, mock_fetch):
        mock_fetch.return_value = []
        res = await UserService.get_projects_favorited(1, self.db)
        assert res.favorited_projects == []

    @patch("backend.services.users.user_service.UserService.is_user_an_admin", new_callable=AsyncMock)
    async def test_delete_user_by_id_permission_denied(self, mock_is_admin):
        mock_is_admin.return_value = False
        res = await UserService.delete_user_by_id(1, 2, self.db)
        assert res is None

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_countries_contributed(self, mock_fetch):
        mock_fetch.return_value = [{"name": "Peru", "mapped": 10, "validated": 5, "total": 15}]
        res = await UserService.get_countries_contributed(1, self.db)
        assert res.total == 1
        assert res.countries_contributed[0].name == "Peru"

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    @patch("backend.models.postgis.user.User.set_is_expert", new_callable=AsyncMock)
    async def test_set_user_is_expert(self, mock_set_expert, mock_get_user):
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user
        await UserService.set_user_is_expert(1, True, self.db)
        mock_set_expert.assert_awaited_once_with(mock_user, True, self.db)

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    async def test_update_user_changes_username(self, mock_get_user):
        mock_user = AsyncMock()
        mock_user.username = "old_name"
        mock_user.picture_url = "old_pic"
        mock_get_user.return_value = mock_user
        
        await UserService.update_user(1, "new_name", "new_pic", self.db)
        mock_user.update_username.assert_awaited_once_with("new_name", self.db)
        mock_user.update_picture_url.assert_awaited_once_with("new_pic", self.db)
        
    async def test_add_role_to_user_needs_admin(self):
        with patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock) as mock_get_user:
            mock_admin = MagicMock()
            mock_admin.role = UserRole.MAPPER.value
            mock_get_user.return_value = mock_admin
            
            with pytest.raises(UserServiceError, match="NeedAdminRole"):
                await UserService.add_role_to_user(1, "user1", "ADMIN", self.db)

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_contributions_by_day_returns_dtos(self, mock_fetch):
        mock_fetch.return_value = [
            {"day": datetime.utcnow().date(), "cnt": 3},
            {"day": (datetime.utcnow() - timedelta(days=1)).date(), "cnt": 5},
        ]
        result = await UserService.get_contributions_by_day(self.test_user.id, self.db)

        assert len(result) == 2
        assert result[0].count == 3
        assert result[1].count == 5

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_project_managers_success(self, mock_fetch):
        mock_fetch.return_value = [{"id": 1, "username": "pm_user"}]
        result = await UserService.get_project_managers(self.db)
        assert len(result) == 1

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_general_admins_success(self, mock_fetch):
        mock_fetch.return_value = [{"id": 1, "username": "admin_user"}]
        result = await UserService.get_general_admins(self.db)
        assert len(result) == 1

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_general_admins_raises_not_found(self, mock_fetch):
        mock_fetch.return_value = []
        with pytest.raises(NotFound):
            await UserService.get_general_admins(self.db)

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    async def test_update_user_no_changes(self, mock_get_user):
        mock_user = AsyncMock()
        mock_user.username = "same_name"
        mock_user.picture_url = "same_pic"
        mock_get_user.return_value = mock_user

        result = await UserService.update_user(1, "same_name", "same_pic", self.db)

        mock_user.update_username.assert_not_awaited()
        mock_user.update_picture_url.assert_not_awaited()
        assert result == mock_user

    @patch("backend.models.postgis.project.Project.as_dto_for_admin", new_callable=AsyncMock)
    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_projects_favorited_with_results(self, mock_fetch, mock_as_dto):
        mock_fetch.return_value = [{"project_id": 1}, {"project_id": 2}]
        mock_as_dto.side_effect = [MagicMock(name="p1"), MagicMock(name="p2")]

        result = await UserService.get_projects_favorited(self.test_user.id, self.db)

        assert len(result.favorited_projects) == 2
        assert mock_as_dto.await_count == 2

    async def test_is_user_blocked_true_for_read_only(self):
        query = "UPDATE users SET role = :role WHERE id = :user_id"
        await self.db.execute(
            query, values={"user_id": self.test_user.id, "role": UserRole.READ_ONLY.value}
        )
        assert await UserService.is_user_blocked(self.test_user.id, self.db) is True

    async def test_is_user_blocked_false_for_mapper(self):
        assert await UserService.is_user_blocked(self.test_user.id, self.db) is False

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    async def test_update_user_changes_username_and_picture(self, mock_get_user):
        mock_user = AsyncMock()
        mock_user.username = "old_name"
        mock_user.picture_url = "old_pic"
        mock_get_user.return_value = mock_user

        result = await UserService.update_user(1, "new_name", "new_pic", self.db)

        mock_user.update_username.assert_awaited_once_with("new_name", self.db)
        mock_user.update_picture_url.assert_awaited_once_with("new_pic", self.db)
        assert result == mock_user

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    async def test_update_user_no_changes(self, mock_get_user):
        mock_user = AsyncMock()
        mock_user.username = "same_name"
        mock_user.picture_url = "same_pic"
        mock_get_user.return_value = mock_user

        result = await UserService.update_user(1, "same_name", "same_pic", self.db)

        mock_user.update_username.assert_not_awaited()
        mock_user.update_picture_url.assert_not_awaited()
        assert result == mock_user

    async def test_get_projects_mapped_empty(self):
        projects = await UserService.get_projects_mapped(self.test_user.id, self.db)
        assert projects == []

    @patch("backend.services.users.user_service.UserService.check_and_update_mapper_level", new_callable=AsyncMock)
    @patch("backend.models.postgis.user.User.as_dto", new_callable=AsyncMock)
    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_get_user_dto_by_username_success(self, mock_fetch, mock_as_dto, mock_check_level):
        mock_fetch.return_value = {"id": 1, "username": "testuser"}
        mock_as_dto.return_value = MagicMock()
        mock_check_level.return_value = None

        with patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock) as mock_get_user:
            mock_get_user.return_value = MagicMock(id=1, username="logged_in")
            
            result = await UserService.get_user_dto_by_username("testuser", 1, self.db)
            
            assert result is not None
            mock_check_level.assert_called_once()

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_get_user_dto_by_username_not_found(self, mock_fetch):
        mock_fetch.return_value = None

        with pytest.raises(NotFound, match="USER_NOT_FOUND"):
            await UserService.get_user_dto_by_username("nonexistent", 1, self.db)

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    async def test_get_user_dto_by_id_success(self, mock_get_user):
        mock_request_user = MagicMock()
        mock_request_user.username = "logged_in"
        mock_get_user.side_effect = [self.test_user, mock_request_user]

        with patch("backend.models.postgis.user.User.as_dto", new_callable=AsyncMock) as mock_as_dto:
            mock_as_dto.return_value = MagicMock()
            
            result = await UserService.get_user_dto_by_id(self.test_user.id, 1, self.db)
            
            assert result is not None

    @patch("backend.services.users.user_service.UserService.is_user_an_admin", new_callable=AsyncMock)
    @patch("backend.services.users.user_service.UserService.get_user_dto_by_id", new_callable=AsyncMock)
    async def test_delete_user_by_id_self_delete(self, mock_get_dto, mock_is_admin):
        mock_get_dto.return_value = MagicMock()
        mock_is_admin.return_value = False

        with patch("databases.Database.transaction") as mock_transaction:
            mock_transaction.return_value.__aenter__.return_value = None
            mock_transaction.return_value.__aexit__.return_value = None
            
            result = await UserService.delete_user_by_id(1, 1, self.db)
            
            assert result is not None

    @patch("backend.services.users.user_service.UserService.is_user_an_admin", new_callable=AsyncMock)
    async def test_delete_user_by_id_admin_delete_other(self, mock_is_admin):
        mock_is_admin.return_value = True

        with patch("backend.services.users.user_service.UserService.get_user_dto_by_id", new_callable=AsyncMock) as mock_get_dto:
            mock_get_dto.return_value = MagicMock()
            
            with patch("databases.Database.transaction") as mock_transaction:
                mock_transaction.return_value.__aenter__.return_value = None
                mock_transaction.return_value.__aexit__.return_value = None
                
                result = await UserService.delete_user_by_id(2, 1, self.db)
                
                assert result is not None

    @patch("backend.services.users.user_service.UserService.is_user_an_admin", new_callable=AsyncMock)
    async def test_delete_user_by_id_permission_denied(self, mock_is_admin):
        mock_is_admin.return_value = False

        result = await UserService.delete_user_by_id(2, 1, self.db)

        assert result is None

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_interests_stats_with_data(self, mock_fetch):
        mock_fetch.return_value = [
            {"id": 1, "name": "Interest1", "count_projects": 5},
            {"id": 2, "name": "Interest2", "count_projects": 3},
        ]

        result = await UserService.get_interests_stats(self.test_user.id, self.db)

        assert len(result) == 2
        assert result[0].id == 1
        assert result[0].name == "Interest1"

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_interests_stats_empty(self, mock_fetch):
        mock_fetch.return_value = []

        result = await UserService.get_interests_stats(self.test_user.id, self.db)

        assert result == []

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    @patch("backend.models.postgis.task.Task.task_as_dto", new_callable=AsyncMock)
    async def test_get_tasks_dto_with_filters(self, mock_task_as_dto, mock_fetch_all):
        mock_fetch_all.return_value = [
            {"project_id": 1, "task_id": 1, "max": datetime.utcnow(), "comments": 0}
        ]
        mock_task_as_dto.return_value = MagicMock()

        result = await UserService.get_tasks_dto(
            user_id=self.test_user.id,
            task_status="MAPPED",
            project_id=1,
            page=1,
            page_size=10,
            db=self.db
        )

        assert result.user_tasks is not None
        assert result.pagination is not None

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_tasks_dto_empty(self, mock_fetch_all):
        mock_fetch_all.return_value = []

        result = await UserService.get_tasks_dto(
            user_id=self.test_user.id,
            db=self.db
        )

        assert result.user_tasks == []

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_get_detailed_stats_user_not_found(self, mock_fetch_one):
        mock_fetch_one.return_value = None

        with pytest.raises(NotFound, match="USER_NOT_FOUND"):
            await UserService.get_detailed_stats("nonexistent", self.db)

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_get_recommended_projects_user_not_found(self, mock_fetch_one):
        mock_fetch_one.return_value = None

        with pytest.raises(NotFound, match="USER_NOT_FOUND"):
            await UserService.get_recommended_projects("nonexistent", "en", self.db)

    @patch("backend.services.users.user_service.OSMService.get_osm_details_for_user")
    @patch("backend.services.users.user_service.UserService.get_user_by_username", new_callable=AsyncMock)
    async def test_get_osm_details_for_user_success(self, mock_get_user, mock_osm):
        mock_get_user.return_value = MagicMock(id=1)
        mock_osm.return_value = MagicMock()

        result = await UserService.get_osm_details_for_user("testuser", self.db)

        assert result is not None

    @patch("backend.services.users.user_service.User.get_all_users_not_paginated", new_callable=AsyncMock)
    @patch("backend.services.users.user_service.UserService.check_and_update_mapper_level", new_callable=AsyncMock)
    async def test_refresh_mapper_level(self, mock_check_level, mock_get_users):
        mock_get_users.return_value = [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3)]

        result = await UserService.refresh_mapper_level(self.db)

        assert result == 4
        assert mock_check_level.call_count == 3

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_has_user_accepted_license_true(self, mock_fetch):
        mock_fetch.return_value = [True]

        result = await UserService.has_user_accepted_license(1, 1, self.db)

        assert result is True

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_has_user_accepted_license_false(self, mock_fetch):
        mock_fetch.return_value = [False]

        result = await UserService.has_user_accepted_license(1, 1, self.db)

        assert result is False

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_countries_contributed_with_data(self, mock_fetch):
        mock_fetch.return_value = [
            {"name": "Peru", "mapped": 10, "validated": 5, "total": 15},
            {"name": "Brazil", "mapped": 8, "validated": 3, "total": 11},
        ]

        result = await UserService.get_countries_contributed(self.test_user.id, self.db)

        assert result.total == 2
        assert result.countries_contributed[0].name == "Peru"
        assert result.countries_contributed[0].mapped == 10

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_countries_contributed_empty(self, mock_fetch):
        mock_fetch.return_value = []

        result = await UserService.get_countries_contributed(self.test_user.id, self.db)

        assert result.total == 0
        assert result.countries_contributed == []

    async def test_is_user_blocked_true_for_read_only(self):
        query = "UPDATE users SET role = :role WHERE id = :user_id"
        await self.db.execute(
            query, values={"user_id": self.test_user.id, "role": UserRole.READ_ONLY.value}
        )

        result = await UserService.is_user_blocked(self.test_user.id, self.db)

        assert result is True

    async def test_is_user_blocked_false_for_mapper(self):
        result = await UserService.is_user_blocked(self.test_user.id, self.db)

        assert result is False

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    async def test_get_projects_mapped_with_data(self, mock_get_user):
        mock_user = MagicMock()
        mock_user.projects_mapped = [1, 2, 3]
        mock_get_user.return_value = mock_user

        result = await UserService.get_projects_mapped(1, self.db)

        assert result == [1, 2, 3]

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    async def test_update_user_only_username_changes(self, mock_get_user):
        mock_user = AsyncMock()
        mock_user.username = "old_name"
        mock_user.picture_url = "same_pic"
        mock_get_user.return_value = mock_user

        result = await UserService.update_user(1, "new_name", "same_pic", self.db)

        mock_user.update_username.assert_awaited_once_with("new_name", self.db)
        mock_user.update_picture_url.assert_not_awaited()
        assert result == mock_user

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    async def test_update_user_only_picture_changes(self, mock_get_user):
        mock_user = AsyncMock()
        mock_user.username = "same_name"
        mock_user.picture_url = "old_pic"
        mock_get_user.return_value = mock_user

        result = await UserService.update_user(1, "same_name", "new_pic", self.db)

        mock_user.update_username.assert_not_awaited()
        mock_user.update_picture_url.assert_awaited_once_with("new_pic", self.db)
        assert result == mock_user

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    @patch("backend.services.project_search_service.ProjectSearchService.get_total_contributions", new_callable=AsyncMock)
    @patch("backend.services.project_search_service.ProjectSearchService.create_result_dto", new_callable=AsyncMock)
    async def test_get_recommended_projects_with_campaign_tags(
        self, mock_create_dto, mock_get_contrib, mock_fetch_all, mock_fetch_one
    ):
        mock_fetch_one.return_value = {"id": 1, "mapping_level": 1}

        mock_fetch_all.side_effect = [
            [{"project_id": 1}],
            [{"tag": "campaign1"}],
            [{"id": 1, "name": "Project1", "difficulty": 1}],
            [],
        ]

        mock_get_contrib.return_value = [5]
        mock_create_dto.return_value = MagicMock()

        result = await UserService.get_recommended_projects(
            "testuser", "en", self.db
        )

        assert result.results is not None

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    @patch("backend.services.project_search_service.ProjectSearchService.get_total_contributions", new_callable=AsyncMock)
    @patch("backend.services.project_search_service.ProjectSearchService.create_result_dto", new_callable=AsyncMock)
    async def test_get_recommended_projects_with_remaining(
        self, mock_create_dto, mock_get_contrib, mock_fetch_all, mock_fetch_one
    ):
        mock_fetch_one.return_value = {"id": 1, "mapping_level": 1}

        mock_fetch_all.side_effect = [
            [{"project_id": 1}],
            [],
            [],
            [{"id": 2, "name": "Project2", "difficulty": 1}],
        ]

        mock_get_contrib.return_value = [5]
        mock_create_dto.return_value = MagicMock()

        result = await UserService.get_recommended_projects(
            "testuser", "en", self.db
        )

        assert result.results is not None

    @patch("backend.services.users.user_service.UserNextLevel.get_for_user")
    async def test_approve_level_no_request(self, mock_get_request):
        mock_get_request.return_value = None

        await UserService.approve_level(1, 2, self.db)

        mock_get_request.assert_called_once_with(1, self.db)

    @patch("backend.services.users.user_service.UserNextLevel.get_for_user")
    async def test_approve_level_self_vote_error(self, mock_get_request):
        with pytest.raises(UserServiceError, match="PermisisonError"):
            await UserService.approve_level(1, 1, self.db)

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    @patch("backend.services.project_search_service.ProjectSearchService.get_total_contributions", new_callable=AsyncMock)
    @patch("backend.services.project_search_service.ProjectSearchService.create_result_dto", new_callable=AsyncMock)
    async def test_get_recommended_projects_with_no_campaigns(
        self, mock_create_dto, mock_get_contrib, mock_fetch_all, mock_fetch_one
    ):
        mock_fetch_one.return_value = {"id": 1, "mapping_level": 1}

        mock_fetch_all.side_effect = [
            [{"project_id": 1}],
            [],
            [],
            [{"id": 2, "name": "Project2", "difficulty": 1}],
            [],
        ]

        mock_get_contrib.return_value = [5]
        mock_create_dto.return_value = MagicMock()

        result = await UserService.get_recommended_projects(
            "testuser", "en", self.db
        )

        assert result.results is not None

    @patch("backend.services.users.user_service.OSMService.get_osm_details_for_user")
    @patch("backend.services.users.user_service.UserService.get_user_by_username", new_callable=AsyncMock)
    async def test_get_osm_details_for_user_returns_dto(self, mock_get_user, mock_osm):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_get_user.return_value = mock_user

        mock_osm_dto = MagicMock()
        mock_osm.return_value = mock_osm_dto

        result = await UserService.get_osm_details_for_user("testuser", self.db)

        assert result == mock_osm_dto

    @patch("databases.Database.fetch_one", new_callable=AsyncMock)
    async def test_has_user_accepted_license_returns_false(self, mock_fetch):
        mock_fetch.return_value = [False]

        result = await UserService.has_user_accepted_license(1, 1, self.db)

        assert result is False

    @patch("databases.Database.fetch_all", new_callable=AsyncMock)
    async def test_get_countries_contributed_with_multiple_countries(self, mock_fetch):
        mock_fetch.return_value = [
            {"name": "Peru", "mapped": 10, "validated": 5, "total": 15},
            {"name": "Brazil", "mapped": 8, "validated": 3, "total": 11},
            {"name": "Chile", "mapped": 3, "validated": 2, "total": 5},
        ]

        result = await UserService.get_countries_contributed(self.test_user.id, self.db)

        assert result.total == 3
        assert result.countries_contributed[0].name == "Peru"
        assert result.countries_contributed[1].name == "Brazil"
        assert result.countries_contributed[2].name == "Chile"

    @patch("backend.services.users.user_service.UserService.get_user_by_id", new_callable=AsyncMock)
    async def test_is_user_blocked_returns_false_for_admin(self, mock_get_user):
        mock_user = MagicMock()
        mock_user.role = UserRole.ADMIN.value
        mock_get_user.return_value = mock_user

        result = await UserService.is_user_blocked(1, self.db)

        assert result is False