from typing import Callable

from ariadne.asgi import GraphQL
from fastapi import FastAPI, Request

from movies.core.db.session import SessionLocal
from movies.core.resolvers.query import schema

app = FastAPI(debug=True)
app.mount("/graphql", GraphQL(schema, debug=True))


@app.middleware("http")
async def attach_db_session(request: Request, call_next: Callable):
    try:
        request.state.db_session = SessionLocal()
        return await call_next(request)
    finally:
        request.state.db_session.close()
