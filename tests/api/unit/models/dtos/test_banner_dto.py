from backend.models.dtos.banner_dto import BannerDTO

def test_banner_dto():
    data = {
        "message": "Test banner message",
        "visible": False
    }
    dto = BannerDTO(**data)
    assert dto.message == "Test banner message"
    assert dto.visible is False

def test_banner_dto_default_visible():
    data = {
        "message": "Another message"
    }
    dto = BannerDTO(**data)
    assert dto.message == "Another message"
    assert dto.visible is True
