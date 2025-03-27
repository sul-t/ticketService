# from fastapi import Request

# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# from main import app
# from events.config import get_db_uri


# async_engine = create_async_engine(get_db_uri())
# AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)

# @app.middleware('http')
# async def db_session_middleware(request: Request, call_next):
#     session: AsyncSession = None

#     try:
#         session = AsyncSessionLocal()
#         # request.state.db = await session()

#         response = await call_next(request)

#         await session.commit()

#         return response

#     except Exception as e:
#         if request.state.db.is_active:
#             await session.db.rollback()

#         raise

#     finally:
#         if session is not None:
#             await session.close()