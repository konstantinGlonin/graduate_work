from abc import ABC, abstractmethod


class AbstractCache(ABC):
    @abstractmethod
    def get_from_cache(self):
        pass

    @abstractmethod
    def load_to_cache(self):
        pass
