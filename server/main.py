import httpx
import uvicorn
from fastapi import Body, Depends, FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, Params, paginate
from pydantic import BaseModel, EmailStr, HttpUrl
from starlette.config import Config

config = Config('.env')
API = config('RANDOMUSER_URI')
fields = config('USER_FIELDS')
no_of_users = config('NO_OF_USERS')


class RawUser(BaseModel):
    name: str
    email: EmailStr
    picture: HttpUrl

class User(RawUser):
    id: int
    

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

# CRUD - CREATE, READ, UPDATE, DELETE

@app.post('/create_user', status_code=status.HTTP_201_CREATED)
async def create_user(user_info: RawUser = Body()):
    new_id = max([user.id for user in app.state.users]) + 1
    new_user = User(
        id=new_id,
        name=user_info.name,
        email=user_info.email,
        picture=user_info.picture
    )
    app.state.users.append(new_user)
    return {'message': 'User created'}

@app.patch('/update_user')
async def update_user(user_info: User = Body()):
    index = next((index for index, user in enumerate(app.state.users) if user.id == user_info.id), None)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User doesn\'t exist'
        )
    app.state.users[index] = user_info
    return {'message': 'User updated'}

@app.delete('/delete_user')
async def delete_user(user_id: int):
    index = next((index for index, user in enumerate(app.state.users) if user.id == user_id), None)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User doesn\'t exist'
        )
    app.state.users.pop(index)
    return {'message': 'User deleted'}



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
