from ariadne import ObjectType, QueryType, convert_kwargs_to_snake_case, load_schema_from_path, make_executable_schema
from graphql import GraphQLResolveInfo

from movies.entities.db import crud

type_defs = load_schema_from_path("../graphql/")

query = QueryType()
movies = ObjectType("Movies")


@query.field("movies")
async def resolve_movies(*_):
    return movies


@movies.field("getMovieById")
@convert_kwargs_to_snake_case
async def resolve_movie_by_external_id(_, info: GraphQLResolveInfo, external_id: int):
    s = info.context["request"].state.db_session
    return crud.get_movie_by_external_id(s, external_id)


@movies.field("getPopularMovies")
async def resolve_popular_movies(_, info: GraphQLResolveInfo, limit: int = 10):
    s = info.context["request"].state.db_session
    return crud.get_popular_movies(s, limit)


schema = make_executable_schema(type_defs, query, movies)
