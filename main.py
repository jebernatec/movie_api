# import
from typing import Optional

from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse

from pydantic import BaseModel, Field

# app
app = FastAPI()
app.title = "Movie_api"
app.version = "1.0.0"


# models
class Movie(BaseModel): 
    id: Optional[int]
    title: str = Field(max_length=15)
    overview: str
    year: int
    rating: float
    category: str

    class Config:
        schema_extra = {
            "example": {
                "id": 0,
                "title": "Shrek",
                "overview": "movie review",
                "year": 2022,
                "rating": 9.9,
                "category":"kids"
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'La Momia',
        'overview': "El despertar de una antigua momia pone en peligro a todo el mundo ...",
        'year': '2000',
        'rating': 7.8,
        'category': 'Acción'    
    } 

]


# home
@app.get("/", tags=["home"])
def home():
    return HTMLResponse("<h1>Movie API<h1>")

# all movies
@app.get("/movies", tags=["movies"])
def get_movies():
    return movies

# particular movie
@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int = Path(ge = 1, le = 100)):
    for item in movies:
        if item["id"] == id:
            return item
    
    return []

# movies by category
@app.get("/movies/", tags=["movies"])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return [item for item in movies if item["category"] == category and item["title"] == name]

# create a movie
@app.post("/movies", tags=["movies"])
def create_movie(movie: Movie):
    
    movies.append(movie)
    
    return movies

# modificate a movie
@app.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
    
    return movies

# delete a movie
@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id:int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    
    return movies