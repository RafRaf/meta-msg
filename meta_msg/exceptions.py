class BaseMetaMsgError(Exception):
    pass


class DeserializationError(BaseMetaMsgError):
    pass


class ServerError(BaseMetaMsgError):
    def __init__(self, message: str, status_code: int, **kwargs):
        self.message = message
        self.status_code = status_code
        self.exc_info = kwargs
