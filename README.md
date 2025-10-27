# Pygeist
Pygeist is a Python module that abstracts the application layer protocol `Zeitgeist` implementation.

[![Tests](https://github.com/mateogall0/pygeist/actions/workflows/tests.yml/badge.svg)](https://github.com/mateogall0/pygeist/actions/workflows/tests.yml)

```bash
.
├── core -> zeitgeist_core
├── adapters
├── pygeist
└── tests
```
## Protocol
See [here](https://github.com/mateogall0/zeitgeist_core) to look into the core implementation of the protocol.

## Build

### Dev requirements
Install the required dev dependencies utilizing the following commands:
```bash
xargs sudo apt-get -y install < packages.txt
pip install -r requirements-dev.txt
```

To build the required Core implementation and Python C API adapters:
```bash
make
```
This generates `pygeist/_adapter.so`.

## Installation
You can also install it utilizing `pip`:
```bash
pip install pygeist
```

## Example

### Create
```python
from pygeist import ZeitgeistAPI, Request

app = ZeitgeistAPI()

async def main_handler(req: Request):
    return f'Hello! We got this: {req.body}'

app.get('/', main_handler, status_code=200)

app.run()
```
