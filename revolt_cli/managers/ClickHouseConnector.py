from clickhouse_driver import Client


class ClickHouseConnector:
    MAX_BLOCK_SIZE = 100_000

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = Client(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def close(self):
        if self.connection:
            self.connection.disconnect()

    def execute(self, sql, *args, **kwargs):
        return self.connection.execute(sql, *args, **kwargs)

    def execute_iter(self, sql):
        settings = {'max_block_size': self.MAX_BLOCK_SIZE}
        for row in self.connection.execute_iter(sql, settings=settings):
            yield row

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
