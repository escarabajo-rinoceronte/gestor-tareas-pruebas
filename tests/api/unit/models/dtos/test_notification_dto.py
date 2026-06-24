from datetime import datetime
from backend.models.dtos.notification_dto import NotificationDTO

def test_notification_dto():
    now = datetime.now()
    data = {
        "userId": 1,
        "date": now,
        "unreadCount": 5
    }
    dto = NotificationDTO(**data)
    assert dto.user_id == 1
    assert dto.date == now
    assert dto.unread_count == 5
