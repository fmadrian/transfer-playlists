import src.urls as urls
import src.messages as messages
from src.user_errors import ParamsError
class Console:
    def __init__(self, argv):
        self.argv = argv
        self.args = {}

    # Checks that we have the correct amount and type of arguments.
    def check_args(self):
        try:
            if(len(self.argv) == 2):
                if (self.argv[1] == "help" or self.argv[1] == "-h"):
                    print(messages.console["help_msg"])
                    return False
                elif (self.argv[1] == messages.console["liked_videos"]):
                    self.args["playlist_id"] = self.argv[1]
                else:
                    self.args["playlist_id"] = self.check_url(self.argv[1])
                return True
            raise ParamsError("check_args", msg=messages.console["invalid"])
        except ParamsError as e:
            e.log_print()

    # Gets the Youtube playlist url
    def check_url(self, url):
        try:
            identifier = "list="
            id_position = url.find(identifier)
            id_length = len(identifier)
            if(id_position != -1):
                if(url.startswith(urls.youtube["check_playlist"])):
                    playlist_id = url[id_position + id_length:]
                return playlist_id
            raise ParamsError("check_url", msg=messages.console["invalid"])
        except ParamsError as e:
            e.log_print()
        except Exception as e:
            raise e