
r"""
=========
Genotypes
=========
.. currentmodule:: genolake.tahoe.genotypes
.. autosummary::
   :toctree: _generate/

   GenotypeSummary
   VariantsPerSampleDistribution
   HetHomRatioDistribution
   GenotypeCallRatesDistribution
"""

import genolake.tahoe.pileup as pileup
from genolake.tahoe.pileup.track import *
from pyspark.sql.functions import col, expr, when

from .utils import *
from .distribution import HistogramDistribution
import matplotlib.pyplot as plt
plt.rcdefaults()

class GenotypeSummary(object):
    """GenotypeSummary class.
    GenotypeSummary provides visualizations for genotype based summaries.
    """

    def __init__(self, spark, ac, genotypeDataset, sample = 1.0):
        """
        Initializes an GenotypeSummary class.

        Args:
            :param spark: SparkSession
            :param ac: genolake.adam.damContext.ADAMContext
            :param genotypeDataset:  genolake.adam.rdd.GenotypeDataset
            :param sample: fraction of reads to sample from
        """

        # sample must be between 0 and 1
        if sample <= 0 or sample > 1:
            raise Exception('sample {} should be > 0 and <= 1'.format(self.sample))

        self.ss = spark
        self.ac = ac
        self.sample = sample
        # sample dataset
        self.genotypeDataset = genotypeDataset

        # where to store collected data
        self.variantsPerSampleDistribution = None
        self.hetHomRatioDistribution = None
        self.genotypeCallRatesDistribution = None

    def getVariantsPerSampleDistribution(self):
        """
        Computes distribution of variant counts per sample.

        Returns:
           VariantsPerSampleDistribution object
        """
        if self.variantsPerSampleDistribution == None:
            print("Computing coverage variants per sample distribution...")
            # pre-sample before computing coverage

            self.variantsPerSampleDistribution = VariantsPerSampleDistribution(self.ss, \
                                                                               self.genotypeDataset, \
                                                                               sample = self.sample)

        return self.variantsPerSampleDistribution

    def getHetHomRatioDistribution(self):
        """
        Computes a distribution of (Heterozygote/Homozygote) ratios per sample

        Returns:
           HetHomRatioDistribution object
        """
        if self.hetHomRatioDistribution == None:
            print("Computing (Heterozygote/Homozygote) ratio distribution")
            self.hetHomRatioDistribution = HetHomRatioDistribution(self.ss, self.genotypeDataset, self.sample)

        return self.hetHomRatioDistribution

    def getGenotypeCallRatesDistribution(self):
        """
        Computes a distribution of variant CallRate (called / total_variants) per sample

        Returns:
           GenotypeCallRatesDistribution object
        """
        if self.genotypeCallRatesDistribution == None:
            print("Computing per sample callrate distribution")
            self.genotypeCallRatesDistribution = GenotypeCallRatesDistribution(self.ss, self.genotypeDataset, self.sample)

        return self.genotypeCallRatesDistribution

    # Takes a genolake.adam.VariantContextRDD and visualizes results
    def viewPileup(self, contig, start, end, reference = 'hg19', label = "Genotypes", showPlot = True):
        """
        Visualizes a portion of this GenotypeRDD in a scrollable pileup widget

        Args:
            :param contig: contig of locus to view
            :param start: start position of locus to view
            :param end: end position of locus to view
            reference: genome build. Default is hg19
            label: name of genotype track
            showPlot: Disables widget, used for testing. Default is true.

        Returns:
            pileup view for genotypes
        """
        contig_trimmed, contig_full = formatContig(contig)

        # Filter dataset
        filtered = self.genotypeDataset.transform(lambda r: r.filter(((r.referenceName == contig_full) | (r.referenceName == contig_trimmed))
                                                           & (r.start < end) & (r.end > start)))

        # convert to GA4GH JSON to be consumed by tahoe-viz module
        json = self.ac._jvm.org.genolake.tahoe.converters.GA4GHutil.genotypeDatasetToJSON(filtered._jvmRdd)

        # visualize
        if (showPlot):
            # make variant track
            tracks=[Track(viz="genotypes", label=label, source=pileup.sources.GA4GHVariantJson(json))]
            locus="%s:%i-%i" % (contig, start, end)
            return pileup.PileupViewer(locus=locus, reference=reference, tracks=tracks)


class VariantsPerSampleDistribution(HistogramDistribution):
    """ VariantsPerSampleDistribution class.
    VariantsPerSampleDistribution computes a distribution of the count of variants per sample.
    """

    def __init__(self, ss, genotypeDataset, sample = 1.0):
        """
        Initializes a VariantsPerSampleDistributionn class.
        Computes the coverage distribution of a CoverageDataset. This dataset can have data for multiple samples.

        Args:
            :param ss: global SparkSession.
            :param genotypeDataset: genolake.adam.rdd.GenotypeDataset
            :param sample: Fraction to sample GenotypeDataset. Should be between 0 and 1
        """

        self.sc = ss.sparkContext
        self.sample = sample

        self.rdd = genotypeDataset.transform(lambda r: r.filter(( (r.alleles[0] == u'ALT') | (r.alleles[1] == u'ALT')))).toDF().rdd \
            .map(lambda r: ((r["sampleId"]), 1))


        HistogramDistribution.__init__(self)

class HetHomRatioDistribution(object):
    """ HetHomRatioDistribution class.
    HetHomRatioDistribution computes a distribution of (Heterozygote/Homozygote) ratios from a genotypeDataset.
    """
    def __init__(self,ss,genotypeDataset, sample = 1.0):
        """
        Initializes HetHomRatioDistribution class.
        Retrieves the call rate and missing rate for each sample in a genotypeDataset

        Args:
            :param ss: global SparkSession.
            :param genotypeDataset: genolake.adam.rdd.GenotypeDataset
            :param sample: Fraction to sample GenotypeDataset. Should be between 0 and 1
        """

        self.sample = sample
        new_col1 = when((col("alleles")[0] == u'REF') & (col("alleles")[1] == u'ALT'),1) \
            .otherwise(when( (col("alleles")[0] == u'ALT') & (col("alleles")[1] == u'ALT'),2))

        genocounts =  genotypeDataset.toDF().sample(False, self.sample) \
            .withColumn("hethomclass", new_col1) \
            .groupBy("sampleid", "hethomclass").count().collect()

        data_het = {}
        data_hom = {}
        for row in genocounts:
            curr = row.asDict()
            if(curr['hethomclass'] == 1):
              data_het[curr['sampleid']] = curr['count']
            if(curr['hethomclass'] == 2):
              data_hom[curr['sampleid']] = curr['count']

        self.hetHomRatio = []
        for sampleid in data_hom.keys():
            if sampleid in data_het.keys():
                self.hetHomRatio.append(float(data_het[sampleid])/float(data_hom[sampleid]))

    def plot(self, testMode = False, **kwargs):
        """
        Plots final distribution values and returns the plotted distribution as a list

        Returns:
          matplotlib axis to plot and computed data
        """

        if(not testMode):
            figsize = kwargs.get('figsize',(10,5))
            fig, ax = plt.subplots(figsize=figsize)
            hist = ax.hist(self.hetHomRatio,bins=100)
            return ax, self.hetHomRatio
        else:
            return None, self.hetHomRatio


class GenotypeCallRatesDistribution(object):
    """ GenotypeCallRatesDistribution class.
    GenotypeCallRatesDistribution computes a distribution of per-sample genotype call rates from a genotypeDataset.
    """
    def __init__(self,ss,genotypeDataset, sample = 1.0):
        """
        Initializes a GenotypeCallRatesDistribution class.
        Retrieves counts of called and missing genotypes from a genotypeDataset.

        Args:
            :param ss: SparkContext
            :param genotypeDataset: genolake.adam.rdd.GenotypeDataset
            :param sample: Fraction to sample GenotypeDataset. Should be between 0 and 1
        """

        self.sample = sample
        new_col1 = when((col("alleles")[0] != u'NO_CALL') ,1) \
            .otherwise(when( (col("alleles")[0] == u'NO_CALL'),2))

        callrateData = genotypeDataset.toDF().sample(False, self.sample) \
               .withColumn("calledstatus", new_col1) \
               .groupBy("sampleid","calledstatus").count().collect()

        data_called = {}
        data_missing = {}
        for row in callrateData:
            curr = row.asDict()
            if(curr['calledstatus'] == 1):
                data_called[curr['sampleid']] = curr['count']
            if(curr['calledstatus'] == 2):
                data_missing[curr['sampleid']] = curr['count']

        self.callRates = []
        for sampleid in data_called.keys():
            count_called = float(data_called.get(sampleid, 0))
            count_missing = float(data_missing.get(sampleid, 0))
            if(count_called > 0):
                callrate = count_called /  ( count_called + count_missing)
                self.callRates.append(callrate)


    def plot(self, testMode = False, **kwargs):
        """
        Plots final distribution values and returns the plotted distribution as a list

        Args:
         :param testMode: if true, does not generate plot. Used for testing.

        Returns:
           matplotlib axis to plot and computed data
        """

        if(not testMode):
            figsize = kwargs.get('figsize',(10,5))
            fig, ax = plt.subplots(figsize=figsize)
            hist = ax.hist(self.callRates,bins=100)
            return ax, self.callRates
        else:
            return None, self.callRates
