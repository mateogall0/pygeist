from pygeist.utils.signature import process_signature


def test_process_signature_sync():
    def sync_test(a: int, b: float) -> str:
        return f'{a} {b}'

    params, ret = process_signature(sync_test)

    assert params == {'a': int, 'b': float}
    assert ret == str

def test_process_signature_async():
    async def async_test(a: int, b: float) -> str:
        return f'{a} {b}'

    params, ret = process_signature(async_test)

    assert params == {'a': int, 'b': float}
    assert ret == str
