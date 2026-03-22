import json

class NoSQLStore:
    def __init__(self, db_name="hive_nosql_memory"):
        self.db_name = db_name
        self._store = {}

    def set(self, key, value):
        self._store[key] = json.dumps(value)

    def get(self, key):
        data = self._store.get(key)
        return json.loads(data) if data else None

    def list_all(self):
        result = {}
        for k, v in self._store.items():
            result[k] = json.loads(v)
        return result

agent_nosql_store = NoSQLStore()