import abc
import json
import os
from typing import Any

from redis import Redis


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def flush(self) -> None:
        """Очистить содержимое хранилища"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: Redis):
        self.redis_adapter = redis_adapter
        self.retrieve_state()

    def save_state(self, state: dict) -> None:
        self.redis_adapter.set('data', json.dumps(state))

    def retrieve_state(self) -> dict:
        data = self.redis_adapter.get('data')
        if data is not None:
            return json.loads(data)
        return {}

    def flush(self) -> None:
        self.redis_adapter.flushdb()


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str | None = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(state, f)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, 'r') as f:
                state = json.load(f)
            return state
        except Exception:
            return {}

    def flush(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def copy_state(self, src_key: str, dst_key: str) -> None:
        """Скопировать значение ключа"""
        data = self.storage.retrieve_state()
        data[dst_key] = data[src_key]
        self.storage.save_state(data)

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        data = self.storage.retrieve_state()
        data[key] = value
        self.storage.save_state(data)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        data = self.storage.retrieve_state()
        if key in data:
            return data[key]
        return None

    def clear_state(self) -> None:
        self.storage.flush()
