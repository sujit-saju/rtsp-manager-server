# ============================================
# File     : session.py
# Author   : Sujit
# Created  : 2026-06-12
# Desc     : Async database session manager
#            providing automatic transaction
#            handling with commit/rollback
#            and proper session cleanup.
# ============================================

from contextlib import asynccontextmanager

from app.database import SessionLocal


@asynccontextmanager
async def get_db():
    """
    Provides a new AsyncSession for each usage.

    Behavior:
    - Creates a new database session.
    - Commits the transaction if execution succeeds.
    - Rolls back the transaction if an exception occurs.
    - Ensures the session is always closed.

    Usage:
        async with get_db() as db:
            result = await db.execute(...)
    """

    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()