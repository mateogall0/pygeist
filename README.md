# Pygeist
Pygeist is a Python module that abstracts the application layer protocol `Zeitgeist` implementation.

[![Tests](https://github.com/mateogall0/pygeist/actions/workflows/tests.yml/badge.svg)](https://github.com/mateogall0/pygeist/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

#### Protocol
See [here](https://github.com/mateogall0/zeitgeist_core) to look into the core implementation of the protocol.

```bash
.
├── core -> zeitgeist_core
├── adapters
├── pygeist
└── tests
```

## Installation
This package is available for `pip`:
```bash
pip install pygeist
```

## Quick endpoint example

#### Create
```python
# example.py
from pygeist import ZeitgeistAPI, Request

app = ZeitgeistAPI()

async def main_handler(req: Request):
    return f'Hello! We got this: {req.body}'

app.get('/', main_handler, status_code=200)
```

#### Run
```bash
python3 -m pygeist example:app
```

## Model support
This module utilizes [Pydantic](https://pypi.org/project/pydantic/) for both input and output handling of inputs:
```python
# user.py
from pygeist import Router
from pydantic import BaseModel

class UserModel(BaseModel):
    name: str
    age: int

async def user_main():
    return {'name': 'test', 'age': 21}

async def is_adult(user: UserModel):
    return u.age >= 18

router = Router('/user')
router.get('/', user_main, status_code=200, response_model=UserModel)
router.get('/isadult', is_adult, status_code=200)
```

## Testing
This module implements a `TestClient` allowing for a mock integration of a client interacting with the server.
It is recommended to use the [Pytest](https://pypi.org/project/pytest/) framework:
```python
# tests.py
from pygeist import TestClient
from example import app
import pytest

@pytest.mark.asyncio
async def test_get():
    async with TestCient(app) as client:
        res = await client.get('/')
        assert res.status_code == 200
```

## Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/mateogall0/pygeist/issues) or open a [pull request](https://github.com/mateogall0/pygeist/pulls).

To set up the project locally:

```bash
git clone https://github.com/mateogall0/pygeist
cd pygeist
xargs sudo apt-get -y install < packages.txt
make
pip install -r requirements-dev.txt
pytest
```
