
r"""
========
Features
========
.. currentmodule:: genolake.tahoe.features
.. autosummary::
   :toctree: _generate/

   FeatureSummary
"""

import genolake.tahoe.pileup as pileup
from genolake.tahoe.pileup.track import *
from genolake.adam.adamContext import ADAMContext
from .utils import *

class FeatureSummary(object):
    """ FeatureSummary class.
    FeatureSummary provides scrollable visualization of features based on genomic regions.
    """

    def __init__(self, ac, dataset):
        """
        Initializes a GenomicRDD viz class.

        Args:
            :param ac: genolake.adam.damContext.ADAMContext
            :param dataset: genolake.adam.rdd.FeatureDataset
        """
        self.ac = ac
        self.dataset = dataset

    # Takes a genolake.adam.FeatureRDD and visualizes results in pileup format
    def viewPileup(self, contig, start, end, reference = 'hg19', label = "Features", showPlot = True):
        """
        Visualizes a portion of this FeatureDataset in a scrollable pileup widget

        Args:
            :param contig: contig of locus to view
            :param start: start position of locus to view
            :param end: end position of locus to view
            reference: genome build. Default is hg19
            label: name of feature track
            showPlot: Disables widget, used for testing. Default is true.

        Returns:
            pileup view for features
        """

        contig_trimmed, contig_full = formatContig(contig)

        # Filter dataset
        filtered = self.dataset.transform(lambda r: r.filter(((r.referenceName == contig_full) | (r.referenceName == contig_trimmed))
                                                           & (r.start < end) & (r.end > start)))

        # convert to GA4GH JSON to be consumed by tahoe-viz module
        json = self.ac._jvm.org.genolake.tahoe.converters.GA4GHutil.featureDatasetToJSON(filtered._jvmRdd)

        # visualize
        if (showPlot):
            # make feature track
            tracks=[Track(viz="features", label=label, source=pileup.sources.GA4GHFeatureJson(json))]
            locus="%s:%i-%i" % (contig, start, end)
            return pileup.PileupViewer(locus=locus, reference=reference, tracks=tracks)


