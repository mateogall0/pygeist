from zeitgeist_server.utils.singleton import singleton_class
from zeitgeist_server.exceptions import ServerAlreadyStarted
import pytest


@pytest.mark.parametrize("exc_cls", [TypeError, Exception, ServerAlreadyStarted])
def test_singleton_class(exc_cls):
    @singleton_class(exc_cls=exc_cls)
    class ExampleClass:
        pass

    inst = ExampleClass()
    assert inst, 'the __init__ method failed'

    with pytest.raises(exc_cls):
        ExampleClass()
