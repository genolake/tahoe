
r"""
========
Variants
========
.. currentmodule:: genolake.tahoe.variants
.. autosummary::
   :toctree: _generate/

   VariantSummary
"""

import genolake.tahoe.pileup as pileup
from genolake.tahoe.pileup.track import *
from genolake.adam.adamContext import ADAMContext
from .utils import *

class VariantSummary(object):
    """ VariantSummary class.
    VariantSummary provides scrollable visualization of variants based on genomic regions.
    """

    def __init__(self, ac, dataset):
        """
        Initializes a GenomicDataset viz class.

        Args:
            :param ac: genolake.adamContext.ADAMContext
            :param dataset: genolake.adam.rdd.VariantDataset
        """
        self.ac = ac
        self.dataset = dataset

    # Takes a genolake.adam.VariantContextRDD and visualizes results
    def viewPileup(self, contig, start, end, reference = 'hg19', label = "Variants", showPlot = True):
        """
        Visualizes a portion of this VariantRDD in a scrollable pileup widget

        Args:
            :param contig: contig of locus to view
            :param start: start position of locus to view
            :param end: end position of locus to view
            reference: genome build. Default is hg19
            label: name of variant track
            showPlot: Disables widget, used for testing. Default is true.

        Returns:
            pileup view for variants
        """
        contig_trimmed, contig_full = formatContig(contig)

        # Filter RDD
        filtered = self.dataset.transform(lambda r: r.filter(((r.referenceName == contig_full) | (r.referenceName == contig_trimmed))
                                                           & (r.start < end) & (r.end > start)))

        # convert to GA4GH JSON to be consumed by tahoe-viz module
        json = self.ac._jvm.org.genolake.tahoe.converters.GA4GHutil.variantDatasetToJSON(filtered._jvmRdd)

        # visualize
        if (showPlot):
            # make variant track
            tracks=[Track(viz="variants", label=label, source=pileup.sources.GA4GHVariantJson(json))]
            locus="%s:%i-%i" % (contig, start, end)
            return pileup.PileupViewer(locus=locus, reference=reference, tracks=tracks)

