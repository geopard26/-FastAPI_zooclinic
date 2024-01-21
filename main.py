from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, HTTPException

app = FastAPI()

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"

class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType

class Timestamp(BaseModel):
    id: int
    timestamp: int

dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

@app.get('/', response_model=str)
def root():
    return "Hello, World!"

@app.get('/post', response_model=List[Timestamp], summary='Get Posts')
def get_posts():
    return post_db

@app.post('/post', response_model=Timestamp, summary='Create Post')
def create_post():
    new_id = post_db[-1].id + 1 if post_db else 0
    new_timestamp = post_db[-1].timestamp + 1 if post_db else 0
    new_post = Timestamp(id=new_id, timestamp=new_timestamp)
    post_db.append(new_post)
    return new_post

@app.get('/dog', response_model=List[Dog], summary='Get Dogs')
def get_dogs(kind: Optional[DogType] = None):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())

@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    if not isinstance(dog.pk, int):
        raise HTTPException(status_code=400, detail='PK must be an integer.')
    if dog.pk in dogs_db:
        raise HTTPException(status_code=409, detail='The specified PK already exists.')
    dogs_db[dog.pk] = dog
    return dog

@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By Pk')
def get_dog(pk: int):
    dog = dogs_db.get(pk)
    if dog is None:
        raise HTTPException(status_code=404, detail='Dog not found.')
    return dog

@app.patch('/dog/{pk}', response_model=Dog, summary='Update Dog')
def update_dog(pk: int, updated_dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail='Dog not found.')
    dogs_db[pk] = updated_dog
    return updated_dog