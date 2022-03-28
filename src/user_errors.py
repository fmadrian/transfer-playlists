from src.log import Log
"""
define Python user-defined exceptions
    message : Error message
    function: Function that triggered the error
    result:  Error's JSON.
"""

class BaseError(Exception):
    """def __init__(self, message, obj):
        super(Exception).__init__(message)
        self.obj = obj
    """
    def __init__(self, request, response=None, msg=None):
        self.request = request
        self.response = response
        self.msg = msg

    def log_print(self):
        error = None
        if self.msg is None:
            error = "{}:{} {}".format(self.__class__.__name__, self.request, self.response.json())
        else:
            error = "{}:{} {}".format(self.__class__.__name__, self.request, self.msg)
        Log().write_error(error)

# Exceptions generated when we make calls to the Spotify API
class SpotifyError(BaseError):
    def __init__(self, request, response=None, msg=None):
        BaseError.__init__(self, request, response, msg)

# Exceptions generated when we make calls to the Youtube client
class YoutubeError(BaseError):
    def __init__(self, request, response=None, msg=None):
        BaseError.__init__(self, request, response, msg)

# Exceptions generated when we make calls to the Youtube-dl client.
class YoutubeDLError(BaseError):
    def __init__(self, request, response=None, msg=None):
        BaseError.__init__(self, request, response, msg)

# Exceptions related to commands.
class ParamsError(BaseError):
    def __init__(self, request, response=None, msg=None):
        BaseError.__init__(self, request, response, msg)

# Exceptions related to required files.
class RequirementError(BaseError):
    def __init__(self, message, object=None):
        BaseError.__init__(self, message, object)