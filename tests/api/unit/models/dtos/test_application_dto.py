from datetime import datetime
from backend.models.dtos.application_dto import ApplicationDTO, ApplicationsDTO

def test_application_dto():
    now = datetime.now()
    data = {
        "keyId": 1,
        "userId": 2,
        "applicationkey": "secret-key",
        "createdDate": now
    }
    dto = ApplicationDTO(**data)
    assert dto.id == 1
    assert dto.user == 2
    assert dto.app_key == "secret-key"
    assert dto.created == now

def test_applications_dto():
    now = datetime.now()
    data = {
        "applications": [
            {
                "keyId": 1,
                "userId": 2,
                "applicationkey": "secret-key",
                "createdDate": now
            }
        ]
    }
    dto = ApplicationsDTO(**data)
    assert len(dto.applications) == 1
    assert dto.applications[0].id == 1
    assert dto.applications[0].app_key == "secret-key"

def test_applications_dto_empty():
    dto = ApplicationsDTO()
    assert dto.applications == []
