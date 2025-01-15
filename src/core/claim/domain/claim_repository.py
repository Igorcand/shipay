from abc import ABC, abstractmethod
from uuid import UUID
from src.core.claim.domain.claim import Claim

class ClaimRepository(ABC):
    @abstractmethod
    def create(self, claim):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Claim | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, claim: Claim) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Claim]:
        raise NotImplementedError