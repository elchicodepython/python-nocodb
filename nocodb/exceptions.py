class NocoDBAPIError(Exception):
    def __init__(self, message, status_code, response_json=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_json = response_json
        self.response_text = response_text
