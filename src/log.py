from datetime import datetime
import src.messages as messages
class Log:
    def __init__(self, logname="log"):
        self.logname = logname
        self.create()
    def create(self):
        try:
            file = open("{}.txt".format(self.logname), "x")
            file.close()
            self.write(messages.log["create"])
        except FileExistsError:
            pass
        except Exception as e:
            print(e)

    def write(self, log):
        try:
            log_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            file = open("{}.txt".format(self.logname), "a", encoding='utf-8')
            msg = "[{0}] - {1}\n".format(log_time, log)
            file.write(msg)
            print(msg)
        except FileNotFoundError:
            self.create()
            self.write(log)
        except Exception as e:
            print(e)
        finally:
            file.close()
    def write_error(self, error):
        self.write("{} {}".format("", error))
    def write_info(self, function, info):
        self.write("{} {}".format("", info))
