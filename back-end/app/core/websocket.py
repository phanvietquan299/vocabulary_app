from fastapi import APIRouter, WebSocket

router = APIRouter()
clients_by_session = {}


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, session_id: str):
    await ws.accept()
    clients_by_session[session_id] = ws

    from app.patterns.singleton.LearningProgressManager import LearningProgressManager

    manager = LearningProgressManager()
    learned_words = manager.get_words(session_id)

    await ws.send_json({
        "type": "initial_learned_words",
        "session_id": session_id,
        "learned_words": [word.to_dict() for word in learned_words]
    })

    try:
        while True:
            await ws.receive_text()
    except Exception:
        if session_id in clients_by_session:
            del clients_by_session[session_id]

async def push_learned_words_to_session(session_id: str, learned_words: set):
    if session_id in clients_by_session:
        try:
            await clients_by_session[session_id].send_json({
                "session_id": session_id,
                "learned_words": list(learned_words)
            })
            return True
        except Exception:
            del clients_by_session[session_id]
    return False