from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    def get(self, object_id, model):
        pass

    @abstractmethod
    def get_many(self, params, model):
        pass
