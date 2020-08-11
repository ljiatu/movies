from ariadne import (
    MutationType,
    QueryType,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)

from movies.core.resolvers.mutations.movie import movie_mutations
from movies.core.resolvers.queries.company import companies
from movies.core.resolvers.queries.movie import movie, movies

type_defs = load_schema_from_path("graphql/")

query = QueryType()
mutation = MutationType()


@query.field("movies")
async def resolve_movies(*_):
    return {}


@query.field("companies")
async def resolve_companies(*_):
    return {}


@mutation.field("movieMutations")
async def resolve_movie_mutations(*_):
    return {}


schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    movies,
    movie,
    companies,
    snake_case_fallback_resolvers,
    movie_mutations,
)
