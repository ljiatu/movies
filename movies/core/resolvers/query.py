from ariadne import (
    QueryType,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)

from movies.core.resolvers.company import companies
from movies.core.resolvers.movie import movie, movies

type_defs = load_schema_from_path("graphql/")

query = QueryType()


@query.field("movies")
async def resolve_movies(*_):
    return movies


@query.field("companies")
async def resolve_companies(*_):
    return companies


schema = make_executable_schema(
    type_defs, query, movies, movie, companies, snake_case_fallback_resolvers
)
