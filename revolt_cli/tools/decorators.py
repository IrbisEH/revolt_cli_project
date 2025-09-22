from functools import wraps


def log_process(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self.log.debug(f'start process: "{method.__name__}"')
        try:
            return method(self, *args, **kwargs)
        finally:
            self.log.debug(f'end process: "{method.__name__}"')
    return wrapper