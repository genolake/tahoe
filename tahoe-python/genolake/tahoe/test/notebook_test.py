
from genolake.tahoe.test import SparkTestCase

from genolake.adam.adamContext import ADAMContext


class NotebookTest(SparkTestCase):

    def test_example(self):
        # these variables are read into tahoe-python.py
        spark = self.ss
        testMode = True
        alignmentFile = self.exampleFile("chr17.7500000-7515000.sam")
        variantFile = self.exampleFile("snv.chr17.7502100-7502500.vcf")
        genotypeFile = self.exampleFile("genodata.v3.vcf")
        featureFile = self.exampleFile("chr17.582500-594500.bed")

        # this file is converted from ipynb in make test
        testFile = self.exampleFile("notebooks/tahoe-viz.py")
        exec(open(testFile).read())

    def test_coverage_example(self):
        # these variables are read into tahoe-python.py
        spark = self.ss
        testMode = True
        alignmentFile = self.exampleFile("chr17.7500000-7515000.sam")

        # this file is converted from tahoe-python.coverage.ipynb in the Makefile
        testCoverageFile = self.exampleFile("notebooks/tahoe-python-coverage.py")
        exec(open(testCoverageFile).read())

    def test_alignment_example(self):
        # these variables are read into tahoe-python.py
        spark = self.ss
        testMode = True
        alignmentFile = self.exampleFile("chr17.7500000-7515000.sam")

        # this file is converted from tahoe-python-alignment.ipynb in the Makefile
        testAlignmentFile = self.exampleFile("notebooks/tahoe-python-alignment.py")
        exec(open(testAlignmentFile).read())

    def test_variants_example(self):
        # these variables are read into tahoe-python.py
        spark = self.ss
        testMode = True
        vcfFile = self.exampleFile("genodata.v3.vcf")

        # this file is converted from tahoe-python-alignment.ipynb in the Makefile
        testVariantFile = self.exampleFile("notebooks/tahoe-python-variants.py")
        exec(open(testVariantFile).read())
