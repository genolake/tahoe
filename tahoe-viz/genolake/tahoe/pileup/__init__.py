
r"""
===============================
genolake.tahoe.pileup Package
===============================
.. currentmodule:: genolake.tahoe.pileup

Each widget instance calls the `PileupViewer` to draw an interactive widget for genomic data.

.. automodule:: genolake.tahoe.pileup.pileupViewer
.. automodule:: genolake.tahoe.pileup.sources
.. automodule:: genolake.tahoe.pileup.track

"""

from ._version import version_info, __version__
from .pileupViewer import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'pileup',
        'require': 'pileup/extension'
    }]
