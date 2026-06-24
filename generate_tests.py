import os

base_dir = r"e:\Ing. Sistemas\4to_año\PS\Proyecto_Final\gestor-tareas-pruebas\tests\api\unit\models\dtos"

def generate_banner():
    path = os.path.join(base_dir, "test_banner_dto.py")
    content = "from backend.models.dtos.banner_dto import BannerDTO\n\n"
    for i in range(1, 31):
        content += f"""def test_banner_dto_case_{i}():
    data = {{"message": "Test message {i}", "visible": {i % 2 == 0}}}
    dto = BannerDTO(**data)
    assert dto.message == "Test message {i}"
    assert dto.visible is {i % 2 == 0}

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_tags():
    path = os.path.join(base_dir, "test_tags_dto.py")
    content = "from backend.models.dtos.tags_dto import TagsDTO\n\n"
    for i in range(1, 31):
        content += f"""def test_tags_dto_case_{i}():
    data = {{"tags": ["tag{i}", "tag{i+1}"]}}
    dto = TagsDTO(**data)
    assert dto.tags == ["tag{i}", "tag{i+1}"]

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_notification():
    path = os.path.join(base_dir, "test_notification_dto.py")
    content = "from datetime import datetime\nfrom backend.models.dtos.notification_dto import NotificationDTO\n\n"
    for i in range(1, 31):
        content += f"""def test_notification_dto_case_{i}():
    date_val = datetime(202{i%10}, {(i%12)+1}, {(i%28)+1})
    data = {{"userId": {i}, "date": date_val, "unreadCount": {i * 2}}}
    dto = NotificationDTO(**data)
    assert dto.user_id == {i}
    assert dto.date == date_val
    assert dto.unread_count == {i * 2}

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_settings():
    path = os.path.join(base_dir, "test_settings_dto.py")
    content = "from backend.models.dtos.settings_dto import SettingsDTO, SupportedLanguage\n\n"
    for i in range(1, 31):
        content += f"""def test_settings_dto_case_{i}():
    data = {{
        "mapperLevelIntermediate": {i * 10},
        "mapperLevelAdvanced": {i * 20},
        "supportedLanguages": [{{"code": "en{i}", "language": "English{i}"}}]
    }}
    dto = SettingsDTO(**data)
    assert dto.mapper_level_intermediate == {i * 10}
    assert dto.mapper_level_advanced == {i * 20}
    assert dto.supported_languages[0].code == "en{i}"

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_task_annotation():
    path = os.path.join(base_dir, "test_task_annotation_dto.py")
    content = "from backend.models.dtos.task_annotation_dto import TaskAnnotationDTO\n\n"
    for i in range(1, 31):
        content += f"""def test_task_annotation_dto_case_{i}():
    data = {{
        "taskId": {i},
        "annotationType": "type_{i}",
        "annotationSource": "source_{i}",
        "annotationMarkdown": "markdown_{i}",
        "properties": {{"key": {i}}}
    }}
    dto = TaskAnnotationDTO(**data)
    assert dto.task_id == {i}
    assert dto.annotation_type == "type_{i}"
    assert dto.annotation_source == "source_{i}"
    assert dto.annotation_markdown == "markdown_{i}"
    assert dto.properties == {{"key": {i}}}

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_grid():
    path = os.path.join(base_dir, "test_grid_dto.py")
    content = "from backend.models.dtos.grid_dto import GridDTO, SplitTaskDTO\n\n"
    for i in range(1, 16):
        content += f"""def test_grid_dto_case_{i}():
    data = {{
        "areaOfInterest": {{"type": "Polygon", "coordinates": [[[{i}, {i}]]]}},
        "grid": {{"type": "FeatureCollection", "features": []}},
        "clipToAoi": {i % 2 == 0}
    }}
    dto = GridDTO(**data)
    assert dto.clip_to_aoi is {i % 2 == 0}

def test_split_task_dto_case_{i}():
    data = {{
        "userId": {i},
        "taskId": {i*10},
        "projectId": {i*100},
        "preferred_locale": "locale_{i}"
    }}
    dto = SplitTaskDTO(**data)
    assert dto.user_id == {i}
    assert dto.task_id == {i*10}

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_application():
    path = os.path.join(base_dir, "test_application_dto.py")
    content = "from datetime import datetime\nfrom backend.models.dtos.application_dto import ApplicationDTO, ApplicationsDTO\n\n"
    for i in range(1, 31):
        content += f"""def test_application_dto_case_{i}():
    date_val = datetime(202{i%10}, {(i%12)+1}, {(i%28)+1})
    data = {{"keyId": {i}, "userId": {i+1}, "applicationkey": "key_{i}", "createdDate": date_val}}
    dto = ApplicationDTO(**data)
    assert dto.id == {i}
    assert dto.app_key == "key_{i}"

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

generate_banner()
generate_tags()
generate_notification()
generate_settings()
generate_task_annotation()
generate_grid()
generate_application()
print("Tests generated!")
