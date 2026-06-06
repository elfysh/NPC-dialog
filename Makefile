.PHONY: help venv sync install-unsloth setup api front front-demo

PYTHON := 3.10.12
API_HOST ?= 0.0.0.0
API_PORT ?= 8000
FRONT_PORT ?= 8501
# WB Demo stands: https://demo-stands.wb.ru/<prefix>/<jupyterhub-user>/ (https://demo-stands.wb.ru/research/borovskoy.roman/)
# Требуют bind 0.0.0.0 и порт 8282. Streamlit по их доке префикс в команде не задаёт.
DEMO_STAND_PORT ?= 8282
API_BASE_URL ?= http://127.0.0.1:$(API_PORT)

help:
	@echo "Targets:"
	@echo "  make setup          - create .venv, sync deps, install unsloth"
	@echo "  make venv           - create .venv with Python $(PYTHON)"
	@echo "  make sync           - install deps from pyproject.toml"
	@echo "  make install-unsloth - install unsloth separately"
	@echo "  make api            - run FastAPI server"
	@echo "  make front          - run Streamlit (local / SSH-туннель; порт $(FRONT_PORT))"
	@echo "  make front-demo     - Streamlit для demo-stands.wb.ru (0.0.0.0:$(DEMO_STAND_PORT))"
	@echo ""
	@echo "Demo stands: подними API на этой же ВМ (make api), затем make front-demo."
	@echo "В браузере открой https://demo-stands.wb.ru/research/borovskoy.roman/"
	@echo "  Dev      → /research-dev/<user>/"
	@echo "  Research → /research/<user>/"
	@echo "  GPU      → /research-gpu/<user>/"
	@echo ""
	@echo "Optional env vars:"
	@echo "  CHUNKS_PATH, FAISS_INDEX_PATH, LORA_PATH, EMBEDDING_MODEL_NAME"
	@echo "  API_HOST, API_PORT, FRONT_PORT, DEMO_STAND_PORT, API_BASE_URL"

venv:
	uv venv --python $(PYTHON)

sync:
	uv sync

install-unsloth:
	uv pip install unsloth

setup: venv sync install-unsloth

api:
	uv run uvicorn app:app --host $(API_HOST) --port $(API_PORT)

front:
	API_BASE_URL=$(API_BASE_URL) uv run streamlit run streamlit_front.py \
		--server.address 0.0.0.0 --server.port $(FRONT_PORT)

front-demo:
	API_BASE_URL=$(API_BASE_URL) uv run streamlit run streamlit_front.py \
		--server.address 0.0.0.0 --server.port $(DEMO_STAND_PORT)
