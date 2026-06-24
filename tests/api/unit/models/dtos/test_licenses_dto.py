import pytest

from backend.models.dtos.licenses_dto import LicenseDTO, LicenseListDTO


@pytest.mark.anyio
class TestLicensesDTOs:
    def test_license_dto(self):
        data = {
            "licenseId": 1,
            "name": "ODbL",
            "description": "Open Data Commons Open Database License",
            "plainText": "You are free to copy, distribute and use the database.",
        }
        dto = LicenseDTO(**data)
        assert dto.license_id == 1
        assert dto.name == "ODbL"
        assert dto.description == "Open Data Commons Open Database License"
        assert dto.plain_text == "You are free to copy, distribute and use the database."

    def test_license_list_dto(self):
        dto = LicenseListDTO()
        assert dto.licenses == []
        dto.licenses.append(LicenseDTO(name="ODbL"))
        assert len(dto.licenses) == 1
