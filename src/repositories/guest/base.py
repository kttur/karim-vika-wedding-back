from abc import ABC, abstractmethod

from src.entities.guest import Guest


class BaseGuestRepository(ABC):
    @abstractmethod
    def add(self, guest: Guest) -> None:
        pass

    @abstractmethod
    def list(self) -> list[Guest]:
        pass
