from backend.models.dtos.task_annotation_dto import TaskAnnotationDTO

def test_task_annotation_dto():
    data = {
        "taskId": 100,
        "annotationType": "validation",
        "annotationSource": "user",
        "annotationMarkdown": "Looks good",
        "properties": {"key": "value"}
    }
    dto = TaskAnnotationDTO(**data)
    assert dto.task_id == 100
    assert dto.annotation_type == "validation"
    assert dto.annotation_source == "user"
    assert dto.annotation_markdown == "Looks good"
    assert dto.properties == {"key": "value"}

def test_task_annotation_dto_defaults():
    dto = TaskAnnotationDTO()
    assert dto.task_id is None
    assert dto.annotation_type is None
