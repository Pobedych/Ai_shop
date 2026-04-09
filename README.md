# Ai_shop

Telegram bot shop on `aiogram 3` with PostgreSQL, SQLAlchemy async sessions, Alembic migrations, i18n and `aiocryptopay` integration.

## What the project does

- registers Telegram users in PostgreSQL
- stores user profile data, selected language and balance
- shows a localized start menu
- supports `ru`, `en` and `zh` locales
- displays product categories and items from the database
- shows RUB balance with USD conversion through an external rate API
- has a top-up flow entrypoint with Crypto Pay invoice creation
- tracks schema changes through Alembic

## Current status

The project already has:

- user registration and update through middleware
- item browsing by category
- language switching
- admin-only `/admin` entrypoint
- Docker-based local environment
- PostgreSQL schema migrations

Payment flow is currently partial:

- the bot requests a top-up amount
- creates a Crypto Pay invoice through `aiocryptopay`
- but does not yet persist payment entities or credit the user balance after confirmed payment

## Stack

- Python 3.12
- aiogram 3.27
- SQLAlchemy 2.0
- asyncpg
- PostgreSQL 16
- Alembic
- aiogram_i18n + Fluent
- aiocryptopay
- Docker Compose

## Project structure

```text
app/
  backend/
    core/         # config and DB setup
    models/       # SQLAlchemy models
    services/     # user, shop and payment logic
    utils/        # helper utilities
  bot/
    fsm/          # FSM states
    handlers/     # Telegram handlers
    keyboards/    # inline/reply keyboards
    locales/      # Fluent translations
    middleware/   # DB, user, admin and i18n middleware
migrations/
  versions/       # Alembic revisions
```

## Environment variables

Create a `.env` file in the project root.

Required:

```env
TOKEN=your_telegram_bot_token
PAYMENT_API_KEY=your_cryptobot_api_token

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

If `DATABASE_URL` is not provided, it is assembled from the `DB_*` variables.

## Installation

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Local run

Before running locally:

- make sure PostgreSQL is available
- create the database
- configure `.env`
- apply migrations

Run migrations:

```powershell
alembic upgrade head
```

Start the bot:

```powershell
python -m app.bot.run_bot
```

## Run with Docker

Build containers:

```powershell
docker compose build
```

Start PostgreSQL:

```powershell
docker compose up -d db
```

Apply migrations:

```powershell
docker compose run --rm migrate
```

Start the bot:

```powershell
docker compose up -d bot
```

View logs:

```powershell
docker compose logs -f bot
```

Restart the bot after code or migration changes:

```powershell
docker compose up -d --build bot
```

## Deploy for miniapp.noxshop.ru

The main `docker-compose.yml` includes the bot, database, mini app and HTTPS termination.

Requirements before first start:

- the A record for `miniapp.noxshop.ru` must point to your server public IP
- ports `80` and `443` must be open on the server firewall
- Docker and Docker Compose plugin must be installed on the server
- copy your `.env` to the server, but use production secrets instead of local ones

Deploy:

```powershell
docker compose up -d --build
```

Check logs:

```powershell
docker compose logs -f caddy
docker compose logs -f miniapp
docker compose logs -f bot
```

Apply migrations manually if needed:

```powershell
docker compose run --rm migrate
```

Rebuild after frontend or bot changes:

```powershell
docker compose up -d --build
```

`Caddy` obtains and renews TLS certificates automatically, so `https://miniapp.noxshop.ru` should start working without a separate nginx + certbot setup.

## Migrations

Alembic is configured in:

- `alembic.ini`
- `migrations/env.py`
- `migrations/versions/`

Current migration chain includes:

- `aa0b537312b2_baseline.py`
- `3d4b0d6a9f21_create_items_table.py`
- `bc380ff60f42_create_users_table.py`
- `c7f8e2a4b1d9_align_users_schema_with_uuid_model.py`
- `d1a2f3b4c5d6_expand_users_balance_precision.py`

Apply all migrations:

```powershell
alembic upgrade head
```

Check current revision:

```powershell
alembic current
```

Create a new migration:

```powershell
alembic revision --autogenerate -m "describe_change"
```

## Main flows

### User flow

- `/start` creates or updates a user in the database
- the main menu provides access to shop, balance, settings and about pages
- language is stored in the `users` table and used by i18n middleware

### Shop flow

- categories are loaded from the `items` table
- item lists are filtered by category

### Balance flow

- the bot shows current balance in RUB
- it also tries to convert balance to USD through an external HTTP API
- if the exchange-rate API is unavailable, the bot falls back to a simplified welcome message

### Payment flow

- user selects top-up
- user chooses CryptoBot payment
- bot asks for an amount
- backend creates a Crypto Pay invoice

At the moment the project does not yet include:

- payment persistence in a separate table
- invoice status synchronization
- webhook handling
- safe balance crediting after confirmed payment

## Dependencies

Project dependencies are pinned in [requirements.txt](requirements.txt).

## Notes

- `payment_service.py` currently contains only a thin wrapper around `aiocryptopay`
- exchange-rate conversion depends on external network availability
- the bot uses polling, not webhook delivery
- bot state storage is in-memory
