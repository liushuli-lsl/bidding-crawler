

class RequestException(IOError):
    """There was an ambiguous exception that occurred while handling your
    request.
    """

    def __init__(self, *args, **kwargs):
        """Initialize RequestException with `request` and `response` objects."""
        response = kwargs.pop('response', None)
        self.response = response
        self.request = kwargs.pop('request', None)
        if (response is not None and not self.request and
                hasattr(response, 'request')):
            self.request = self.response.request
        super(RequestException, self).__init__(*args, **kwargs)

class ForbiddenError(RequestException):
    """发生 HTTP 403 错误."""

class InvalidRequest(RequestException):
    """发生 HTTP 400 错误."""

class ServiceUnavailableError(RequestException):
    """发生 HTTP 503 错误."""
