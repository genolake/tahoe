
from genolake.tahoe.test import SparkTestCase
from genolake.tahoe.genotypes import *

from genolake.adam.adamContext import ADAMContext


class GenotypesTest(SparkTestCase):

    def test_VariantsPerSampleDistribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile("genodata.v3.test.vcf")

        genotypes = ac.loadGenotypes(testFile)
        _, data = VariantsPerSampleDistribution(self.ss, genotypes).plotDistributions(testMode= True)

        expected = [6, 8, 8, 1, 7, 8]
        assert(sum(data) == sum(expected))


    def test_VariantsPerSampleDistributionSampling(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile("genodata.v3.test.vcf")

        genotypes = ac.loadGenotypes(testFile)
        _, data = VariantsPerSampleDistribution(self.ss, genotypes, sample=0.9).plotDistributions(testMode= True)

        expected = [6, 8, 8, 1, 7, 8]

        # estimated counts should be around real counts
        dev = 8
        assert(sum(expected) > sum(data) - dev and sum(expected) < sum(data) + dev)

    def test_HetHomRatioDistribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile("genodata.v3.test.vcf")

        genotypes = ac.loadGenotypes(testFile)
        _, data =  HetHomRatioDistribution(self.ss, genotypes, sample=1.0).plot(testMode= True)
        expected = sorted([5.0, 0.6, 0.14, 0.17, 1.67])
        sorted_data = sorted(data)

        assert( expected == [ round(x,2) for x in sorted_data ])

    def test_GenotypeCallRatesDistribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile("genodata.v3.test.vcf")

        genotypes = ac.loadGenotypes(testFile)
        _, data =  GenotypeCallRatesDistribution(self.ss, genotypes, sample=1.0).plot(testMode= True)
        expected = sorted([0.95, 0.88, 0.89, 0.94, 0.93, 0.90])
        sorted_data = sorted(data)

        assert( expected == [ round(x,2) for x in sorted_data] )


    def test_GenotypeSummary(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile("genodata.v3.test.vcf")

        genotypes = ac.loadGenotypes(testFile)
        gs =  GenotypeSummary(self.ss, ac, genotypes)

        _, data = gs.getVariantsPerSampleDistribution().plotDistributions(testMode= True)

        expected = [6, 8, 8, 1, 7, 8]
        assert(sum(data) == sum(expected))

    def test_visualize_genotypes(self):
        # load file
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile("genodata.v3.test.vcf")

        # read features
        genotypes = ac.loadGenotypes(testFile)

        gs =  GenotypeSummary(self.ss, ac, genotypes)

        contig = "chr22"
        start = 21079600
        end = 21079700

        x = gs.viewPileup(contig, start, end)
        assert(x != None)

