from abc import ABC, abstractmethod
class LLMWebSearch(ABC):
    @abstractmethod
    def search(self, url: str):
        pass