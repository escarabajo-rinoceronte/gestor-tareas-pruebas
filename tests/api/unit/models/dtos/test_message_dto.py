import pytest
from datetime import datetime
from pydantic import ValidationError

from backend.models.dtos.message_dto import (
    ChatMessageDTO,
    ListChatMessageDTO,
    MessageDTO,
    MessagesDTO,
    ProjectChatDTO,
)
from backend.models.dtos.stats_dto import Pagination


@pytest.mark.anyio
class TestMessageDTOs:
    def test_message_dto_valid(self):
        data = {
            "messageId": 1,
            "subject": "Test Subject",
            "message": "Test Message",
            "fromUserId": 2,
            "fromUsername": "user2",
            "displayPictureUrl": "http://img",
            "projectId": 3,
            "projectTitle": "Proj",
            "taskId": 4,
            "messageType": "type1",
            "sentDate": "2023-01-01T00:00:00",
            "read": False,
        }
        dto = MessageDTO(**data)
        assert dto.message_id == 1
        assert dto.subject == "Test Subject"
        assert dto.message == "Test Message"
        assert dto.sent_date.year == 2023
        assert dto.read is False

    def test_message_dto_invalid_subject(self):
        data = {
            "subject": "",
            "message": "Test Message",
        }
        with pytest.raises(ValidationError):
            MessageDTO(**data)

    def test_messages_dto(self):
        dto = MessagesDTO()
        assert dto.user_messages == []
        # Añadimos el campo obligatorio 'fromUserId'
        dto.user_messages.append(MessageDTO(subject="A", message="B", fromUserId=1))
        assert len(dto.user_messages) == 1

        pag = Pagination(
            hasNext=False,
            hasPrev=False,
            nextNum=None,
            page=1,
            pages=1,
            prevNum=None,
            perPage=10,
            total=1,
        )
        dto.pagination = pag
        assert dto.pagination.total == 1

    def test_chat_message_dto(self):
        dt = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            "id": 1,
            "message": "Chat msg",
            "user_id": 2,
            "project_id": 3,
            "picture_url": "http://pic",
            "timestamp": dt,
            "username": "user",
        }
        dto = ChatMessageDTO(**data)
        assert dto.id == 1
        assert dto.message == "Chat msg"
        assert dto.user_id == 2
        assert dto.project_id == 3
        assert dto.timestamp == dt

    def test_list_chat_message_dto(self):
        dt = datetime(2023, 1, 1, 12, 0, 0)
        data = {
            "id": 1,
            "message": "Chat list msg",
            "picture_url": "http://pic",
            "timestamp": dt,
            "username": "user",
        }
        dto = ListChatMessageDTO(**data)
        assert dto.message == "Chat list msg"

    def test_project_chat_dto(self):
        dto = ProjectChatDTO()
        assert dto.chat == []
        dto.chat.append(
            ListChatMessageDTO(
                message="msg",
                timestamp=datetime(2023, 1, 1, 12, 0, 0),
                username="u",
            )
        )
        assert len(dto.chat) == 1
