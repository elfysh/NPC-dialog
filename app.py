import json
from contextlib import asynccontextmanager
from typing import Iterator, Optional

import faiss
import polars as pl
import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

from character_bot import SkyrimCharacterService
from config import settings

_service: Optional[SkyrimCharacterService] = None


def _load_chunks() -> pl.DataFrame:
    path = settings.chunks_path
    if not path.exists():
        raise FileNotFoundError(f"Нет файла с чанками: {path.resolve()}")
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pl.read_parquet(path)
    if suffix == ".csv":
        return pl.read_csv(path)
    if suffix == ".jsonl":
        return pl.read_ndjson(path)
    raise ValueError(f"Поддерживаются .parquet, .jsonl и .csv, получено: {suffix}")


def _load_faiss():
    p = settings.faiss_index_path
    if not p.exists():
        raise FileNotFoundError(f"Нет FAISS индекса: {p.resolve()}")
    return faiss.read_index(str(p))


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _service
    chunks_db = _load_chunks()
    embedding_model = SentenceTransformer(settings.embedding_model_name)
    faiss_index = _load_faiss()

    _service = SkyrimCharacterService(
        chunks_db=chunks_db,
        embedding_model=embedding_model,
        faiss_index=faiss_index,
        lora_path=settings.lora_path,
        max_seq_length=settings.max_seq_length,
        max_new_tokens_default=settings.max_new_tokens_generate,
        dtype=torch.float16,
        load_in_4bit=settings.load_in_4bit,
        logs_dir=settings.conversation_logs_dir,
    )
    yield
    _service = None


app = FastAPI(title="Skyrim Character API", lifespan=lifespan)


def get_service() -> SkyrimCharacterService:
    if _service is None:
        raise HTTPException(status_code=503, detail="Сервис ещё не готов")
    return _service


class SetupBody(BaseModel):
    session_id: str = Field(..., min_length=1, description="Идентификатор сессии диалога")
    character_name: str
    location: str
    active_quest: str
    player_query: str


class ChatBody(BaseModel):
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ResetBody(BaseModel):
    session_id: str = Field(..., min_length=1)


@app.get("/health")
def health():
    return {"ok": True, "model_loaded": _service is not None}


@app.post("/setup")
def setup_character(body: SetupBody):
    """
    Первый ход: полный ответ в JSON после генерации.
    Поток на клиенте: POST /setup/stream (SSE).
    """
    svc = get_service()
    text = svc.setup_character(
        session_id=body.session_id,
        character_name=body.character_name,
        location=body.location,
        active_quest=body.active_quest,
        player_query=body.player_query,
    )
    return {"response": text, "log_path": str(svc.session_log_path(body.session_id))}


@app.post("/chat")
def chat(body: ChatBody):
    svc = get_service()
    text = svc.chat(session_id=body.session_id, user_message=body.message)
    return {"response": text, "log_path": str(svc.session_log_path(body.session_id))}


def _sse_pack(obj: dict) -> str:
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


STREAM_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
}


@app.post("/setup/stream")
def setup_character_stream(body: SetupBody):
    """SSE: события `data: {\"chunk\": \"...\"}` и финально `{\"done\": true, \"log_path\": \"...\"}`."""

    def event_iter() -> Iterator[str]:
        svc = get_service()
        try:
            for piece in svc.stream_setup_character(
                session_id=body.session_id,
                character_name=body.character_name,
                location=body.location,
                active_quest=body.active_quest,
                player_query=body.player_query,
            ):
                if piece:
                    yield _sse_pack({"chunk": piece})
            yield _sse_pack(
                {"done": True, "log_path": str(svc.session_log_path(body.session_id))}
            )
        except Exception as e:
            yield _sse_pack({"error": str(e)})

    return StreamingResponse(
        event_iter(),
        media_type="text/event-stream",
        headers=STREAM_HEADERS,
    )


@app.post("/chat/stream")
def chat_stream(body: ChatBody):
    def event_iter() -> Iterator[str]:
        svc = get_service()
        try:
            for piece in svc.stream_chat(session_id=body.session_id, user_message=body.message):
                if piece:
                    yield _sse_pack({"chunk": piece})
            yield _sse_pack(
                {"done": True, "log_path": str(svc.session_log_path(body.session_id))}
            )
        except Exception as e:
            yield _sse_pack({"error": str(e)})

    return StreamingResponse(
        event_iter(),
        media_type="text/event-stream",
        headers=STREAM_HEADERS,
    )


@app.post("/reset")
def reset_session(body: ResetBody):
    get_service().reset_session(body.session_id)
    return {"ok": True}


def main():
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )


if __name__ == "__main__":
    main()
