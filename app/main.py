from typing import Union
from fastapi import FastAPI
from .habi_repository import HabiRepository

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Greetings": "Welcome to habi test",
        "docs": "http://127.0.0.1:8000/docs"
    }

@app.get("/property")
def read_property(year: Union[int, None] = None, city: Union[str, None] = None, status: Union[str, None] = None):
    repository = HabiRepository()
    return repository.getProperty(year, city, status)