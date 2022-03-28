from genericpath import exists
import json

class FileManager:
    @staticmethod
    def createJSONFile(filename, content):
        try:
            file = open("{}.json".format(filename), "a")
            jsoncontent = json.dumps(content,indent=3)
            file.write(jsoncontent)
        except FileExistsError:
            pass

    @staticmethod
    def checkFileExists(filename):
        return exists(filename)

    # Reads a JSON file and returns an object
    @staticmethod
    def readJSONFile(filename):
        # read file
        with open("{}.json".format(filename), 'r') as jsonfile:
            data=jsonfile.read()
        # parse file
        jsonobject = json.loads(data)
        return jsonobject
