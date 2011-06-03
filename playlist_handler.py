from book import Book
import os

class PlaylistHandler(object):
    def name(self):
        raise NotImplementedError()

    def supported_extensions(self):
        raise NotImplementedError()

    def load_book(self, filepath):
        raise NotImplementedError()

    def _prettify_fpath(self, fpath):
        basename = os.path.basename(fpath)
        basename.replace('_', ' ')
        basename = basename.split('.')[0]
        return basename

class M3UPlaylistHandler(PlaylistHandler):
    def name(self):
        return u"M3U Playlists"

    def supported_extensions(self):
        return (
            u".m3u",
        )

    def _read_files_from_m3u(self, m3u_path):
        fp = open(m3u_path, 'r')
        lines = fp.readlines()
        lines = [ l.strip() for l in lines ]
        lines = [ l for l in lines if not l.startswith('#') ]
        fp.close()
        fp = None

        name = self._prettify_fpath(m3u_path)

        return lines

    def load_book(self, filepath):
        filelist = self._read_files_from_m3u(filepath)
        title = self._prettify_fpath(filepath)
        description = "A book of %d files" % len(filelist)
        coverimage = None
        book = Book(title, filelist, description, coverimage)
        return book

class PlaylistFormatManager(object):
    def __init__(self):
        self._handlers = []
        self._handlers.append(M3UPlaylistHandler())

    def handler_for_filepath(self, fpath):
        basename, ext = os.path.splitext(fpath)
        for h in self._handlers:
            if ext in h.supported_extensions():
                return h
        return None

