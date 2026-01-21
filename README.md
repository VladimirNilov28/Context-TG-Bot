# Context-TG-Bot

A Telegram bot powered by vector embeddings and PostgreSQL for semantic document search and question-answering.  Combines document ingestion, text chunking, embeddings, and similarity search with a Telegram interface.

## Overview

**Context-TG-Bot** is a RAG (Retrieval-Augmented Generation) application built with Python that: 
- Ingests documents (TXT, PDF) and chunks them intelligently
- Generates embeddings for semantic search
- Stores documents, chunks, and embeddings in PostgreSQL with pgvector extension
- Provides a Telegram bot interface for searching documents via natural language queries
- Supports both fake (deterministic) and real (OpenAI) embeddings

**Key Technologies:**
- Language:  Python 3.11+
- Framework: aiogram (async Telegram bot)
- Database: PostgreSQL with pgvector extension
- ORM: SQLAlchemy
- Embeddings: OpenAI API or deterministic fake embeddings
- Document Readers: pdfplumber, pdfminer for PDF extraction

## Project Structure

```
Context-TG-Bot/
├── app/
│   ├── bot.py              # Main Telegram bot entry point & dispatcher
│   ├── main.py             # Smoke tests for DB & search functionality
│   ├── core/
│   │   └── config.py       # Settings loaded from environment variables
│   ├── db/
│   │   ├── session.py      # SQLAlchemy session & engine setup
│   │   └── models.py       # ORM models:  Document, Chunk, Embedding
│   ├── services/
│   │   ├── embeddings.py   # Fake & OpenAI embedding generation
│   │   ├── chunking.py     # Text splitting & tokenization
│   │   ├── ingest.py       # Document ingestion pipeline
│   │   ├── search.py       # Vector similarity search (pgvector)
│   │   ├── readers.py      # TXT & PDF file readers
│   │   └── rag.py          # RAG functionality (context assembly)
│   ├── handlers/
│   │   ├── start.py        # /start command
│   │   ├── help.py         # /help command
│   │   ├── ask.py          # /ask <question> search handler
│   │   ├── debug.py        # /debug diagnostics
│   │   ├── upload.py       # File upload & ingestion
│   │   └── echo.py         # Fallback echo handler
│   ├── scripts/
│   │   ├── seed_demo.py    # One-off demo data seeding (1 doc, 2 chunks, 2 embeddings)
│   │   ├── ingest_demo.py  # Demo ingestion with counters
│   │   └── debug_query.py  # Debug similarity search
│   └── Dockerfile          # Docker setup (Python 3.11-slim)
├── docker/
│   ├── docker-compose.yml  # PostgreSQL + pgvector setup
│   └── postgres.env        # DB environment variables
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Prerequisites

- **Python 3.11+**
- **PostgreSQL 14+** with pgvector extension
- **Docker & Docker Compose** (recommended for PostgreSQL)
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- OpenAI API Key (optional, if using real embeddings)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/VladimirNilov28/Context-TG-Bot.git
cd Context-TG-Bot
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source . venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL with pgvector

Using Docker Compose (recommended):

```bash
cd docker
docker-compose up -d
```

Or manually install PostgreSQL and pgvector extension:

```bash
CREATE EXTENSION IF NOT EXISTS vector;
```

### 5. Configure Environment Variables

Create `app/.env`:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Database (local development)
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/contextdb

# OpenAI (optional, for real embeddings)
OPENAI_API_KEY=your_openai_key_here

# Embeddings Configuration
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIM=1536
USE_FAKE_EMBEDDINGS=true  # Set to 'false' for real OpenAI embeddings

# Environment
ENV=dev
```

## Usage

### Run the Bot

```bash
cd app
python bot.py
```

The bot will start polling for updates.  Find your bot on Telegram and use: 

```
/start           - Check bot connectivity
/help            - Show available commands
/ask <question>  - Search for relevant document chunks
/debug           - Show database & configuration diagnostics
```

### Example Query

```
/ask what is vector search
```

Bot responds with top 5 most similar chunks from ingested documents, showing:
- Chunk ID
- Distance score (cosine distance)
- Content preview (first 400 characters)

### Demo Scripts

#### Seed Demo Data

```bash
cd app
python scripts/seed_demo.py
```

Creates 1 document with 2 chunks and 2 embeddings for testing.

#### Ingest Demo

```bash
python scripts/ingest_demo.py
```

Ingests a demo text and displays document/chunk/embedding counts.

#### Debug Query

```bash
python scripts/debug_query.py
```

Tests embedding generation and similarity search.

#### Smoke Tests

```bash
python main.py
```

Checks database connectivity and search functionality.

## Configuration

### Core Settings (`app/core/config.py`)

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | Required | Telegram bot API token |
| `DATABASE_URL` | Required | PostgreSQL connection string |
| `OPENAI_API_KEY` | Optional | OpenAI API key for real embeddings |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model name |
| `EMBEDDING_DIM` | `1536` | Embedding dimension (must match model) |
| `USE_FAKE_EMBEDDINGS` | `true` | Use deterministic fake embeddings (dev) |
| `ENV` | `dev` | Environment: `dev` or `prod` |

### Database Models

**Document**
- `id`: Primary key
- `source`: Document source/filename
- `mime`: MIME type (e.g., `text/plain`, `application/pdf`)
- `created_at`: Timestamp

**Chunk**
- `id`: Primary key
- `document_id`: Foreign key to Document
- `content`: Text content
- `token_count`: Approximate token count
- `chunk_order`: Position in document

**Embedding**
- `id`: Primary key
- `chunk_id`: Foreign key to Chunk
- `vector`: pgvector (embedding vector)
- `model`: Embedding model name
- `created_at`: Timestamp

## Development

### Project Layout

```
Services → Handle core logic (embeddings, search, ingestion)
Handlers → Telegram message handlers (commands & events)
DB       → Models & session management
Core     → Configuration & constants
Scripts  → One-off utilities & demos
```

### Key Services

- **`embeddings.py`**: Generates embeddings (fake or OpenAI)
- **`chunking.py`**: Splits documents into chunks with overlap
- **`ingest.py`**: Pipeline:  text → chunks → embeddings → DB
- **`search.py`**: pgvector similarity search (cosine distance)
- **`readers.py`**: Handles TXT & PDF file extraction

### Code Style

- Type hints throughout
- Russian comments for clarity
- Async/await for Telegram handlers
- SQLAlchemy ORM for database operations

## Docker Deployment

### Build Image

```bash
docker build -t context-tg-bot -f app/Dockerfile .
```

### Run Container

```bash
docker run -it \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e DATABASE_URL=postgresql://postgres:postgres@db:5432/contextdb \
  -e USE_FAKE_EMBEDDINGS=true \
  context-tg-bot
```

With Docker Compose:

```bash
cd docker
docker-compose up
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Verify DATABASE_URL in app/. env matches docker-compose setup
# Local:  postgresql://postgres:postgres@localhost:5433/contextdb
# Docker: postgresql://postgres:postgres@db:5432/contextdb
```

### Debug Command

Send `/debug` to bot to see: 
- Environment (dev/prod)
- Embedding configuration
- Database connection details
- Document/chunk/embedding counts

### Missing pgvector Extension

```bash
docker exec <postgres_container> psql -U postgres -d contextdb -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

## License

This project is open source.  License details TBD.

## Contact

**Author:** [VladimirNilov28](https://github.com/VladimirNilov28)

For questions or issues, please open a GitHub issue in the repository. 

---

**Last Updated:** January 2026  
**Repository:** [VladimirNilov28/Context-TG-Bot](https://github.com/VladimirNilov28/Context-TG-Bot)
