import os
import re
import sys
from configparser import ConfigParser


class handleFileData():

    path = "."
    rules = []

    def __init__(self):
        print("[init] config.ini init...")
        config = ConfigParser()
        try:
            config.read("config.ini", encoding="utf-8")
            for c in config.options("Rule"):
                self.rules.append(config.get("Rule", c))
        except:
            print("[init:error] config.ini Not Found.")
            sys.exit(0)

    def handle(self, path):

        print("waiting.....")
        handleFiles = []
        if not os.path.isfile(path):
            rootpath = path
            for root, dirs, files in os.walk(path):
                handleFiles.extend([os.path.join(root, f) for f in files])
        else:
            handleFiles.append(path)
            p = path.split(os.sep)
            rootpath = os.sep.join(p[0:len(p)-1])
        for file in handleFiles:
            # rb mode to open, will not has decodeError
            with open(file, "rb") as f:
                try:
                    for content in f:
                        try:
                            # handle decodeError
                            content = content.decode("utf-8")
                        except UnicodeDecodeError as e:
                            # has UnicodeDecodeError data buyao
                            print("[UnicodeDecodeError] ", e)
                            continue
                        hide = False
                        for index, rule in enumerate(self.rules):
                            try:
                                r = re.compile(rule)
                            except re.error as e:
                                print(e)
                                sys.exit(0)
                            if r.search(content.lower()):
                                with open("{}/{}.txt".format(rootpath, index), "a", encoding="utf-8") as fr:
                                    fr.write("{}\n".format(content.strip()))
                                    # print("{}.txt -> {}".format(index, content.strip()), end="\r\n")
                                # has in will break
                                hide = True
                                break
                        if not hide:
                            with open("{}/not_hide.txt".format(rootpath), "a", encoding="utf-8") as fh:
                                fh.write("{}\n".format(content.strip()))
                                # print("not_hide.txt -> {}".format(content.strip()), end="\r\n")

                except UnicodeDecodeError as e:
                    # has UnicodeDecodeError data buyao
                    print(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("usage: python handleFileData.py path")
        sys.exit(0)
    handleFileData = handleFileData()
    handleFileData.handle(sys.argv[1])
    # handleFileData.handle("D:\\tools\\tools\\myDicts\\04 dirDict\\dir.txt")
    pass
