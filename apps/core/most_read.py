"""
Most Read engine — Redis sorted set backed popularity tracking.

Three time windows:
  mostread:3h   — trending (TTL 3 hours)
  mostread:24h  — today    (TTL 24 hours)
  mostread:7d   — weekly   (TTL 7 days)

Dedup key:
  viewed:{card_id}:{fingerprint}  — TTL 90 seconds

All operations fail silently if Redis is unavailable.
"""

import hashlib
import logging

from django.core.cache import cache

logger = logging.getLogger(__name__)

WINDOWS = {
    "3h": 3 * 3600,
    "24h": 24 * 3600,
    "7d": 7 * 24 * 3600,
}

DEDUP_TTL = 90  # seconds


def _get_redis():
    """Return raw Redis connection or None if unavailable."""
    try:
        from django_redis import get_redis_connection

        conn = get_redis_connection("redis")
        conn.ping()  # Eager check — lazy connections only fail on use
        return conn
    except Exception:
        return None


def _fingerprint(ip, user_agent):
    """Build a short hash from IP + User-Agent for dedup."""
    raw = f"{ip}:{user_agent}"
    return hashlib.md5(raw.encode(), usedforsecurity=False).hexdigest()[:12]


def record_view(card_id, ip, user_agent):
    """
    Increment view counters for a content card across all time windows.
    Skips if the same fingerprint viewed within DEDUP_TTL seconds.
    """
    conn = _get_redis()
    if conn is None:
        return

    try:
        fp = _fingerprint(ip, user_agent)
        dedup_key = f"viewed:{card_id}:{fp}"

        # Check dedup — skip if already counted recently
        if conn.get(dedup_key):
            return

        # Set dedup marker
        conn.setex(dedup_key, DEDUP_TTL, 1)

        # Increment across all windows
        pipe = conn.pipeline()
        for window, ttl in WINDOWS.items():
            key = f"mostread:{window}"
            pipe.zincrby(key, 1, str(card_id))
            # Set TTL only if not already set (preserves existing expiry)
            pipe.expire(key, ttl, nx=True)
        pipe.execute()

    except Exception:
        logger.exception("Failed to record view for card %s", card_id)


def get_most_read(window="24h", count=5):
    """
    Return the top N most-read ContentCards for the given window.
    Results are cached for 5 minutes in Django's default cache.
    Falls back to empty list if Redis is down.
    """
    cache_key = f"most_read:{window}:{count}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    conn = _get_redis()
    if conn is None:
        return []

    try:
        key = f"mostread:{window}"
        # Get top card IDs from sorted set (highest score first)
        raw_ids = conn.zrevrange(key, 0, count - 1)
        if not raw_ids:
            return []

        card_ids = [int(cid) for cid in raw_ids]

        from apps.articles.models import Article

        cards_by_id = {
            c.pk: c
            for c in Article.objects.filter(
                pk__in=card_ids,
                status="published",
                exclude_from_most_read=False,
            )
        }

        # Preserve Redis ordering
        result = [cards_by_id[cid] for cid in card_ids if cid in cards_by_id]

        cache.set(cache_key, result, timeout=300)
        return result

    except Exception:
        logger.exception("Failed to fetch most read for window %s", window)
        return []


def seed_from_cards(cards):
    """
    Seed the sorted sets with editorial picks.
    Higher sort_order cards get lower scores; featured cards get a boost.
    """
    conn = _get_redis()
    if conn is None:
        logger.warning("Redis unavailable — cannot seed most read data")
        return False

    try:
        pipe = conn.pipeline()
        for i, card in enumerate(cards):
            score = (len(cards) - i) * 10
            if card.is_featured:
                score += 50
            for window, ttl in WINDOWS.items():
                key = f"mostread:{window}"
                pipe.zadd(key, {str(card.pk): score})
                pipe.expire(key, ttl, nx=True)
        pipe.execute()
        logger.info("Seeded most read with %d cards", len(cards))
        return True
    except Exception:
        logger.exception("Failed to seed most read data — is Redis running?")
        return False
