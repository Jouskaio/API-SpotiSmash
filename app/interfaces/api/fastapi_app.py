import logging

from fastapi import FastAPI, HTTPException, Query

from app.infrastructure.logging.setup_logging import setup_logging
from app.interfaces.api.routes import user, callback, public_users

app = FastAPI()
setup_logging()
logger = logging.getLogger('uvicorn.error')


# All the routes are included in the main app
app.include_router(user.router)
app.include_router(callback.router)
app.include_router(public_users.router)