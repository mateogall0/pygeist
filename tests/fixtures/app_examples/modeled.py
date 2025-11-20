import pytest
from pygeist.exceptions import ZEITException
from pygeist.request import Request
from . import zeit_app
import asyncio
from pydantic import BaseModel
from pygeist.dependency import Depends

@pytest.fixture
def app(zeit_app):
    class UserModel(BaseModel):
        name: str
        age: int


    async def example_depend(req: Request):
        try:
            return float(req.body['update'])
        except Exception as e:
            print(e)
            return 0.0

    async def main():
        return {'name': 'test', 'age': 21}

    async def is_adult(u: UserModel):
        return u.age >= 18

    async def echo_float(value: float):
        return value

    async def is_age_greater(age: int, user: UserModel):
        return age > user.age

    async def echo_float_list(values: list[float]):
        return values

    async def with_depend(example = Depends(example_depend)):
        return example > 0.0

    zeit_app.get('/', main, status_code=200, response_model=UserModel)
    zeit_app.get('/isadult', is_adult, status_code=200)
    zeit_app.get('/echo_float', echo_float, status_code=200)
    zeit_app.get('/is_age_greater', is_age_greater, status_code=200)
    zeit_app.get('/echo_float_list', echo_float_list, status_code=200)
    zeit_app.get('/with_depend', with_depend, status_code=200)

    yield zeit_app
