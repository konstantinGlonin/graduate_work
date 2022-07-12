from __future__ import annotations

import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from lib.config import Config
from lib.log import logger


class Loader:
    def __init__(self, config: Config) -> None:
        self.config = config.elk
        self.client = None
        self.connect()
        self.check_indexes()

    def connected(self) -> bool:
        return self.client and self.client.ping()

    def connect(self):
        self.close()
        self.client = Elasticsearch(f'http://{self.config.host}:{self.config.port}')

    def close(self):
        if self.connected():
            try:
                self.client.transport.close()
            except Exception:
                pass

        self.client = None

    def check_indexes(self) -> None:
        for index in self.config.indexes:
            if not self.client.indices.exists(index=index):
                self.create_index(index)

    def create_index(self, index_name: str) -> None:
        file = self.config.index_schemas[index_name]
        with open(file) as f:
            schema = json.load(f)
        if not self.connected():
            logger.info('reconnect elastic')
            self.connect()
        self.client.indices.create(index=index_name, **schema)
        logger.info(f"Index '{index_name}' was created")

    def save_data(self, data: list, index_name) -> None:
        if not self.connected():
            logger.info('reconnect elastic')
            self.connect()
        lines, status = bulk(client=self.client,
                             actions=[{"_index": index_name, "_id": i.id, **i.dict()} for i in data])

        logger.info(f"Data migrated to ES {index_name}: {lines} {status}")
