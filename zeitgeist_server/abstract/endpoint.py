from abc import ABC, abstractmethod


class AEndpoints(ABC):

    @abstractmethod
    def print_all(self) -> None:
        pass
