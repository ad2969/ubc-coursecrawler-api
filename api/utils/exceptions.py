class PageError(Exception):
    def __init__(self, message = 'Internal error'):
        self.message = message
        super().__init__(self.message)
