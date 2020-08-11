import aiohttp
from ariadne import ObjectType, convert_kwargs_to_snake_case

from movies.core.clients.tmdb import post
from movies.settings import TMDB_BASE_URL, TMDB_GUEST_SESSION_ID

movie_mutations = ObjectType("MovieMutations")


class RatingOutOfBoundException(ValueError):
    def __init__(self, rating: float):
        self.rating = rating

    def __str__(self):
        return f"Rating out of bound. Expected 0.5 <= rating <= 10, got {self.rating}"


@movie_mutations.field("rate")
@convert_kwargs_to_snake_case
async def resolve_rate(*_, movie_id: int, rating: float) -> bool:
    # TMDb requires rating to be within [0.5, 10].
    if rating < 0.5 or rating > 10:
        raise RatingOutOfBoundException(rating)
    query_url = f"{TMDB_BASE_URL}/movie/{movie_id}/rating"
    async with aiohttp.ClientSession() as httpSession:
        params = {"guest_session_id": TMDB_GUEST_SESSION_ID}
        data = {"value": rating}
        await post(httpSession, query_url, data=data, params=params)
        return True
