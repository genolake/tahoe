
r"""
============
PileupViewer
============
.. currentmodule:: genolake.tahoe.pileup.pileupViewer
.. autosummary::
   :toctree: _generate/

   PileupViewer
"""

import ipywidgets as widgets
from traitlets import Unicode, Int, List
from .track import Track, track_list_serialization

@widgets.register('genolake.tahoe.pileup.PileupViewer')
class PileupViewer(widgets.DOMWidget):
    """ Widget wrapper for pileup.js viewer in Jupyter notebooks.
    """

    _view_name = Unicode('PileupViewerView').tag(sync=True)
    _model_name = Unicode('PileupViewerModel').tag(sync=True)
    _view_module = Unicode('pileup').tag(sync=True)
    _model_module = Unicode('pileup').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    # locus with placeholder
    locus=Unicode('chr1:1-50').tag(sync=True)
    # string of reference genome.
    reference = Unicode('hg19').tag(sync=True)
    # Array of track elements
    tracks = List(Track()).tag(sync=True, **track_list_serialization)

