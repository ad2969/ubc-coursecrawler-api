from rest_framework.response import Response

# allows a function "then_callback" to be called after a response is returned 
class ResponseThen(Response):
    def __init__(self, data, then_callback, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback

    def close(self):
        super().close()
        self.then_callback()

class ResponseError(Exception):
    def __init__(self, statusCode, status, message="Internal error"):
        self.statusCode = statusCode
        self.status = status
        self.message = message
        super().__init__(self.message)
