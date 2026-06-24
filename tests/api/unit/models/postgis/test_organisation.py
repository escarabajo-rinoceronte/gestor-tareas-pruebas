import pytest
from backend.models.dtos.organisation_dto import OrganisationDTO
from backend.models.postgis.organisation import OrganisationType
from tests.api.helpers.test_helpers import (
    create_canned_organisation,
    create_canned_user,
)


@pytest.mark.anyio
class TestOrganisation:
    @pytest.fixture(autouse=True)
    async def setup_test_data(self, db_connection_fixture, request):
        assert db_connection_fixture is not None, "Database connection is not available"

        request.cls.test_org = await create_canned_organisation(db_connection_fixture)
        request.cls.test_user = await create_canned_user(db_connection_fixture)

        assert self.test_org is not None, "Failed to create test organisation"
        assert self.test_user is not None, "Failed to create test user"

    async def test_get_organisations_managed_by_user(self, db_connection_fixture):
        """Test fetching organisations managed by a user."""
        # Assign the user as a manager
        await db_connection_fixture.execute(
            """
            INSERT INTO organisation_managers (organisation_id, user_id)
            VALUES (:organisation_id, :user_id)
            """,
            {"organisation_id": self.test_org.id, "user_id": self.test_user.id},
        )

        # Fetch organisations managed by the user
        organisations = await db_connection_fixture.fetch_all(
            """
            SELECT o.id, o.name FROM organisations o
            JOIN organisation_managers om ON o.id = om.organisation_id
            WHERE om.user_id = :user_id
            """,
            {"user_id": self.test_user.id},
        )

        assert len(organisations) == 1
        assert organisations[0].name == self.test_org.name

    async def test_as_dto(self, db_connection_fixture):
        """Test organisation DTO conversion with and without managers."""
        # Assign the user as a manager
        await db_connection_fixture.execute(
            """
            INSERT INTO organisation_managers (organisation_id, user_id)
            VALUES (:organisation_id, :user_id)
            """,
            {"organisation_id": self.test_org.id, "user_id": self.test_user.id},
        )

        # Fetch organisation details
        org_record = await db_connection_fixture.fetch_one(
            """
            SELECT id, name, slug, logo, description, url, type, subscription_tier
            FROM organisations WHERE id = :id
            """,
            {"id": self.test_org.id},
        )

        # Fetch managers
        managers = await db_connection_fixture.fetch_all(
            """
            SELECT u.id, u.username FROM users u
            JOIN organisation_managers om ON u.id = om.user_id
            WHERE om.organisation_id = :id
            """,
            {"id": self.test_org.id},
        )

        # Convert to DTO
        org_dto = OrganisationDTO(
            organisation_id=org_record["id"],
            name=org_record["name"],
            slug=org_record["slug"],
            logo=org_record["logo"],
            description=org_record["description"],
            url=org_record["url"],
            type=OrganisationType(org_record["type"]).name,
            subscription_tier=org_record["subscription_tier"],
            managers=[{"id": m["id"], "username": m["username"]} for m in managers],
        )

        # Assertions
        assert org_dto.organisation_id == self.test_org.id
        assert org_dto.name == self.test_org.name
        assert org_dto.slug == self.test_org.slug
        assert len(org_dto.managers) == 1
        assert org_dto.managers[0].username == self.test_user.username

        # Test omitting managers
        org_dto.managers = []
        assert len(org_dto.managers) == 0


    async def test_get_organisation_by_id_direct(self, db_connection_fixture):
        """Verifica la obtención de una organización existente mediante una consulta directa."""
        org = await db_connection_fixture.fetch_one(
            "SELECT id, name FROM organisations WHERE id = :id",
            {"id": self.test_org.id},
        )
        assert org is not None
        assert org["id"] == self.test_org.id
        assert org["name"] == self.test_org.name

    async def test_get_organisation_by_slug(self, db_connection_fixture):
        """Prueba la búsqueda exacta de una organización filtrando por su campo slug."""
        org = await db_connection_fixture.fetch_one(
            "SELECT id, slug FROM organisations WHERE slug = :slug",
            {"slug": self.test_org.slug},
        )
        assert org is not None
        assert org["id"] == self.test_org.id

    async def test_get_organisation_by_invalid_id(self, db_connection_fixture):
        """Garantiza que la búsqueda con un ID inexistente devuelva un resultado vacío (None)."""
        org = await db_connection_fixture.fetch_one(
            "SELECT * FROM organisations WHERE id = :id",
            {"id": 999999},
        )
        assert org is None

    async def test_update_organisation_name(self, db_connection_fixture):
        """Valida la actualización del nombre de una organización en la base de datos."""
        new_name = "Organizacion Corregida S.A."
        await db_connection_fixture.execute(
            "UPDATE organisations SET name = :name WHERE id = :id",
            {"name": new_name, "id": self.test_org.id},
        )
        org = await db_connection_fixture.fetch_one(
            "SELECT name FROM organisations WHERE id = :id",
            {"id": self.test_org.id},
        )
        assert org["name"] == new_name

    async def test_update_organisation_url(self, db_connection_fixture):
        """Valida que se pueda modificar correctamente la URL del sitio web de la organización."""
        new_url = "https://example-updated.org"
        await db_connection_fixture.execute(
            "UPDATE organisations SET url = :url WHERE id = :id",
            {"url": new_url, "id": self.test_org.id},
        )
        org = await db_connection_fixture.fetch_one(
            "SELECT url FROM organisations WHERE id = :id",
            {"id": self.test_org.id},
        )
        assert org["url"] == new_url

    async def test_organisation_dto_instantiation_minimal(self, db_connection_fixture):
        """Comprueba que el DTO se instancie de forma correcta con una lista vacía de managers."""
        dto = OrganisationDTO(
            organisation_id=self.test_org.id,
            name=self.test_org.name,
            slug=self.test_org.slug,
            logo=None,
            description=None,
            url=None,
            type=OrganisationType(self.test_org.type).name,
            subscription_tier=1,
            managers=[],
        )
        assert dto.organisation_id == self.test_org.id
        assert len(dto.managers) == 0

    async def test_remove_organisation_manager(self, db_connection_fixture):
        """Prueba la eliminación física de un registro de relación en la tabla organisation_managers."""
        await db_connection_fixture.execute(
            """
            INSERT INTO organisation_managers (organisation_id, user_id)
            VALUES (:organisation_id, :user_id) ON CONFLICT DO NOTHING
            """,
            {"organisation_id": self.test_org.id, "user_id": self.test_user.id},
        )
        await db_connection_fixture.execute(
            "DELETE FROM organisation_managers WHERE organisation_id = :org_id AND user_id = :user_id",
            {"org_id": self.test_org.id, "user_id": self.test_user.id},
        )
        managers = await db_connection_fixture.fetch_all(
            "SELECT * FROM organisation_managers WHERE organisation_id = :org_id",
            {"org_id": self.test_org.id},
        )
        assert len(managers) == 0

    async def test_organisation_managers_empty_by_default(self, db_connection_fixture):
        """Asegura que una organización recién creada no posea mánagers por defecto asociados con el ID del usuario de prueba."""
        managers = await db_connection_fixture.fetch_all(
            "SELECT * FROM organisation_managers WHERE organisation_id = :org_id AND user_id = :user_id",
            {"org_id": self.test_org.id, "user_id": self.test_user.id},
        )
        assert len(managers) == 0

    async def test_count_total_organisations(self, db_connection_fixture):
        """Valida que el conteo total de la tabla organisations sea mayor o igual a 1."""
        count = await db_connection_fixture.fetch_one("SELECT COUNT(*) as total FROM organisations")
        assert count["total"] >= 1

    async def test_organisation_type_mapping_is_valid(self, db_connection_fixture):
        """Comprueba que el valor entero de la base de datos mapee hacia un enum de OrganisationType válido."""
        org_record = await db_connection_fixture.fetch_one(
            "SELECT type FROM organisations WHERE id = :id",
            {"id": self.test_org.id},
        )
        enum_type = OrganisationType(org_record["type"])
        assert enum_type in OrganisationType

    async def test_organisation_subscription_tier_default(self, db_connection_fixture):
        """Verifica que el nivel de suscripción obtenido corresponda al asignado originalmente en la base de datos."""
        org_record = await db_connection_fixture.fetch_one(
            "SELECT subscription_tier FROM organisations WHERE id = :id",
            {"id": self.test_org.id},
        )
        assert org_record["subscription_tier"] == self.test_org.subscription_tier

    async def test_organisation_slug_is_not_null(self, db_connection_fixture):
        """Comprueba que el registro de la organización tenga un slug definido."""
        org_record = await db_connection_fixture.fetch_one(
            "SELECT slug FROM organisations WHERE id = :id",
            {"id": self.test_org.id},
        )
        assert org_record["slug"] is not None

    async def test_organisation_managers_join_returns_empty_for_invalid_user(self, db_connection_fixture):
        """Valida que la consulta join entre organizaciones y mánagers devuelva una lista vacía para un ID de usuario incorrecto."""
        organisations = await db_connection_fixture.fetch_all(
            """
            SELECT o.id FROM organisations o
            JOIN organisation_managers om ON o.id = om.organisation_id
            WHERE om.user_id = :user_id
            """,
            {"user_id": 999999},
        )
        assert len(organisations) == 0

    async def test_update_organisation_slug(self, db_connection_fixture):
        """Prueba la edición controlada del campo slug de una organización existente."""
        new_slug = "nuevo-slug-test-123"
        await db_connection_fixture.execute(
            "UPDATE organisations SET slug = :slug WHERE id = :id",
            {"slug": new_slug, "id": self.test_org.id},
        )
        org = await db_connection_fixture.fetch_one(
            "SELECT slug FROM organisations WHERE id = :id",
            {"id": self.test_org.id},
        )
        assert org["slug"] == new_slug

    async def test_update_organisation_description(self, db_connection_fixture):
        """Prueba la modificación y lectura exitosa del campo de descripción."""
        new_desc = "Esta es una descripcion de prueba actualizada."
        await db_connection_fixture.execute(
            "UPDATE organisations SET description = :desc WHERE id = :id",
            {"desc": new_desc, "id": self.test_org.id},
        )
        org = await db_connection_fixture.fetch_one(
            "SELECT description FROM organisations WHERE id = :id",
            {"id": self.test_org.id},
        )
        assert org["description"] == new_desc

    async def test_organisation_managers_multiple_inserts_handled(self, db_connection_fixture):
        """Verifica que la tabla puente soporte registros únicos de mánagers sin generar colisiones."""
        await db_connection_fixture.execute(
            """
            INSERT INTO organisation_managers (organisation_id, user_id)
            VALUES (:organisation_id, :user_id) ON CONFLICT DO NOTHING
            """,
            {"organisation_id": self.test_org.id, "user_id": self.test_user.id},
        )
        managers = await db_connection_fixture.fetch_all(
            "SELECT user_id FROM organisation_managers WHERE organisation_id = :org_id",
            {"org_id": self.test_org.id},
        )
        assert len(managers) >= 1

    async def test_organisation_dto_mutation_safe(self, db_connection_fixture):
        """Valida que los campos de una instancia DTO de organización se dejen mutar de forma segura en memoria."""
        dto = OrganisationDTO(
            organisation_id=self.test_org.id,
            name=self.test_org.name,
            slug=self.test_org.slug,
            logo=None,
            description=None,
            url=None,
            type=OrganisationType(self.test_org.type).name,
            subscription_tier=2,
            managers=[],
        )
        dto.name = "Mutated Name"
        assert dto.name == "Mutated Name"

    async def test_get_organisation_type_as_integer(self, db_connection_fixture):
        """Asegura que el tipo de organización persistido en SQL se devuelva como un valor de tipo entero."""
        org_record = await db_connection_fixture.fetch_one(
            "SELECT type FROM organisations WHERE id = :id",
            {"id": self.test_org.id},
        )
        assert isinstance(org_record["type"], int)

    async def test_organisation_record_has_id(self, db_connection_fixture):
        """Valida de manera explícita que la organización cargada en base de datos posea una clave primaria válida."""
        org_record = await db_connection_fixture.fetch_one(
            "SELECT id FROM organisations WHERE id = :id",
            {"id": self.test_org.id},
        )
        assert org_record["id"] == self.test_org.id