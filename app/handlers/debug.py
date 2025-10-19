from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import text
from app.db.session import engine, get_session
from app.core.config import settings

router = Router(name="debug")

@router.message(F.text == "/debug")
async def cmd_debug(msg: Message):
    with engine.connect() as c:
        db, addr, port = c.execute(
            text("SELECT current_database(), inet_server_addr(), inet_server_port()")
        ).one()
    with get_session() as s:
        counts = s.execute(text("""
            SELECT
              (SELECT count(*) FROM documents)  AS docs,
              (SELECT count(*) FROM chunks)     AS chunks,
              (SELECT count(*) FROM embeddings) AS embs,
              (SELECT count(*) FROM chunks c JOIN embeddings e ON e.chunk_id=c.id) AS join_count
        """)).mappings().one()

    await msg.answer(
        "DEBUG\n"
        f"ENV={settings.ENV}\n"
        f"EMBEDDING_DIM={settings.EMBEDDING_DIM}\n"
        f"USE_FAKE_EMBEDDINGS={settings.USE_FAKE_EMBEDDINGS}\n"
        f"DATABASE_URL={settings.DATABASE_URL}\n"
        f"DB_CONN={db}@{addr}:{port}\n"
        f"counts: {dict(counts)}"
    )
