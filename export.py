__author__ = 'swolfod'

import os
import sys
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if PROJECT_DIR not in sys.path:
        sys.path.insert(0, PROJECT_DIR)

    dictDir = os.path.dirname(os.path.abspath(__file__)) + '/dict'

    files = [f for f in listdir(dictDir) if isfile(join(dictDir, f))]

    words = set()

    for file in files:
        if not file.endswith(".dic"):
            continue

        filename = file[:len(file) - 4]

        if len(sys.argv) <= 1 or filename in sys.argv:
            with open(os.path.join(dictDir, file)) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        words.add(line)

    words = list(words)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sogou.dic"), "w") as outFile:
        for word in words:
            outFile.write(word + '\n')