import base64
import pytest
from httpx import AsyncClient

from unittest.mock import patch, AsyncMock

from backend.services.users.authentication_service import AuthenticationService
from backend.models.postgis.task import Task, TaskStatus
from backend.models.postgis.statuses import UserGender, UserRole
from backend.exceptions import get_message_from_sub_code

from tests.api.helpers.test_helpers import (
    create_canned_user,
    return_canned_user,
    create_canned_project,
    create_canned_interest,
)

TEST_USERNAME = "test_user"
TEST_USER_ID = 1111111
TEST_EMAIL = "test@hotmail.com"

USER_NOT_FOUND_SUB_CODE = "USER_NOT_FOUND"
USER_NOT_FOUND_MESSAGE = get_message_from_sub_code(USER_NOT_FOUND_SUB_CODE)


def make_token_for_user(user_id: int) -> str:
    raw = AuthenticationService.generate_session_token_for_user(user_id)
    return f"Token {base64.b64encode(raw.encode('utf-8')).decode('utf-8')}"


def assert_user_detail_response(
    response,
    user_id=TEST_USER_ID,
    username=TEST_USERNAME,
    email=TEST_EMAIL,
    gender=None,
    own_info=True,
):
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == user_id
    assert body["username"] == username
    if own_info:
        assert body["emailAddress"] == email
        assert body["gender"] == gender
        assert body["isEmailVerified"] is False
    else:
        assert body["emailAddress"] is None
        assert body["gender"] is None
        assert body["selfDescriptionGender"] is None


@pytest.mark.anyio
class TestUsersQueriesOwnLockedDetailsAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        user_row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, user_row)
        self.user_session_token = make_token_for_user(self.user.id)
        self.url = "/api/v2/users/queries/tasks/locked/details/"

    async def test_returns_403_without_session_token(self, client: AsyncClient):
        resp = await client.get(self.url)
        assert resp.status_code == 403

    async def test_returns_404_if_no_tasks_locked(self, client: AsyncClient):
        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        assert resp.status_code == 404
        assert resp.json()["error"]["sub_code"] == "TASK_NOT_FOUND"

    async def test_returns_200_if_tasks_locked(self, client: AsyncClient):
        self.test_project, self.test_author, self.test_project_id = (
            await create_canned_project(self.db)
        )
        await Task.lock_task_for_mapping(1, self.test_project_id, self.user.id, self.db)
        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["tasks"]) == 1
        assert body["tasks"][0]["taskId"] == 1
        assert body["tasks"][0]["projectId"] == self.test_project_id


@pytest.mark.anyio
class TestUsersQueriesUsernameAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        user_row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, user_row)
        self.user_session_token = make_token_for_user(self.user.id)
        self.url = f"/api/v2/users/queries/{self.user.username}/"

    async def test_returns_403_without_session_token(self, client: AsyncClient):
        resp = await client.get(self.url)
        assert resp.status_code == 403

    async def test_returns_404_if_user_not_found(self, client: AsyncClient):
        resp = await client.get(
            "/api/v2/users/queries/unknown_user/",
            headers={"Authorization": self.user_session_token},
        )
        assert resp.status_code == 404
        assert resp.json()["error"]["sub_code"] == USER_NOT_FOUND_SUB_CODE

    async def test_returns_email_and_gender_if_own_info_requested(
        self, client: AsyncClient
    ):
        await self.db.execute(
            "UPDATE users SET email_address = :email, gender = :gender WHERE id = :id",
            {"email": TEST_EMAIL, "gender": UserGender.MALE.value, "id": self.user.id},
        )

        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        assert_user_detail_response(
            resp, TEST_USER_ID, TEST_USERNAME, TEST_EMAIL, UserGender.MALE.name, True
        )

    async def test_email_and_gender_not_returned_if_requested_by_other(
        self, client: AsyncClient
    ):
        await self.db.execute(
            "UPDATE users SET email_address = :email, gender = :gender WHERE id = :id",
            {
                "email": TEST_EMAIL,
                "gender": UserGender.FEMALE.value,
                "id": self.user.id,
            },
        )

        other_row = await return_canned_user(self.db, "user_2", 2222222)
        other = await create_canned_user(self.db, other_row)
        other_token = make_token_for_user(other.id)

        resp = await client.get(self.url, headers={"Authorization": other_token})
        assert_user_detail_response(
            resp, TEST_USER_ID, TEST_USERNAME, None, None, False
        )


@pytest.mark.anyio
class TestUsersQueriesOwnLockedAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        user_row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, user_row)
        self.user_session_token = make_token_for_user(self.user.id)
        self.url = "/api/v2/users/queries/tasks/locked/"

    async def test_returns_403_without_session_token(self, client: AsyncClient):
        resp = await client.get(self.url)
        assert resp.status_code == 403

    async def test_returns_empty_list_if_no_tasks_locked(self, client: AsyncClient):
        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["lockedTasks"] == []
        assert body["projectId"] is None
        assert body["taskStatus"] is None

    async def test_returns_locked_task_if_tasks_locked(self, client: AsyncClient):
        self.test_project, self.test_author, self.test_project_id = (
            await create_canned_project(self.db)
        )
        await Task.lock_task_for_mapping(1, self.test_project_id, self.user.id, self.db)

        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        body = resp.json()
        assert resp.status_code == 200
        assert body["lockedTasks"] == [1]
        assert body["projectId"] == self.test_project_id
        assert body["taskStatus"] == TaskStatus.LOCKED_FOR_MAPPING.name


@pytest.mark.anyio
class UsersQueriesInterestsAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        user_row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, user_row)
        self.user_session_token = make_token_for_user(self.user.id)
        self.url = f"/api/v2/users/{self.user.username}/queries/interests/"

    async def test_returns_403_without_session_token(self, client: AsyncClient):
        resp = await client.get(self.url)
        assert resp.status_code == 403

    async def test_returns_empty_list_if_no_interests(self, client: AsyncClient):
        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        assert resp.status_code == 200
        assert resp.json()["interests"] == []

    async def test_returns_404_if_user_not_found(self, client: AsyncClient):
        resp = await client.get(
            "/api/v2/users/invalid_username/queries/interests/",
            headers={"Authorization": self.user_session_token},
        )
        assert resp.status_code == 404
        assert resp.json()["error"]["sub_code"] == USER_NOT_FOUND_SUB_CODE

    async def test_returns_user_interests_if_interest_found(self, client: AsyncClient):
        i1 = await create_canned_interest(self.db, name="interest_1")
        i2 = await create_canned_interest(self.db, name="interest_2")

        await self.db.execute_many(
            """
            INSERT INTO user_interests (user_id, interest_id) VALUES (:user_id, :interest_id)
            """,
            [
                {"user_id": self.user.id, "interest_id": i1.id},
                {"user_id": self.user.id, "interest_id": i2.id},
            ],
        )

        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        body = resp.json()
        assert resp.status_code == 200
        assert len(body["interests"]) == 2
        assert body["interests"][0]["id"] == i1.id
        assert body["interests"][0]["name"] == i1.name
        assert body["interests"][1]["id"] == i2.id
        assert body["interests"][1]["name"] == i2.name


@pytest.mark.anyio
class TestUsersQueriesUsernameFilterAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row1 = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, row1)
        row2 = await return_canned_user(self.db, "user_2", 2222222)
        self.user_2 = await create_canned_user(self.db, row2)
        row3 = await return_canned_user(self.db, "user_3", 3333333)
        self.user_3 = await create_canned_user(self.db, row3)

        self.user_session_token = make_token_for_user(self.user.id)
        self.url = "/api/v2/users/queries/filter/tes/"

    async def test_returns_403_without_session_token(self, client: AsyncClient):
        resp = await client.get(self.url)
        assert resp.status_code == 403

    async def test_returns_404_if_no_users_found(self, client: AsyncClient):
        resp = await client.get(
            "/api/v2/users/queries/filter/invalid_username/",
            headers={"Authorization": self.user_session_token},
        )
        assert resp.status_code == 404
        assert resp.json()["error"]["sub_code"] == USER_NOT_FOUND_SUB_CODE

    async def test_returns_users_if_users_found(self, client: AsyncClient):
        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        assert resp.status_code == 200
        keys = list(resp.json().keys())
        assert "pagination" in keys and "usernames" in keys and "users" in keys
        assert len(resp.json()["usernames"]) == 1
        assert resp.json()["usernames"][0] == self.user.username
        assert resp.json()["pagination"]["page"] == 1
        assert resp.json()["pagination"]["perPage"] == 20
        assert resp.json()["pagination"]["total"] == 1

    async def test_returnns_matching_project_contributors(self, client: AsyncClient):
        self.test_project, self.test_author, self.test_project_id = (
            await create_canned_project(self.db)
        )

        await Task.get(1, self.test_project_id, self.db)
        await Task.lock_task_for_mapping(
            1, self.test_project_id, self.user_2.id, self.db
        )
        await Task.unlock_task(
            1, self.test_project_id, self.user_2.id, TaskStatus.MAPPED, self.db
        )

        resp = await client.get(
            f"/api/v2/users/queries/filter/user_/?projectId={self.test_project_id}",
            headers={"Authorization": self.user_session_token},
        )
        assert resp.status_code == 200
        assert len(resp.json()["usernames"]) == 2
        assert resp.json()["usernames"][0] == self.user_2.username
        assert resp.json()["usernames"][1] == self.user_3.username
        assert resp.json()["users"][0]["username"] == self.user_2.username
        assert resp.json()["users"][0]["projectId"] == self.test_project_id


@pytest.mark.anyio
class TestUsersAllAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, row)
        self.user_session_token = make_token_for_user(self.user.id)

        for i in range(30):
            row = await return_canned_user(self.db, f"user_{i}", i)
            await create_canned_user(self.db, row)

        self.url = "/api/v2/users/"

    async def test_returns_403_without_session_token(self, client: AsyncClient):
        resp = await client.get(self.url)
        assert resp.status_code == 403

    async def test_returns_400_if_invalid_role(self, client: AsyncClient):
        resp = await client.get(
            self.url,
            headers={"Authorization": self.user_session_token},
            params={"role": "GOD"},
        )
        assert resp.status_code == 400
        assert resp.json()["SubCode"] == "InvalidData"

    async def test_returns_per_page_20_users_by_default(self, client: AsyncClient):
        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        assert resp.status_code == 200
        assert len(resp.json()["users"]) == 20
        assert resp.json()["pagination"]["page"] == 1
        assert resp.json()["pagination"]["perPage"] == 20
        assert resp.json()["pagination"]["total"] == 31

    async def test_pagination_can_be_disabled(self, client: AsyncClient):
        resp = await client.get(
            self.url,
            headers={"Authorization": self.user_session_token},
            params={"pagination": "false"},
        )
        assert resp.status_code == 200
        assert len(resp.json()["users"]) == 31

    async def test_returns_specified_per_page_users(self, client: AsyncClient):
        resp = await client.get(
            self.url,
            headers={"Authorization": self.user_session_token},
            params={"perPage": 10},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["users"]) == 10
        assert body["pagination"]["page"] == 1
        assert body["pagination"]["perPage"] == 10
        assert body["pagination"]["total"] == 31
        assert body["pagination"]["hasNext"] is True
        assert body["pagination"]["pages"] == 4

    async def test_returns_specified_page_users(self, client: AsyncClient):
        resp = await client.get(
            self.url,
            headers={"Authorization": self.user_session_token},
            params={"page": 2},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["users"]) == 11
        assert body["pagination"]["page"] == 2
        assert body["pagination"]["hasNext"] is False
        assert body["pagination"]["hasPrev"] is True
        assert body["pagination"]["pages"] == 2

    async def test_returns_users_with_specified_role_(self, client: AsyncClient):
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": UserRole.ADMIN.value, "id": self.user.id},
        )

        resp = await client.get(
            self.url,
            headers={"Authorization": self.user_session_token},
            params={"role": "ADMIN"},
        )
        assert resp.status_code == 200
        assert len(resp.json()["users"]) == 1
        assert resp.json()["pagination"]["page"] == 1
        assert resp.json()["pagination"]["total"] == 1

    async def test_returns_users_with_specified_level(self, client: AsyncClient):
        level_url = "api/v2/levels/"
        levels = await client.get(level_url)
        level_results = levels.json()["levels"]
        test_level = level_results[2]
        await self.db.execute(
            "UPDATE users SET mapping_level = :lvl WHERE id = :id",
            {"lvl": test_level["id"], "id": self.user.id},
        )

        resp = await client.get(
            self.url,
            headers={"Authorization": self.user_session_token},
            params={"level": test_level["id"]},
        )
        assert resp.status_code == 200
        assert len(resp.json()["users"]) == 1
        assert resp.json()["users"][0]["mappingLevel"] == test_level["name"]
        assert resp.json()["pagination"]["page"] == 1
        assert resp.json()["pagination"]["total"] == 1


@pytest.mark.anyio
class TestUsersRecommendedProjectsAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, row)
        self.user_session_token = make_token_for_user(self.user.id)
        self.url = f"/api/v2/users/{self.user.username}/recommended-projects/"

    async def test_returns_403_without_session_token(self, client: AsyncClient):
        resp = await client.get(self.url)
        assert resp.status_code == 403

    async def test_returns_404_if_user_does_not_exist(self, client: AsyncClient):
        resp = await client.get(
            "/api/v2/users/non_existent/recommended-projects/",
            headers={"Authorization": self.user_session_token},
        )
        assert resp.status_code == 404

    async def test_returns_recommended_projects(self, client: AsyncClient):
        await create_canned_project(self.db)
        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        assert resp.status_code == 200


@pytest.mark.anyio
class TestUsersRestAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, row)
        self.user_session_token = make_token_for_user(self.user.id)
        self.url = f"/api/v2/users/{self.user.id}/"

    async def test_returns_403_without_session_token(self, client: AsyncClient):
        resp = await client.get(self.url)
        assert resp.status_code == 403

    async def test_returns_404_if_user_does_not_exist(self, client: AsyncClient):
        resp = await client.get(
            "/api/v2/users/999/", headers={"Authorization": self.user_session_token}
        )
        assert resp.status_code == 404

    async def test_returns_email_and_gender_if_own_info_requested(
        self, client: AsyncClient
    ):
        await self.db.execute(
            "UPDATE users SET email_address = :email, gender = :gender WHERE id = :id",
            {"email": TEST_EMAIL, "gender": UserGender.MALE.value, "id": self.user.id},
        )

        resp = await client.get(
            self.url, headers={"Authorization": self.user_session_token}
        )
        assert_user_detail_response(
            resp, TEST_USER_ID, TEST_USERNAME, TEST_EMAIL, UserGender.MALE.name, True
        )

    async def test_email_and_gender_not_returned_if_requested_by_other(
        self, client: AsyncClient
    ):
        await self.db.execute(
            "UPDATE users SET email_address = :email, gender = :gender WHERE id = :id",
            {
                "email": TEST_EMAIL,
                "gender": UserGender.FEMALE.value,
                "id": self.user.id,
            },
        )

        other_row = await return_canned_user(self.db, "user_2", 2222222)
        other = await create_canned_user(self.db, other_row)
        other_token = make_token_for_user(other.id)

        resp = await client.get(self.url, headers={"Authorization": other_token})
        assert_user_detail_response(
            resp, TEST_USER_ID, TEST_USERNAME, None, None, False
        )

@pytest.mark.anyio
class TestUsersDeleteUserAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, row)
        self.user_session_token = make_token_for_user(self.user.id)
        self.url = f"/api/v2/users/{self.user.id}/"

        admin_row = await return_canned_user(self.db, "admin_user", 222222)
        self.admin = await create_canned_user(self.db, admin_row)
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": UserRole.ADMIN.value, "id": self.admin.id},
        )
        self.admin_session_token = make_token_for_user(self.admin.id)

    async def test_returns_401_if_other_user_requested(self, client: AsyncClient):
        other_row = await return_canned_user(self.db, "user_2", 333333)
        other = await create_canned_user(self.db, other_row)

        resp = await client.delete(
            f"/api/v2/users/{other.id}/",
            headers={"Authorization": self.user_session_token},
        )
        assert resp.status_code == 401

    async def test_returns_200_if_user_deletes_himself(self, client: AsyncClient):
        temp_row = await return_canned_user(self.db, "self_delete_user", 444444)
        temp_user = await create_canned_user(self.db, temp_row)
        temp_token = make_token_for_user(temp_user.id)

        resp = await client.delete(
            f"/api/v2/users/{temp_user.id}/",
            headers={"Authorization": temp_token},
        )
        assert resp.status_code == 200

    async def test_returns_200_if_admin_deletes_user(self, client: AsyncClient):
        temp_row = await return_canned_user(self.db, "admin_deletes_user", 555555)
        temp_user = await create_canned_user(self.db, temp_row)

        resp = await client.delete(
            f"/api/v2/users/{temp_user.id}/",
            headers={"Authorization": self.admin_session_token},
        )
        assert resp.status_code == 200

    async def test_returns_500_if_user_not_found(self, client: AsyncClient):
        resp = await client.delete(
            "/api/v2/users/9999999/",
            headers={"Authorization": self.admin_session_token},
        )
        assert resp.status_code == 500


@pytest.mark.anyio
class TestUsersDeleteUsersAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, row)
        self.user_session_token = make_token_for_user(self.user.id)

        admin_row = await return_canned_user(self.db, "admin_user", 222222)
        self.admin = await create_canned_user(self.db, admin_row)
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": UserRole.ADMIN.value, "id": self.admin.id},
        )
        self.admin_session_token = make_token_for_user(self.admin.id)

    async def test_returns_401_if_not_admin(self, client: AsyncClient):
        other_row = await return_canned_user(self.db, "other_user", 333333)
        other = await create_canned_user(self.db, other_row)

        resp = await client.delete(
            f"/api/v2/users/{other.id}/",
            headers={"Authorization": self.user_session_token},
        )
        assert resp.status_code == 401

    async def test_returns_405_if_bulk_delete_not_implemented(self, client: AsyncClient):
        resp = await client.delete(
            "/api/v2/users/",
            headers={"Authorization": self.admin_session_token},
        )
        assert resp.status_code == 405


@pytest.mark.anyio
class TestGetUserFavoriteProjects:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, "fav_user", 88881)
        self.user = await create_canned_user(self.db, row)
        self.token = make_token_for_user(self.user.id)
        self.url = "/api/v2/users/queries/favorites/"

    async def test_returns_200_with_empty_favorites(self, client: AsyncClient):
        resp = await client.get(self.url, headers={"Authorization": self.token})
        assert resp.status_code == 200
        assert resp.json()["favoritedProjects"] == []

    async def test_returns_favorites_when_user_has_projects(self, client: AsyncClient):
        test_project, test_author, test_project_id = await create_canned_project(
            self.db
        )

        await self.db.execute(
            "INSERT INTO project_favorites (user_id, project_id) VALUES (:user_id, :project_id)",
            {"user_id": self.user.id, "project_id": test_project_id},
        )

        resp = await client.get(self.url, headers={"Authorization": self.token})
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["favoritedProjects"]) == 1
        assert body["favoritedProjects"][0]["projectId"] == test_project_id

    async def test_returns_403_without_token(self, client: AsyncClient):
        resp = await client.get(self.url)
        assert resp.status_code == 403


@pytest.mark.anyio
class TestGetUserInterests:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, "interests_user", 88882)
        self.user = await create_canned_user(self.db, row)
        self.token = make_token_for_user(self.user.id)
        self.url = f"/api/v2/users/{self.user.username}/queries/interests/"

    async def test_returns_200_with_no_interests(self, client: AsyncClient):
        resp = await client.get(self.url, headers={"Authorization": self.token})
        assert resp.status_code == 200
        assert resp.json()["interests"] == []

    async def test_returns_interests_when_user_has_interests(self, client: AsyncClient):
        i1 = await create_canned_interest(self.db, interest_id=111, name="test_integration_interest_1")
        i2 = await create_canned_interest(self.db, interest_id=112, name="test_integration_interest_2")

        await self.db.execute_many(
            """
            INSERT INTO user_interests (user_id, interest_id) VALUES (:user_id, :interest_id)
            """,
            [
                {"user_id": self.user.id, "interest_id": i1.id},
                {"user_id": self.user.id, "interest_id": i2.id},
            ],
        )

        resp = await client.get(self.url, headers={"Authorization": self.token})
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["interests"]) == 2
        assert body["interests"][0]["id"] == i1.id
        assert body["interests"][0]["name"] == i1.name
        assert body["interests"][1]["id"] == i2.id
        assert body["interests"][1]["name"] == i2.name

    async def test_returns_403_without_token(self, client: AsyncClient):
        resp = await client.get(self.url)
        assert resp.status_code == 403


@pytest.mark.anyio
class TestUsersFavoritesAndRecommendationsAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        user_row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, user_row)
        self.user_session_token = make_token_for_user(self.user.id)

    async def test_get_user_favorite_projects_success(self, client: AsyncClient):
        test_project, test_author, test_project_id = await create_canned_project(
            self.db
        )
        await self.db.execute(
            "INSERT INTO project_favorites (user_id, project_id) VALUES (:user_id, :project_id)",
            {"user_id": self.user.id, "project_id": test_project_id},
        )

        url = "/api/v2/users/queries/favorites/"
        resp = await client.get(url, headers={"Authorization": self.user_session_token})
        assert resp.status_code == 200
        assert "favoritedProjects" in resp.json()
        assert len(resp.json()["favoritedProjects"]) == 1

    async def test_get_recommended_projects_success(self, client: AsyncClient):
        await create_canned_project(self.db)
        await create_canned_project(self.db)

        url = f"/api/v2/users/{self.user.username}/recommended-projects/"
        resp = await client.get(url, headers={"Authorization": self.user_session_token})
        assert resp.status_code == 200
        body = resp.json()
        assert "results" in body


@pytest.mark.anyio
class TestGetAndZeroUserAPI:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        user_row = await return_canned_user(self.db, TEST_USERNAME, TEST_USER_ID)
        self.user = await create_canned_user(self.db, user_row)
        self.user_session_token = make_token_for_user(self.user.id)

        other_row = await return_canned_user(self.db, "other_user_test", 99999)
        self.other_user = await create_canned_user(self.db, other_row)
        self.other_token = make_token_for_user(self.other_user.id)

        admin_row = await return_canned_user(self.db, "admin_test_user", 88888)
        self.admin_user = await create_canned_user(self.db, admin_row)
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": UserRole.ADMIN.value, "id": self.admin_user.id},
        )
        self.admin_token = make_token_for_user(self.admin_user.id)

    async def test_get_user_by_id_success(self, client: AsyncClient):
        url = f"/api/v2/users/{self.user.id}/"
        resp = await client.get(url, headers={"Authorization": self.user_session_token})
        assert resp.status_code == 200
        assert resp.json()["id"] == self.user.id

    async def test_delete_user_unauthorized_if_not_self_or_admin(self, client: AsyncClient):
        url = f"/api/v2/users/{self.user.id}/"
        resp = await client.delete(url, headers={"Authorization": self.other_token})
        assert resp.status_code == 401
        assert resp.json()["SubCode"] == "UserPermissionError"

    async def test_delete_own_user_success(self, client: AsyncClient):
        temp_row = await return_canned_user(self.db, "self_delete_temp", 77777)
        temp_user = await create_canned_user(self.db, temp_row)
        temp_token = make_token_for_user(temp_user.id)

        url = f"/api/v2/users/{temp_user.id}/"
        resp = await client.delete(url, headers={"Authorization": temp_token})
        assert resp.status_code == 200

    async def test_delete_user_by_admin_success(self, client: AsyncClient):
        temp_row = await return_canned_user(self.db, "admin_deletes_temp", 66666)
        temp_user = await create_canned_user(self.db, temp_row)

        url = f"/api/v2/users/{temp_user.id}/"
        resp = await client.delete(url, headers={"Authorization": self.admin_token})
        assert resp.status_code == 200

    async def test_delete_user_not_found(self, client: AsyncClient):
        url = "/api/v2/users/99999999/"
        resp = await client.delete(url, headers={"Authorization": self.admin_token})
        assert resp.status_code == 500


@pytest.mark.anyio
class TestDeleteUserReturnsNone:
    @pytest.fixture(autouse=True)
    async def _setup(self, db_connection_fixture):
        self.db = db_connection_fixture
        row = await return_canned_user(self.db, "del_none_user", 55551)
        self.user = await create_canned_user(self.db, row)
        await self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": UserRole.ADMIN.value, "id": self.user.id},
        )
        self.token = make_token_for_user(self.user.id)

    async def test_delete_user_returns_400_when_service_returns_none(self, client: AsyncClient):
        with patch("backend.api.users.resources.UserService.delete_user_by_id", new_callable=AsyncMock, return_value=None):
            resp = await client.delete(
                f"/api/v2/users/{self.user.id}/",
                headers={"Authorization": self.token}
            )
            assert resp.status_code == 400
            assert resp.json()["SubCode"] == "UserNotFound"

