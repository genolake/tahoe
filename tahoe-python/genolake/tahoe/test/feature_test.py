
from genolake.tahoe.test import SparkTestCase
from genolake.tahoe.features import *

from genolake.adam.adamContext import ADAMContext


class FeatureTest(SparkTestCase):

    def test_visualize_features(self):
        # load file
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile("smalltest.bed")

        # read features
        features = ac.loadFeatures(testFile)

        featureViz = FeatureSummary(ac, features)

        contig = "chrM"
        start = 1
        end = 2000

        x = featureViz.viewPileup(contig, start, end)
        assert(x != None)
