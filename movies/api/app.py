from typing import Callable

from ariadne.asgi import GraphQL
from fastapi import FastAPI, Request

from movies.core.db.session import create_db_session, db_engine
from movies.core.resolvers.base import schema

app = FastAPI(debug=True)
app.mount("/graphql", GraphQL(schema, debug=True))


@app.middleware("http")
async def attach_db_session(request: Request, call_next: Callable):
    try:
        request.state.db_session = create_db_session(db_engine)()
        return await call_next(request)
    finally:
        request.state.db_session.close()
