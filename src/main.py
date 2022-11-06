from typing import List

from fastapi import FastAPI, HTTPException

from src.db.connection import db_connection
from src.queries.recipe_table import Recipe
from src.serializers.recipe import RecipeGetter, RecipeSetter

app = FastAPI()

recipe_module = Recipe(db_connection)


@app.get("/")
def welcome():
    return {"message": "Hello world!"}

@app.get("/health")
def get_health():
    return {"message": "Hello world!"}

@app.get("/count")
def count_records():
    return {""}