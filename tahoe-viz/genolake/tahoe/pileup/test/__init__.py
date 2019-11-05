
import os
import unittest


class PileupTestCase(unittest.TestCase):

    def exampleFile(self, file):

        tahoeRoot = os.path.dirname(os.getcwd())
        return os.path.join(os.path.join(tahoeRoot, "example-files"), file)


    def notebookFile(self, file):

        tahoeRoot = os.path.dirname(os.getcwd())
        return os.path.join(os.path.join(tahoeRoot, "tahoe-viz", "examples"), file)


    def dataFile(self, file):

        tahoeRoot = os.path.dirname(os.getcwd())
        return os.path.join(os.path.join(tahoeRoot, "tahoe-viz", "examples", "data"), file)

