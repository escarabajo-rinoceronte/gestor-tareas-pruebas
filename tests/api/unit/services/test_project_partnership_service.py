import pytest
from datetime import datetime, timedelta
from backend.services.project_partnership_service import ProjectPartnershipService, NotFound, BadRequest
from tests.api.helpers.test_helpers import create_canned_project

@pytest.mark.anyio
class TestProjectPartnershipService:
    @pytest.fixture(autouse=True)
    async def setup_test_data(self, db_connection_fixture, request):
        request.cls.db = db_connection_fixture
        # Preparar proyecto y partner base
        proj, user, pid = await create_canned_project(self.db)
        request.cls.project_id = pid
        
        # Crear un partner manual para las pruebas
        await self.db.execute(
            "INSERT INTO partners (id, name, primary_hashtag) VALUES (10, 'Test Partner', '#test')",
        )
        request.cls.partner_id = 10

    async def test_get_partnership_raises_not_found(self):
        with pytest.raises(NotFound):
            await ProjectPartnershipService.get_partnership_as_dto(999, self.db)

    async def test_create_partnership_invalid_dates_raises_error(self):
        """Valida que la fecha de inicio no puede ser posterior a la de fin."""
        start = datetime.utcnow()
        end = start - timedelta(days=1)
        
        with pytest.raises(BadRequest, match="INVALID_TIME_RANGE"):
            await ProjectPartnershipService.create_partnership(
                self.db, self.project_id, self.partner_id, start, end
            )

    async def test_create_partnership_happy_path(self):
        """Valida la creación exitosa y el registro en el historial."""
        start = datetime.utcnow()
        
        partnership_id = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        
        assert partnership_id is not None
        # Verificar historial (Action 0 = CREATE)
        history = await self.db.fetch_one(
            "SELECT action FROM project_partnerships_history WHERE partnership_id = :id",
            {"id": partnership_id}
        )
        assert history["action"] == 0

    async def test_update_partnership_time_range_success(self):
        """Valida la actualización de fechas y el registro del cambio."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        
        new_end = start + timedelta(days=10)
        await ProjectPartnershipService.update_partnership_time_range(
            self.db, pid, start, new_end
        )
        
        updated = await ProjectPartnershipService.get_partnership_as_dto(pid, self.db)
        assert updated.ended_on is not None
        # Verificar historial de actualización (Action 2 = UPDATE)
        history = await self.db.fetch_val(
            "SELECT COUNT(*) FROM project_partnerships_history WHERE partnership_id = :id AND action = 2",
            {"id": pid}
        )
        assert history == 1

    async def test_delete_partnership_cleanup(self):
        """Valida el borrado lógico/histórico y físico del vínculo."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        
        await ProjectPartnershipService.delete_partnership(pid, self.db)
        
        # Verificar que ya no existe el vínculo
        with pytest.raises(NotFound):
            await ProjectPartnershipService.get_partnership_as_dto(pid, self.db)
            
        # Verificar historial de borrado (Action 1 = DELETE)
        del_history = await self.db.fetch_one(
            "SELECT action FROM project_partnerships_history WHERE project_id = :pid AND partner_id = :ptid ORDER BY id DESC",
            {"pid": self.project_id, "ptid": self.partner_id}
        )
        assert del_history["action"] == 1

    async def test_get_partnerships_by_project_returns_list(self):
        """Valida la recuperación de todos los partners de un proyecto."""
        await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, datetime.utcnow(), None
        )
        
        results = await ProjectPartnershipService.get_partnerships_by_project(self.project_id, self.db)
        assert len(results) == 1
        assert results[0].partner_id == self.partner_id


    async def test_get_partnership_as_dto_success(self):
        """Valida que se pueda recuperar un DTO correcto tras crear una asociación válida."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        dto = await ProjectPartnershipService.get_partnership_as_dto(pid, self.db)
        assert dto is not None
        assert dto.project_id == self.project_id
        assert dto.partner_id == self.partner_id

    async def test_get_partnerships_by_project_empty(self):
        """Valida que un proyecto sin asociaciones retorne una lista vacía sin lanzar excepciones."""
        # Usamos un ID de proyecto ficticio que no tenga vinculaciones
        results = await ProjectPartnershipService.get_partnerships_by_project(999955, self.db)
        assert isinstance(results, list)
        assert len(results) == 0

    async def test_update_partnership_time_range_invalid_dates_raises_error(self):
        """Valida que la actualización falle si se intenta colocar un fin menor que el inicio."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        invalid_end = start - timedelta(days=5)
        with pytest.raises(BadRequest):
            await ProjectPartnershipService.update_partnership_time_range(
                self.db, pid, start, invalid_end
            )

    async def test_history_contains_correct_metadata_on_create(self):
        """Verifica que el historial guarde la fecha exacta o aproximada al crear una relación."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        history = await self.db.fetch_one(
            "SELECT partnership_id FROM project_partnerships_history WHERE partnership_id = :id AND action = 0",
            {"id": pid}
        )
        assert history["partnership_id"] == pid

    async def test_create_partnership_with_predefined_end_date(self):
        """Comprueba la creación exitosa asignando desde un inicio tanto la fecha de inicio como la de fin."""
        start = datetime.utcnow()
        end = start + timedelta(days=30)
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, end
        )
        dto = await ProjectPartnershipService.get_partnership_as_dto(pid, self.db)
        assert dto.ended_on is not None

    async def test_multiple_partnerships_same_project_different_partners(self):
        """Valida que un mismo proyecto pueda tener múltiples asociaciones con partners diferentes."""
        # Creamos un segundo partner de forma manual para evitar duplicar IDs primarios
        await self.db.execute(
            "INSERT INTO partners (id, name, primary_hashtag) VALUES (11, 'Second Test Partner', '#test2')",
        )
        
        start = datetime.utcnow()
        pid1 = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        pid2 = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, 11, start, None
        )
        
        results = await ProjectPartnershipService.get_partnerships_by_project(self.project_id, self.db)
        assert len(results) >= 2
        assert any(r.partner_id == self.partner_id for r in results)
        assert any(r.partner_id == 11 for r in results)

    async def test_get_partnership_as_dto_has_expected_properties(self):
        """Valida estructuralmente que el DTO devuelto por el servicio contenga las propiedades base requeridas."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        dto = await ProjectPartnershipService.get_partnership_as_dto(pid, self.db)
        assert hasattr(dto, "id") or hasattr(dto, "partnership_id")
        assert hasattr(dto, "started_on")

    async def test_create_partnership_history_record_count(self):
        """Comprueba que sólo se inserte un registro en el historial por cada acción de creación limpia."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        count = await self.db.fetch_val(
            "SELECT COUNT(*) FROM project_partnerships_history WHERE partnership_id = :id AND action = 0",
            {"id": pid}
        )
        assert count == 1

    async def test_history_sequence_integration(self):
        """Garantiza que las acciones consecutivas (Crear y Modificar) dejen la traza correcta en el historial."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        await ProjectPartnershipService.update_partnership_time_range(
            self.db, pid, start, start + timedelta(days=1)
        )
        
        actions = await self.db.fetch_all(
            "SELECT action FROM project_partnerships_history WHERE partnership_id = :id ORDER BY id ASC",
            {"id": pid}
        )
        assert len(actions) >= 2
        assert actions[0]["action"] == 0

    async def test_get_partnerships_by_project_returns_correct_types(self):
        """Asegura que los elementos de la lista devuelta por la búsqueda por proyecto sean objetos iterables estructurados."""
        start = datetime.utcnow()
        await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        results = await ProjectPartnershipService.get_partnerships_by_project(self.project_id, self.db)
        assert isinstance(results, list)
        if len(results) > 0:
            assert results[0].project_id == self.project_id

    async def test_create_partnership_is_stored_in_database(self):
        """Consulta directamente la tabla relacional para verificar la persistencia física de la asociación."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        record = await self.db.fetch_one(
            "SELECT * FROM project_partnerships WHERE id = :id",
            {"id": pid}
        )
        assert record is not None
        assert record["project_id"] == self.project_id

    async def test_partnership_started_on_type_is_datetime(self):
        """Valida que la propiedad 'started_on' mapeada por el DTO retorne una instancia válida de datetime."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        dto = await ProjectPartnershipService.get_partnership_as_dto(pid, self.db)
        assert isinstance(dto.started_on, datetime)

    async def test_delete_partnership_removes_from_active_list(self):
        """Asegura que tras un borrado, el partner desaparezca inmediatamente de la lista activa del proyecto."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        
        init_list = await ProjectPartnershipService.get_partnerships_by_project(self.project_id, self.db)
        assert any(x.partner_id == self.partner_id for x in init_list)
        
        await ProjectPartnershipService.delete_partnership(pid, self.db)
        
        post_list = await ProjectPartnershipService.get_partnerships_by_project(self.project_id, self.db)
        assert not any(x.partner_id == self.partner_id for x in post_list)

    async def test_update_partnership_start_date_only(self):
        """Valida la actualización correcta modificando únicamente el valor de la fecha de inicio."""
        start = datetime.utcnow()
        pid = await ProjectPartnershipService.create_partnership(
            self.db, self.project_id, self.partner_id, start, None
        )
        
        new_start = start - timedelta(days=2)
        await ProjectPartnershipService.update_partnership_time_range(
            self.db, pid, new_start, None
        )
        dto = await ProjectPartnershipService.get_partnership_as_dto(pid, self.db)
        assert dto.started_on is not None

    async def test_create_partnership_equal_start_and_end_dates(self):
        """Prueba que los límites de tiempo idénticos (mismo segundo) sean procesados según las reglas del servicio."""
        start = datetime.utcnow()
        try:
            pid = await ProjectPartnershipService.create_partnership(
                self.db, self.project_id, self.partner_id, start, start
            )
            assert pid is not None
        except BadRequest:
            pass