
r"""
========
Coverage
========
.. currentmodule:: genolake.tahoe.coverage
.. autosummary::
   :toctree: _generate/

   CoverageDistribution
"""

import collections
import matplotlib.pyplot as plt
from .distribution import CountDistribution
plt.rcdefaults()

class CoverageDistribution(CountDistribution):
    """ CoverageDistribution class.
    Plotting functionality for visualizing coverage distributions of multi-sample cohorts.
    """

    def __init__(self, ss, coverageDataset, sample = 1.0, bin_size = 10, pre_sampled = False):
        """
        Initializes a CoverageDistribution class.
        Computes the coverage distribution of a CoverageRDD. This RDD can have data for multiple samples.

        Args:
            :param ss: global SparkSession.
            :param coverageRDD: genolake.adam.rdd.CoverageDataset
            :param sample: Fraction to sample CoverageRDD. Should be between 0 and 1

        """

        self.sc = ss.sparkContext
        self.sample = sample
        self.rdd = coverageDataset.toDF().rdd \
            .map(lambda r: ((r["optSampleId"], r["count"] - r["count"]%bin_size), (int(r["end"])-int(r["start"]))))

        CountDistribution.__init__(self)
