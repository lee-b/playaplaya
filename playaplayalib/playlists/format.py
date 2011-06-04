from playaplayalib.book import Book
import os
import urllib

class PlaylistFormat(object):
    def name(self):
        raise NotImplementedError()

    def supported_extensions(self):
        raise NotImplementedError()

    def load_book(self, filepath):
        raise NotImplementedError()

    def _file_uri(self, base_dir, fpath):
        if not fpath.startswith('/') and not fpath.startswith('\\'):
            fpath = os.path.join(base_dir, fpath)
        # we don't urlencode the path, since it should be encoded already
        return "file://" + urllib.quote(fpath)

    def _absolute_uri(self, base_dir, uri):
        if ':/' not in uri:
            uri = "file://" + base_dir + "/" + uri
        return uri

