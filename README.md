# Ai_shop

Telegram bot shop on `aiogram 3` with PostgreSQL, SQLAlchemy async sessions, i18n (`ru`/`en`) and Alembic-based schema tracking.

## What the project does

- registers Telegram users in PostgreSQL
- stores user profile data, balance and selected language
- shows a localized start menu
- displays RUB balance with USD conversion
- supports a simple top-up flow stub through bot UI
- tracks DB schema through Alembic

## Stack

- Python 3.12
- aiogram 3
- SQLAlchemy 2 + asyncpg
- PostgreSQL 16
- Alembic
- Docker Compose

## Project structure

```text
app/
  backend/
    core/        # config, DB engine, session factory
    models/      # SQLAlchemy models
    services/    # business logic for users
    utils/       # helper functions
  bot/
    handlers/    # bot handlers
    keyboards/   # inline/reply keyboards
    locales/     # i18n translations
migrations/      # Alembic config and revisions
```

## Environment variables

Create a `.env` file in the project root.

Required:

```env
TOKEN=your_telegram_bot_token
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_shop
DB_USER=postgres
DB_PASSWORD=postgres
TG_CHANNEL=@your_channel
SUPPORT_ACCOUNT=@support
ADMINS=123456789,987654321
```

Optional:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_shop
```

If `DATABASE_URL` is not provided, it is assembled from `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.

## Local run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.bot.run_bot
```

Before running locally, make sure PostgreSQL is available and `.env` is configured.

## Run with Docker

Build images:

```powershell
docker compose build
```

Start PostgreSQL:

```powershell
docker compose up -d db
```

Run the bot:

```powershell
docker compose up -d bot
```

Apply migrations:

```powershell
docker compose run --rm migrate
```

## Alembic and migrations

The project already has Alembic configured in:

- `alembic.ini`
- `migrations/env.py`
- `migrations/versions/`

Current revision history starts with a baseline revision:

- `aa0b537312b2_baseline.py`

Important: the current baseline revision is empty and is intended for an existing database that already has the current schema. It does **not** create all tables from scratch on a clean database.

### For an existing database

Bind the current database state to Alembic once:

```powershell
docker compose run --rm bot alembic stamp head
```

After that, all future schema changes should go only through Alembic.

### For future schema changes

Create a new migration:

```powershell
docker compose run --rm bot alembic revision --autogenerate -m "describe_change"
```

Apply it:

```powershell
docker compose run --rm migrate
```

## Notes

- `migrate` is useful for applying future migrations to an existing database.
- the current baseline is not enough to bootstrap a brand-new database schema from zero
- exchange rate conversion uses an external HTTP API, so balance display depends on network availability

