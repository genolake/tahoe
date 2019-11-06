
import unittest
from genolake.tahoe.pileup.test import PileupTestCase

class tahoeVizExampleTest(PileupTestCase):

    def test_notebook_example(self):

        # these variables are read into tahoe-tutorial.py
        bedFile = self.exampleFile("chr17.582500-594500.bed")
        alignmentJsonFile = self.dataFile("alignments.ga4gh.chr17.1-250.json") # TODO
        testMode = True

    # this file is converted from tahoe-python-alignment.ipynb in the Makefile
        pileupFile = self.notebookFile("pileup-tutorial.py")
        exec(open(pileupFile).read())


# Run tests
if __name__ == '__main__':
    unittest.main()
