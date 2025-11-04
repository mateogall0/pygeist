from pygeist import ZeitgeistAPI, Request

app = ZeitgeistAPI()

async def main_handler(req: Request):
    return f'Hello! We got this: {req.body}'

app.get('/', main_handler, status_code=200)
