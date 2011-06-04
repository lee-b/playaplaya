from m3u_format import M3UPlaylistFormat
from pls_format import PLSPlaylistFormat
from xspf_format import XSPFPlaylistFormat
from asx_format import ASXPlaylistFormat
import os

class PlaylistManager(object):
    def __init__(self):
        self._handlers = []
        self._handlers.append(M3UPlaylistFormat())
        self._handlers.append(PLSPlaylistFormat())
        self._handlers.append(XSPFPlaylistFormat())
        self._handlers.append(ASXPlaylistFormat())

    def supported_filters(self):
        filters = []
        for h in self._handlers:
            name = h.name()
            exts = h.supported_extensions()
            filters.append( (name,exts) )
        return filters

    def handler_for_filepath(self, fpath):
        basename, ext = os.path.splitext(fpath)
        for h in self._handlers:
            if ext in h.supported_extensions():
                return h
        return None

