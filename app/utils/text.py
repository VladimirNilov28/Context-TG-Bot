"""Текстовые утилиты."""
import re

def truncate(s: str, n: int = 500) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"

def strip_md(s: str) -> str:
    """Чуть-чуть обезоружим Markdown V2."""
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', s)
