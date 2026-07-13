import asyncio
import sys

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin

from src.core.config import settings
from src.core.database import engine
from src.core.provider import MyAuthProvider
from src.infra.messaging.broker import lifespan
from src.models.log import AuditLog, AuditLogView

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.add_middleware(SessionMiddleware, secret_key=settings.MIDDLEWARE_STARTLETTE)

admin = Admin(
    engine,
    title='Ateliê Digital - Auditoria',
    base_url='/admin/',
    auth_provider=MyAuthProvider(login_path='/sign-in', logout_path='/sign-out'),
)

admin.add_view(AuditLogView(AuditLog))

admin.mount_to(app)
