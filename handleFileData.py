import os
import re
import sys
from configparser import ConfigParser


class handleFileData():

    path = "."
    rules = []

    def __init__(self):
        print("[init] config init...")
        config = ConfigParser()
        try:
            config.read("config.ini", encoding="utf-8")
            for c in config.options("Rule"):
                self.rules.append(config.get("Rule", c))
        except:
            print("[init:error] config.ini Not Found.")
            sys.exit(0)

    def handle(self, path):

        handleFiles = []
        if not os.path.isfile(path):
            for root, dirs, files in os.walk(path):
                handleFiles.extend(files)
        else:
            handleFiles.append(path)
        for file in handleFiles:
            with open(file, "r", encoding="utf-8") as f:
                for content in f:
                    # try:
                    #     content = f.readline()
                    # except UnicodeDecodeError as e:
                    #     # has UnicodeDecodeError data buyao
                    #     print(e)
                    hide = False
                    for index, rule in enumerate(self.rules):
                        try:
                            r = re.compile(rule)
                        except re.error as e:
                            print(e)
                            sys.exit(0)
                        if r.search(content):
                            with open("{}.txt".format(index), "a", encoding="utf-8") as fr:
                                fr.write("{}\r".format(content.strip()))
                                print("{}.txt -> {}".format(index, content.strip()))
                            # has in will break
                            hide = True
                            break
                    if not hide:
                        with open("not_hide.txt", "a", encoding="utf-8") as fh:
                            fh.write("{}\r".format(content.strip()))
                            print("not_hide.txt -> {}".format(content.strip()))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # if len(sys.argv) == 1:
    #     print("usage: python handleFileData.py path")
    #     sys.exit(0)
    handleFileData = handleFileData()
    handleFileData.handle(sys.argv[2])
    # handleFileData.handle("D:\\tools\\tools\\myDicts\\04 dirDict\\dir.txt")
    pass
