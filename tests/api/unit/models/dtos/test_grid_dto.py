from backend.models.dtos.grid_dto import GridDTO, SplitTaskDTO

def test_grid_dto():
    data = {
        "areaOfInterest": {"type": "Polygon", "coordinates": []},
        "grid": {"type": "FeatureCollection", "features": []},
        "clipToAoi": True
    }
    dto = GridDTO(**data)
    assert dto.area_of_interest == {"type": "Polygon", "coordinates": []}
    assert dto.grid == {"type": "FeatureCollection", "features": []}
    assert dto.clip_to_aoi is True

def test_split_task_dto():
    data = {
        "userId": 1,
        "taskId": 10,
        "projectId": 100,
        "preferred_locale": "es"
    }
    dto = SplitTaskDTO(**data)
    assert dto.user_id == 1
    assert dto.task_id == 10
    assert dto.project_id == 100
    assert dto.preferred_locale == "es"

def test_split_task_dto_default_locale():
    data = {
        "userId": 1,
        "taskId": 10,
        "projectId": 100
    }
    dto = SplitTaskDTO(**data)
    assert dto.preferred_locale == "en"
