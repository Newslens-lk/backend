# backend

Backend for the Bias-Aware Sinhala News Aggregation Platform (Newslens). Implements the data,
processing, model and API layers described in the project SRS: Sinhala news collection,
event clustering, event summarization, bias classification and reporting-difference analysis,
exposed over a versioned REST API.

## Stack

- **API**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 14+ with `pgvector`
- **Cache / rate limiting**: Redis
- **ML**: scikit-learn, PyTorch, Transformers, spaCy, HDBSCAN + Leiden, MLflow (see `requirements-ml.txt`)
- **Migrations**: Alembic

## Project layout

```
app/
  api/v1/          REST endpoints (health, articles, events, predict)
  collection/       Scraping + external dataset ingestion (FR1.1)
  preprocessing/     Cleaning / normalisation
  embedding/         LASER3 sentence embeddings (FR1.3)
  clustering/         HDBSCAN + Leiden event clustering (FR1.3)
  summarization/      Multi-document event summaries (FR1.4)
  classification/      Bias classifier training + inference (FR1.5)
  models/           SQLAlchemy ORM models (matches SRS 3.10 schema)
  schemas/          Pydantic request/response models
  db/               Engine/session setup
  core/             Settings, rate limiting
alembic/            Database migrations
tests/
```

The `collection`, `embedding`, `clustering`, `summarization` and `classification` modules are
currently stubs (`NotImplementedError`) marking where each pipeline stage needs to be built out;
the API, database schema, and request/response contracts around them are functional.

## Getting started

1. Copy the environment template and adjust as needed:
   ```
   cp .env.example .env
   ```
2. Start Postgres + Redis + the API with Docker Compose:
   ```
   docker compose up --build
   ```
3. Apply database migrations:
   ```
   docker compose exec api alembic upgrade head
   ```
4. API docs are available at `http://localhost:8000/docs`.

### Local development without Docker

```
python -m venv .venv
.venv/Scripts/activate   # or source .venv/bin/activate on macOS/Linux
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Install `requirements-ml.txt` separately when working on embedding, clustering, summarization or
classification (heavier dependencies, not required to run the API/DB layer).

## Tests & linting

```
pytest
ruff check app tests alembic
```
