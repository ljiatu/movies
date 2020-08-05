from typing import Any, List, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from movies.core.dataloaders.company_loader import CompanyLoader
from movies.core.dataloaders.movie_loader import MovieLoader
from movies.core.db import crud
from movies.core.entities.company import Company
from movies.core.entities.genre import Genre
from movies.core.entities.movie import Movie

movies = ObjectType("Movies")
movie = ObjectType("Movie")


@movies.field("movie")
async def resolve_movie(*_, id: int) -> int:
    return id


@movie.field("popularity")
async def resolve_popularity(obj, info: GraphQLResolveInfo) -> float:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.popularity


@movie.field("voteCount")
async def resolve_vote_count(obj, info: GraphQLResolveInfo) -> int:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.vote_count


@movie.field("video")
async def resolve_video(obj, info: GraphQLResolveInfo) -> bool:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.video


@movie.field("posterPath")
async def resolve_poster_path(obj, info: GraphQLResolveInfo) -> Optional[str]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.poster_path


@movie.field("externalId")
async def resolve_external_id(obj, info: GraphQLResolveInfo) -> Optional[int]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.external_id


@movie.field("adult")
async def resolve_adult(obj, info: GraphQLResolveInfo) -> bool:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.adult


@movie.field("backdropPath")
async def resolve_backdrop_path(obj, info: GraphQLResolveInfo) -> Optional[str]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.backdrop_path


@movie.field("originalLanguage")
async def resolve_original_language(obj, info: GraphQLResolveInfo) -> Optional[str]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.original_language


@movie.field("originalTitle")
async def resolve_original_title(obj, info: GraphQLResolveInfo) -> Optional[str]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.original_title


@movie.field("title")
async def resolve_title(obj, info: GraphQLResolveInfo) -> str:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.title


@movie.field("voteAverage")
async def resolve_vote_average(obj, info: GraphQLResolveInfo) -> float:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.vote_average


@movie.field("overview")
async def resolve_overview(obj, info: GraphQLResolveInfo) -> Optional[str]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.overview


@movie.field("releaseDate")
async def resolve_release_date(obj, info: GraphQLResolveInfo) -> str:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.release_date


@movie.field("budget")
async def resolve_budget(obj, info: GraphQLResolveInfo) -> Optional[int]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.budget


@movie.field("homepage")
async def resolve_homepage(obj, info: GraphQLResolveInfo) -> Optional[str]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.homepage


@movie.field("imdbId")
async def resolve_imdb_id(obj, info: GraphQLResolveInfo) -> Optional[str]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.imdb_id


@movie.field("revenue")
async def resolve_revenue(obj, info: GraphQLResolveInfo) -> int:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.revenue


@movie.field("runtime")
async def resolve_runtime(obj, info: GraphQLResolveInfo) -> Optional[int]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.runtime


@movie.field("status")
async def resolve_status(obj, info: GraphQLResolveInfo) -> Optional[str]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.status


@movie.field("tagline")
async def resolve_tagline(obj, info: GraphQLResolveInfo) -> Optional[str]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.tagline


@movie.field("genres")
async def resolve_genres(obj, info: GraphQLResolveInfo) -> List[Genre]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    return loaded_movie.genres


@movie.field("productionCompanies")
async def resolve_production_companies(
    obj, info: GraphQLResolveInfo
) -> Optional[List[Company]]:
    assert isinstance(obj, int)
    loaded_movie = await _load_movie(info.context, obj)
    company_loader = CompanyLoader.for_context(info.context)
    companies = await company_loader.load_many(
        [c.id for c in loaded_movie.production_companies]
    )
    return companies


@movies.field("popularMovies")
async def resolve_popular_movies(
    _, info: GraphQLResolveInfo, limit: int = 10
) -> List[Movie]:
    s = info.context["request"].state.db_session
    return crud.get_popular_movies(s, limit)


async def _load_movie(context: Any, id: int) -> Movie:
    movie_loader = MovieLoader.for_context(context)
    return await movie_loader.load(id)
