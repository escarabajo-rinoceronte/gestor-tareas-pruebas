from backend.models.dtos.settings_dto import SettingsDTO, SupportedLanguage

def test_supported_language():
    data = {
        "code": "es",
        "language": "Spanish"
    }
    lang = SupportedLanguage(**data)
    assert lang.code == "es"
    assert lang.language == "Spanish"

def test_settings_dto():
    data = {
        "mapperLevelIntermediate": 250,
        "mapperLevelAdvanced": 500,
        "supportedLanguages": [
            {"code": "en", "language": "English"},
            {"code": "es", "language": "Spanish"}
        ]
    }
    dto = SettingsDTO(**data)
    assert dto.mapper_level_intermediate == 250
    assert dto.mapper_level_advanced == 500
    assert len(dto.supported_languages) == 2
    assert dto.supported_languages[0].code == "en"
