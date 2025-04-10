from collections.abc import AsyncGenerator
from functools import partial

import traceback
import pytest
import yarl

from sqlalchemy.pool import NullPool
from alembic.config import Config
from alembic.command import upgrade as alembic_upgrade
from alembic.runtime import migration
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy import delete, text
from testcontainers.postgres import PostgresContainer
from main import app
from src.core.database import async_session, async_session_maker
from src.core.models import Event
from config import get_db_uri

async def create_database(engine):
    config = Config("alembic.ini")
    async with engine.begin() as conn:
        inspector = await conn.run_sync(lambda sync_conn: migration.MigrationContext.configure(sync_conn).get_current_revision())
        if inspector is None:
            await conn.run_sync(lambda sync_conn: alembic_upgrade(config, "head"))

async def drop_database(engine):
    async with engine.begin() as conn:
        result = await conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        ))
        tables = [row[0] for row in result]
        
        if tables:
            await conn.execute(text(f"TRUNCATE {', '.join(tables)} CASCADE"))

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres") as container:
        yield container

@pytest.fixture(scope="function")
async def postgres_engine(postgres_container):
    try:
        postgres_url = yarl.URL(postgres_container.get_connection_url()).with_scheme('postgresql+asyncpg')
        print (f"Postgres URL: {postgres_url}")
        engine = create_async_engine(str(postgres_url), poolclass=NullPool)
        yield engine
    finally:
        await engine.dispose()

@pytest.fixture
async def postgres_session_factory(postgres_engine: AsyncEngine) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    await create_database(postgres_engine)
    yield async_sessionmaker(postgres_engine, expire_on_commit=False)
    await drop_database(postgres_engine)

@pytest.fixture
async def postgres_session(postgres_session_factory) -> AsyncGenerator[AsyncSession, None]:
    async with postgres_session_factory() as session:
        yield session

@pytest.fixture(autouse=True)
async def setup_test_database(postgres_session_factory):
    original_session_maker = async_session_maker
    
    async def override_async_session():
        async with postgres_session_factory() as session:
            yield session
    
    app.dependency_overrides[async_session] = override_async_session
    
    yield
    
    app.dependency_overrides.clear()

@pytest.fixture
async def async_http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/events") as client:
        yield client
