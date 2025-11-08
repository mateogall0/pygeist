# Pygeist
Pygeist is a Python module that abstracts the application layer protocol `Zeitgeist` implementation.

[![Tests](https://github.com/mateogall0/pygeist/actions/workflows/tests.yml/badge.svg)](https://github.com/mateogall0/pygeist/actions/workflows/tests.yml)

## Protocol
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

## Build
You can also build it and utilize it from source.
### Dev requirements
Install the required dev dependencies utilizing the following commands:
```bash
xargs sudo apt-get -y install < packages.txt
pip install -r requirements-dev.txt
```

### Compilation
To build the required Core implementation and Python C API adapters:
```bash
make
```
This generates `pygeist/_adapter.so`.

## Example

### Create
```python
# example.py
from pygeist import ZeitgeistAPI, Request

app = ZeitgeistAPI()

async def main_handler(req: Request):
    return f'Hello! We got this: {req.body}'

app.get('/', main_handler, status_code=200)
```

### Run
```bash
python3 -m pygeist example:app
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
