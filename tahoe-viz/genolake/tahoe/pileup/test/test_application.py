
import unittest
import genolake.tahoe.pileup as pileup


class tahoeVizTest(unittest.TestCase):

    def test_genotypes(self):
        track = pileup.Track(viz="genotypes", label="myGenotypes", source=pileup.sources.VcfDataSource('{}'))

        x = pileup.PileupViewer(locus="chr22:21340030-21340150", reference="hg19", tracks=[track])
        assert(x.reference == 'hg19')
        assert(x.tracks[0] == track)

    def test_features(self):
        track = pileup.Track(viz="features", label="myFeatures", source=pileup.sources.GA4GHFeatureJson('{}'))

        x = pileup.PileupViewer(locus="chr17:1-250", reference="hg19", tracks=[track])
        assert(x.reference == 'hg19')
        assert(x.tracks[0] == track)

    def test_variants(self):
        track = pileup.Track(viz="variants", label="myVariants", source=pileup.sources.GA4GHVariantJson('{}'))

        x = pileup.PileupViewer(locus="chr17:1-250", reference="hg19", tracks=[track])
        assert(x.reference == 'hg19')
        assert(x.tracks[0] == track)

    def test_pileup(self):
        track = pileup.Track(viz="pileup", label="myReads", source=pileup.sources.GA4GHAlignmentJson('{}'))

        x = pileup.PileupViewer(locus="chr17:1-250", reference="hg19", tracks=[track])
        assert(x.reference == 'hg19')
        assert(x.tracks[0] == track)

    def test_genes(self):
        track = pileup.Track(viz="genes", label="myGenes", source=pileup.sources.BigBedDataSource('fakeGenes.bb'))

        x = pileup.PileupViewer(locus="chr17:1-250", reference="hg19", tracks=[track])
        assert(x.reference == 'hg19')
        assert(x.tracks[0] == track)

    def test_pileup(self):
        track = pileup.Track(viz="pileup", label="myReads", source=pileup.sources.GA4GHAlignmentJson('{}'))

        x = pileup.PileupViewer(locus="chr17:1-250", reference="hg19", tracks=[track])
        assert(x.reference == 'hg19')
        assert(x.tracks[0] == track)

    def test_genes(self):
        track = pileup.Track(viz="genes", label="myGenes", source=pileup.sources.BigBedDataSource('fakeGenes.bb'))

        x = pileup.PileupViewer(locus="chr17:1-250", reference="hg19", tracks=[track])
        assert(x.reference == 'hg19')
        assert(x.tracks[0] == track)


# Run tests
if __name__ == '__main__':
    unittest.main()
