from __future__ import annotations

from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from threading import Thread
from typing import Dict, Generator, List, Optional

import numpy as np
import polars as pl
import torch
from transformers import TextIteratorStreamer

from cyrillic_boost import CyrillicBoostLogitsProcessor


@dataclass
class SessionState:
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    character_context: Optional[str] = None
    is_first_message: bool = True


class SkyrimCharacterService:
    """
    Одна загрузка модели и RAG; отдельная история на session_id.
    Потоковая генерация — через TextIteratorStreamer (SSE в app.py).
    """

    def __init__(
        self,
        chunks_db: pl.DataFrame,
        embedding_model,
        faiss_index,
        lora_path: str,
        max_seq_length: int = 8192,
        max_new_tokens_default: int = 256,
        dtype: torch.dtype = torch.float16,
        load_in_4bit: bool = True,
        logs_dir: Path = Path("./logs/conversations"),
    ):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.max_new_tokens_default = max_new_tokens_default
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.embedding_model = embedding_model
        self.faiss_index = faiss_index
        self.chunks_db = chunks_db
        self._text_col = "text" if "text" in chunks_db.columns else chunks_db.columns[1]
        self._index_col = "index" if "index" in chunks_db.columns else chunks_db.columns[0]

        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=lora_path,
            max_seq_length=max_seq_length,
            dtype=dtype,
            load_in_4bit=load_in_4bit,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True,
            use_cache=True,
        )
        self.tokenizer = get_chat_template(self.tokenizer)
        FastLanguageModel.for_inference(self.model)

        self._sessions: Dict[str, SessionState] = {}
        self._cyrillic_processor = CyrillicBoostLogitsProcessor(self.tokenizer)

    @staticmethod
    def _safe_session_filename(session_id: str) -> str:
        cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "_", session_id).strip("._-") or "session"
        return cleaned[:200]

    def session_log_path(self, session_id: str) -> Path:
        return (self.logs_dir / f"{self._safe_session_filename(session_id)}.json").resolve()

    def _session(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionState()
        return self._sessions[session_id]

    def _persist_session(self, session_id: str) -> None:
        s = self._session(session_id)
        path = self.session_log_path(session_id)
        payload = {
            "session_id": session_id,
            "character_context": s.character_context,
            "is_first_message": s.is_first_message,
            "history": s.conversation_history,
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def search_relevant_chunks(self, query: str, k: int = 3, min_score: float = 0.6) -> List[str]:
        try:
            query_vec = self.embedding_model.encode(
                [query],
                prompt_name="query",
                normalize_embeddings=True,
            )
        except TypeError:
            query_vec = self.embedding_model.encode([query], normalize_embeddings=True)
        scores, indices = self.faiss_index.search(query_vec.astype(np.float32), k * 2)

        results: List[str] = []
        for score, idx in zip(scores[0], indices[0]):
            if score < min_score:
                continue
            chunk_row = self.chunks_db.filter(pl.col(self._index_col) == int(idx))
            if len(chunk_row) > 0:
                row = chunk_row.row(0, named=True)
                results.append(row[self._text_col])

        return results[:k]

    def _prepare_setup(
        self,
        session_id: str,
        character_name: str,
        location: str,
        active_quest: str,
        player_query: str,
    ) -> SessionState:
        s = self._session(session_id)
        s.is_first_message = True
        s.conversation_history = []

        npc_chunks = self.search_relevant_chunks(character_name, k=3, min_score=0.6)
        location_chunks = self.search_relevant_chunks(location, k=2, min_score=0.65)
        quest_chunks = self.search_relevant_chunks(active_quest, k=2, min_score=0.5)
        query_chunks = self.search_relevant_chunks(player_query, k=2, min_score=0.95)

        context_parts: List[str] = []
        if npc_chunks:
            context_parts.append(f"О персонаже {character_name}:\n" + "\n".join(npc_chunks))
        if location_chunks:
            context_parts.append(f"О локации {location}:\n" + "\n".join(location_chunks))
        if quest_chunks:
            context_parts.append(f"О квесте {active_quest}:\n" + "\n".join(quest_chunks))

        s.character_context = "\n\n".join(context_parts)
        system_prompt = self._build_system_prompt(character_name, s.character_context, query_chunks)

        s.conversation_history.append({"role": "system", "content": system_prompt})
        s.conversation_history.append({"role": "user", "content": player_query})
        return s

    def setup_character(
        self,
        session_id: str,
        character_name: str,
        location: str,
        active_quest: str,
        player_query: str,
    ) -> str:
        s = self._prepare_setup(session_id, character_name, location, active_quest, player_query)
        response = self._generate_response(s)
        s.conversation_history.append({"role": "assistant", "content": response})
        s.is_first_message = False

        self._persist_session(session_id)
        return response

    def stream_setup_character(
        self,
        session_id: str,
        character_name: str,
        location: str,
        active_quest: str,
        player_query: str,
    ) -> Generator[str, None, None]:
        s = self._prepare_setup(session_id, character_name, location, active_quest, player_query)
        parts: List[str] = []
        try:
            for chunk in self._iter_generated_chunks(s):
                parts.append(chunk)
                yield chunk
        except Exception:
            raise
        full = "".join(parts).strip()
        s.conversation_history.append({"role": "assistant", "content": full})
        s.is_first_message = False
        self._persist_session(session_id)

    def _append_user_message(self, session_id: str, user_message: str) -> SessionState:
        s = self._session(session_id)
        query_chunks = self.search_relevant_chunks(user_message, k=2)

        if query_chunks:
            context_note = "[Контекст из знаний]:\n" + "\n".join(query_chunks)
            enhanced_message = f"{context_note}\n\n[Сообщение игрока]:\n{user_message}"
        else:
            enhanced_message = user_message

        s.conversation_history.append({"role": "user", "content": enhanced_message})
        return s

    def chat(self, session_id: str, user_message: str) -> str:
        s = self._append_user_message(session_id, user_message)
        response = self._generate_response(s)
        s.conversation_history.append({"role": "assistant", "content": response})

        self._persist_session(session_id)
        return response

    def stream_chat(self, session_id: str, user_message: str) -> Generator[str, None, None]:
        s = self._append_user_message(session_id, user_message)
        parts: List[str] = []
        try:
            for chunk in self._iter_generated_chunks(s):
                parts.append(chunk)
                yield chunk
        except Exception:
            raise
        full = "".join(parts).strip()
        s.conversation_history.append({"role": "assistant", "content": full})
        self._persist_session(session_id)

    def reset_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]
        path = self.session_log_path(session_id)
        if path.exists():
            path.unlink()

    def _build_system_prompt(
        self,
        character_name: str,
        base_context: str,
        query_chunks: List[str],
    ) -> str:
        system_prompt = f"""Ты — {character_name}, персонаж из вселенной The Elder Scrolls: Skyrim.
Отвечай от первого лица, сохраняя характер, манеру речи и мировоззрение персонажа.

Вот немного информации или цитат про персонажа: {base_context}

"""
        if query_chunks:
            system_prompt += f"""Дополнительная информация, релевантная текущему разговору:
{chr(10).join(query_chunks)}

"""

        system_prompt += """
Отвечай реалистично и соответственно своему персонажу и ситуации.
Реагируй на игрока соответствующе. Не бойся быть злым, агрессивным или рассерженным, если того требует ситуация.
Не выходи из роли! Не упоминай, что ты ИИ или языковая модель. Не выдумывай! Если чего-то не знаешь, то так и говори.
Если игрок говорит чушь, не имеющую отношения к ситуации, не бойся реагировать соответственно.
Ты ничего не знаешь из современности. Твой сеттинг - средневековье. Из сеттинга не выходи.
Если спрашивают про что-то из математики, программирования, медицины и других наук, то скажи,
что не знаешь такой магии и посоветуй сходить в лечебницу Стендарра.
Отвечай кратко.
ГОВОРИ ТОЛЬКО ПО-РУССКИ. Запрещено использовать латинские буквы и английские слова.
Даже имена и названия пиши кириллицей."""
        return system_prompt

    def _generate_response(self, session: SessionState, max_new_tokens: Optional[int] = None) -> str:
        return "".join(self._iter_generated_chunks(session, max_new_tokens)).strip()

    def _iter_generated_chunks(
        self,
        session: SessionState,
        max_new_tokens: Optional[int] = None,
    ) -> Generator[str, None, None]:
        max_new_tokens = max_new_tokens or self.max_new_tokens_default

        prompt = self.tokenizer.apply_chat_template(
            session.conversation_history,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        streamer = TextIteratorStreamer(
            self.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
        )

        gen_kwargs = {
            **inputs,
            "max_new_tokens": max_new_tokens,
            "max_length": None,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
            "repetition_penalty": 1.1,
            "do_sample": True,
            "pad_token_id": self.tokenizer.eos_token_id,
            "use_cache": True,
            "num_beams": 1,
            "early_stopping": False,
            "streamer": streamer,
            "logits_processor": [self._cyrillic_processor],
        }

        thread = Thread(target=self._generate_in_thread, kwargs=gen_kwargs)
        thread.start()
        try:
            for text in streamer:
                yield text
        finally:
            thread.join()

    def _generate_in_thread(self, **gen_kwargs):
        with torch.no_grad():
            self.model.generate(**gen_kwargs)
