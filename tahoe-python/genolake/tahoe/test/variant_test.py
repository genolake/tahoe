
from genolake.tahoe.test import SparkTestCase
from genolake.tahoe.variants import *

from genolake.adam.adamContext import ADAMContext


class VariantTest(SparkTestCase):

    def test_visualize_variants(self):
        # load file
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile("bqsr1.vcf")

        variants = ac.loadVariants(testFile)

        variantViz = VariantSummary(ac, variants)

        contig = "chrM"
        start = 1
        end = 2000

        x = variantViz.viewPileup(contig, start, end)
        assert(x != None)
