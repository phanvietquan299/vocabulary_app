from fastapi import APIRouter, WebSocket

router = APIRouter()
clients_by_session = {}


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, session_id: str):
    print("WS CONNECTED")
    await ws.accept()
    clients_by_session[session_id] = ws
    await ws.send_text("WebSocket connected")

    try:
        while True:
            await ws.receive_text()
    except Exception:
        if session_id in clients_by_session:
            del clients_by_session[session_id]

async def push_to_all(message: str):
    count = 0
    for client in clients_by_session.values():
        try:
            await client.send_text(message)
            count += 1
        except Exception:
            pass
    return count


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