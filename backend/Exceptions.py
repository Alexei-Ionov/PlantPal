class InvalidInputError(Exception):
    pass
class InvalidPassword(Exception):
    pass
class APIFail(Exception):
    pass
class JsonException(Exception):
    def __init__(self, error_info):
        self.error_info = error_info
        super().__init__(str(error_info))