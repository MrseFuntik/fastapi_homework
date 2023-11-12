from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


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


@app.post("/")
def post_timestamp(json_timestamp: Timestamp):
    global post_db
    time_stamp_ids = []
    for time_stamp in post_db:
        time_stamp_ids.append(time_stamp.id)
    if json_timestamp.id not in time_stamp_ids:
        post_db.append(json_timestamp)
        return json_timestamp
    else:
        raise HTTPException(status_code=422,
                            detail='Validation Error. A Timestamp object with this id already exists')


@app.get('/')
def root():
    return HTMLResponse(
        '''
<h1> Загадка: Ходишь по живым, лежат тихо, ходишь по мёртвым – громко ворчат </h1>
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
<h2> Ответ: <font size="1">
                                                                                                                                                        Опавшие листья 
</font> </h2>

        '''
    )


@app.get("/dog")
def get_dog(kind: str = '') -> str:
    if kind == '':
        dogs_to_return = []
        for i in dogs_db.values():
            dogs_to_return.append(f'Name: {i.name}, primary key: {i.pk}, kind: {str(i.kind)[8:]}')
        return str(dogs_to_return)
    elif kind == 'terrier':
        dogs_to_return = []
        for i in dogs_db.values():
            if i.kind == 'terrier':
                dogs_to_return.append(f'Name: {i.name}, primary key: {i.pk}, kind: {str(i.kind)[8:]}')
        return str(dogs_to_return)
    elif kind == 'dalmatian':
        dogs_to_return = []
        for i in dogs_db.values():
            if i.kind == 'dalmatian':
                dogs_to_return.append(f'Name: {i.name}, primary key: {i.pk}, kind: {str(i.kind)[8:]}')
        return str(dogs_to_return)
    elif kind == 'bulldog':
        dogs_to_return = []
        for i in dogs_db.values():
            if i.kind == 'bulldog':
                dogs_to_return.append(f'Name: {i.name}, primary key: {i.pk}, kind: {str(i.kind)[8:]}')
        return str(dogs_to_return)
    else:
        raise HTTPException(status_code=422,
                            detail='Validation Error. Incorrect kind of dog')


@app.post("/dog")
def create_dog(json_dog: Dog):
    global dogs_db
    primary_keys = []
    for dog in dogs_db.values():
        primary_keys.append(dog.pk)
    if json_dog.pk not in primary_keys:
        dogs_db[json_dog.pk] = Dog(name=json_dog.name, pk=json_dog.pk, kind=json_dog.kind)
    else:
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')


@app.get("/dog/{pk}")
def get_dog_pk(pk: str) -> str:
    global dogs_db

    primary_key = int(pk)
    for dog in dogs_db.values():
        if dog.pk == primary_key:
            return str(f'Name: {dog.name}, primary key: {dog.pk}, kind: {str(dog.kind)[8:]}')
    raise HTTPException(status_code=422,
                        detail='Validation Error. There is no dog with this primary key')


@app.patch("/dog/{pk}")
def get_dog_pk(pk: str, json_dog: Dog) -> str:
    global dogs_db
    primary_key = int(pk)
    for dog in dogs_db.values():
        if dog.pk == primary_key:
            try:
                dog.pk = json_dog.pk
                dog.name = json_dog.name
                dog.kind = json_dog.kind
                return str(f'Name: {dog.name}, primary key: {dog.pk}, kind: {str(dog.kind)[8:]}')
            except:
                raise HTTPException(status_code=422,
                                    detail='Validation Error')
