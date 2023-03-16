class BaseClient:
    def __init__(self):
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }