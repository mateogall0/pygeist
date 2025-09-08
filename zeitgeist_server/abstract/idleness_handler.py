from abc import ABC, abstractmethod


class AIdlenessHandler(ABC):
    def __init__(self,
                 idleness_max_time: int
                 ) -> None:
        self.idleness_max_time = idleness_max_time

    @property
    def idleness_max_time(self) -> int:
        return self._idleness_max_time

    @idleness_max_time.setter
    def idleness_max_time(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise TypeError(
                '`idleness_max_time` must be an int greater than zero'
            )
        self._idleness_max_time = value

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass
