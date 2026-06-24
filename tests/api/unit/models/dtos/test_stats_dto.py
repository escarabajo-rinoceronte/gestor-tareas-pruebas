import pytest

from backend.models.dtos.stats_dto import (
    CampaignStatsDTO,
    GenderStatsDTO,
    HomePageStatsDTO,
    LevelStats,
    OrganizationListStatsDTO,
    OrganizationProjectsStatsDTO,
    OrganizationStatsDTO,
    OrganizationTasksStatsDTO,
    Pagination,
    ProjectActivityDTO,
    ProjectContributionsDTO,
    ProjectLastActivityDTO,
    TaskStats,
    TaskStatsDTO,
    UserContribution,
    UserStatsDTO,
)


@pytest.mark.anyio
class TestStatsDTOs:
    def test_user_contribution(self):
        data = {
            "username": "user1",
            "mapping_level": "ADVANCED",
            "picture_url": "http://pic",
            "mapped": 10,
            "validated": 5,
            "bad_imagery": 1,
            "total": 16,
            "mapped_tasks": [1, 2],
            "validated_tasks": [3],
            "bad_imagery_tasks": [4],
            "name": "User One",
            "date_registered": "2023-01-01",
        }
        dto = UserContribution(data)
        assert dto.username == "user1"
        assert dto.mapping_level == "ADVANCED"
        assert dto.mapped_tasks == [1, 2]

    def test_project_contributions_dto(self):
        dto = ProjectContributionsDTO()
        assert dto.user_contributions == []

    def test_pagination_from_total_count(self):
        pag = Pagination.from_total_count(page=2, per_page=10, total=25)
        assert pag.page == 2
        assert pag.pages == 3
        assert pag.has_next is True
        assert pag.has_prev is True
        assert pag.next_num == 3
        assert pag.prev_num == 1
        assert pag.per_page == 10
        assert pag.total == 25

    def test_project_activity_dto(self):
        dto = ProjectActivityDTO()
        assert dto.pagination is None
        assert dto.activity is None

    def test_project_last_activity_dto(self):
        dto = ProjectLastActivityDTO()
        assert dto.activity == []

    def test_organization_projects_stats_dto(self):
        dto = OrganizationProjectsStatsDTO(draft=1, published=2)
        assert dto.draft == 1
        assert dto.published == 2

    def test_organization_tasks_stats_dto(self):
        dto = OrganizationTasksStatsDTO(ready=10, mapped=5)
        assert dto.ready == 10
        assert dto.mapped == 5
        assert dto.locked_for_mapping == 0

    def test_organization_stats_dto(self):
        dto = OrganizationStatsDTO()
        assert dto.projects is None
        assert dto.active_tasks is None

    def test_organization_list_stats_dto(self):
        row = ("Org1", 5)
        dto = OrganizationListStatsDTO(row)
        assert dto.organisation == "Org1"
        assert dto.projects_created == 5

    def test_campaign_stats_dto(self):
        row = ("Camp1", 10)
        dto = CampaignStatsDTO(row)
        assert dto.campaign == "Camp1"
        assert dto.projects_created == 10

    def test_home_page_stats_dto(self):
        dto = HomePageStatsDTO()
        assert dto.organisations == []
        assert dto.campaigns == []

    def test_task_stats(self):
        data = {"date": "2023-01-01", "mapped": 10, "validated": 5, "badImagery": 2}
        dto = TaskStats(**data)
        assert dto.date == "2023-01-01"
        assert dto.mapped == 10
        assert dto.bad_imagery == 2

    def test_task_stats_dto(self):
        data = {"taskStats": []}
        dto = TaskStatsDTO(**data)
        assert dto.stats == []

    def test_gender_stats_dto(self):
        data = {"male": 10, "female": 10, "preferNotIdentify": 5, "selfDescribe": 1}
        dto = GenderStatsDTO(**data)
        assert dto.male == 10

    def test_level_stats(self):
        data = {"name": "ADVANCED", "count": 10}
        dto = LevelStats(**data)
        assert dto.name == "ADVANCED"

    def test_user_stats_dto(self):
        data = {
            "total": 100,
            "contributed": 50,
            "emailVerified": 90,
            "genders": {"male": 10, "female": 10, "preferNotIdentify": 5, "selfDescribe": 1},
        }
        dto = UserStatsDTO(**data)
        assert dto.total == 100
        assert dto.genders.male == 10
