from fastapi import APIRouter, WebSocket

router = APIRouter()
clients_by_session = {}


def create_learned_words_payload(session_id: str, learned_words: list[dict], message_type: str):
    return {
        "type": message_type,
        "session_id": session_id,
        "learned_words": learned_words,
    }


def create_media_payload(session_id: str, media_payload: dict):
    return {
        "type": "vocabulary_media_updated",
        "session_id": session_id,
        "media": media_payload,
    }


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, session_id: str):
    await ws.accept()
    clients_by_session[session_id] = ws

    from app.patterns.singleton.LearningProgressManager import LearningProgressManager

    manager = LearningProgressManager()
    learned_words = [word.to_dict() for word in manager.get_words(session_id)]

    await ws.send_json(
        create_learned_words_payload(
            session_id,
            learned_words,
            "initial_learned_words",
        )
    )

    try:
        while True:
            await ws.receive_text()
    except Exception:
        if session_id in clients_by_session:
            del clients_by_session[session_id]


async def push_learned_words_to_session(session_id: str, learned_words: list[dict]):
    if session_id in clients_by_session:
        try:
            await clients_by_session[session_id].send_json(
                create_learned_words_payload(
                    session_id,
                    learned_words,
                    "learned_words_updated",
                )
            )
            return True
        except Exception:
            del clients_by_session[session_id]
    return False


async def push_media_update_to_session(session_id: str, media_payload: dict):
    if session_id in clients_by_session:
        try:
            await clients_by_session[session_id].send_json(
                create_media_payload(session_id, media_payload)
            )
            return True
        except Exception:
            del clients_by_session[session_id]
    return False
