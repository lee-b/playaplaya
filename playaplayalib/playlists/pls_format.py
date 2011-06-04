from format import PlaylistFormat
from ConfigParser import ConfigParser, NoOptionError, NoSectionError
from playaplayalib.book import Book
import os
from playaplayalib.utils import prettify_uri

class PLSPlaylistFormat(PlaylistFormat):
    def name(self):
        return u"PLS Playlists"

    def supported_extensions(self):
        return (
            u".pls",
        )

    def load_book(self, pls_path):
        cp = ConfigParser()
        cp.read(pls_path)

        base_dir = os.path.dirname(os.path.realpath(pls_path))

        try:
            num_files = cp.getint('playlist', 'NumberOfEntries')
        except (NoSectionError, NoOptionError, TypeError), e:
            # not a valid pls file?
            return None

        uris = []
        for i in range(1, num_files):
            try:
                file_path = cp.get('playlist', 'File%d' % i)
#                file_title = cp.get('playlist', 'Title%d' % i)
                uri = self._file_uri(base_dir, file_path)
                uris.append(uri)
            except (NoSectionError, NoOptionError), e:
                # pls appears to be incomplete
                return None

        title = prettify_uri(pls_path)
        description = "A book of %d files" % len(uris)
        coverimage = None
        book = Book(title, uris, description, coverimage)
        return book

