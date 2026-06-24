import pytest
from pydantic import ValidationError

from backend.models.dtos.partner_dto import PartnerDTO


@pytest.mark.anyio
class TestPartnerDTOs:
    def test_partner_dto_valid(self):
        data = {
            "name": "Partner A",
            "primary_hashtag": "partnera",
        }
        dto = PartnerDTO(**data)
        assert dto.name == "Partner A"
        assert dto.primary_hashtag == "partnera"

    def test_partner_dto_invalid(self):
        data = {
            "name": "Partner A",
            # missing primary_hashtag
        }
        with pytest.raises(ValidationError):
            PartnerDTO(**data)

    def test_from_record_with_website_links(self):
        # Arrange
        class DummyRecord:
            def __init__(self, d):
                self._d = d

            def __iter__(self):
                return iter(self._d.items())

            def keys(self):
                return self._d.keys()

            def __getitem__(self, item):
                return self._d[item]

        record = DummyRecord({
            "name": "Partner B",
            "primary_hashtag": "pb",
            "website_links": '[{"url": "http://test"}]'
        })

        # Act
        dto = PartnerDTO.from_record(record)

        # Assert
        assert dto.name == "Partner B"
        assert dto.website_links == [{"url": "http://test"}]

    def test_from_record_without_website_links(self):
        # Arrange
        class DummyRecord:
            def __init__(self, d):
                self._d = d

            def __iter__(self):
                return iter(self._d.items())

        record = DummyRecord({
            "name": "Partner C",
            "primary_hashtag": "pc",
        })

        # Act
        dto = PartnerDTO.from_record(record)

        # Assert
        assert dto.name == "Partner C"
        assert dto.website_links is None
