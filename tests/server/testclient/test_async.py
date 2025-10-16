from pygeist.testclient import TestClient
from tests.fixtures.app_examples.basic import app, zeit_app
import pytest
import asyncio
import time


# @pytest.mark.asyncio
# async def test_async_requests(app):
#     client = TestClient(app)
#     client.link()

#     async def send_req():
#         res = client.get('/async')
#         return res

#     start = time.time()
#     results = await asyncio.gather(send_req(), send_req(), send_req())
#     end = time.time()

#     for r in results:
#         assert r.status_code == 200
#         assert r.body == 'done'

#     final_time = end - start
#     assert final_time < 2
#     client.unlink()
