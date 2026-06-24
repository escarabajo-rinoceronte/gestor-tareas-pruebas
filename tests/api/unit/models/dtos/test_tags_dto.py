from backend.models.dtos.tags_dto import TagsDTO

def test_tags_dto_empty():
    dto = TagsDTO()
    assert dto.tags is None

def test_tags_dto_with_tags():
    data = {
        "tags": ["tag1", "tag2"]
    }
    dto = TagsDTO(**data)
    assert dto.tags == ["tag1", "tag2"]
