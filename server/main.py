import httpx
from pydantic import BaseModel, EmailStr, HttpUrl
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.config import Config
from fastapi_pagination import Page, Params, paginate

config = Config('.env')
API = config('RANDOMUSER_URI')
fields = config('USER_FIELDS')
no_of_users = config('NO_OF_USERS')


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    picture: HttpUrl


def get_data():
    response = httpx.get(f'{API}?inc={fields}&results={no_of_users}')
    return response.json()['results']


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def start_up():
    raw_users = get_data()
    users = []
    for id, raw_user in enumerate(raw_users):
        users.append(
            User(
                id=id,
                name=f"{raw_user['name']['first']} {raw_user['name']['last']}",
                email=raw_user['email'],
                picture=raw_user['picture']['medium']
            )
        )
    app.state.users = users


@app.get('/')
async def home():
    return {'message': 'Hello👋 Jr. Devs!! Let\'s code together 💻🖱'}


@app.get('/users', response_model=Page[User])
async def get_users(
    params: Params = Depends()
):
    return paginate(app.state.users, params)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
