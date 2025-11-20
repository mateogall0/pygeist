from pygeist.utils.signature import process_signature


def test_process_signature_sync():
    def sync_test(a: int, b: float) -> str:
        return f'{a} {b}'

    params, ret = process_signature(sync_test)

    assert params == {'a': (int, None), 'b': (float, None)}
    assert ret == str

def test_process_signature_async():
    async def async_test(a: int, b: float) -> str:
        return f'{a} {b}'

    params, ret = process_signature(async_test)

    assert params == {'a': (int, None), 'b': (float, None)}
    assert ret == str

def test_process_signature_with_default():
    async def async_test(a: int = 5, b: float = 1.2) -> str:
        return f'{a} {b}'

    params, ret = process_signature(async_test)

    assert params == {'a': (int, 5), 'b': (float, 1.2)}
    assert ret == str
