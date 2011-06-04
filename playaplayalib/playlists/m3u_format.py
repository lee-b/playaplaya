from format import PlaylistFormat
from playaplayalib.book import Book
import os
from playaplayalib.utils import prettify_uri

class M3UPlaylistFormat(PlaylistFormat):
    def name(self):
        return u"M3U Playlists"

    def supported_extensions(self):
        return (
            u".m3u",
        )

    def _read_files_from_m3u(self, m3u_path):
        base_dir = os.path.dirname(os.path.realpath(m3u_path))

        fp = open(m3u_path, 'r')
        lines = fp.readlines()
        lines = [ l.strip() for l in lines ]
        lines = [ l for l in lines if not l.startswith('#') ]

        lines = [ self._file_uri(base_dir, l) for l in lines ]

        fp.close()
        fp = None

        name = prettify_uri(m3u_path)

        return lines

    def load_book(self, filepath):
        filelist = self._read_files_from_m3u(filepath)
        title = prettify_uri(filepath)
        description = "A book of %d files" % len(filelist)
        coverimage = None
        book = Book(title, filelist, description, coverimage)
        return book

