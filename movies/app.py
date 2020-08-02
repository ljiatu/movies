from fastapi import FastAPI

app = FastAPI()


@app.get("/movies/popular")
async def get_popular_movies():
    pass
