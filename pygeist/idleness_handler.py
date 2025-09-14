from pygeist.abstract.idleness_handler import AIdlenessHandler
from pygeist import _adapter


class IdlenessHandler(AIdlenessHandler):
    def __enter__(self):
        _adapter._init_sessions_structure(
            idle_timeout=self.idleness_max_time,
        )

    def __exit__(self, exc_type, exc_value, traceback):
        _adapter._destroy_sessions_structure()
