from book import Book
import os
from ConfigParser import ConfigParser, NoOptionError, NoSectionError

class PlaylistFormat(object):
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

    def _fix_filepath(self, base_dir, fpath):
        if fpath.startswith('/') or fpath.startswith('\\'):
            # absolute path; just return it
            return fpath
        else:
            return os.path.join(base_dir, fpath)

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

        lines = [ self._fix_filepath(base_dir, l) for l in lines ]

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

        filelist = []
        for i in range(1, num_files):
            try:
                file_path = cp.get('playlist', 'File%d' % i)
#                file_title = cp.get('playlist', 'Title%d' % i)
                file_path = self._fix_filepath(base_dir, file_path)
                filelist.append(file_path)
            except (NoSectionError, NoOptionError), e:
                # pls appears to be incomplete
                return None

        title = self._prettify_fpath(pls_path)
        description = "A book of %d files" % len(filelist)
        coverimage = None
        book = Book(title, filelist, description, coverimage)
        return book

class PlaylistFormatManager(object):
    def __init__(self):
        self._handlers = []
        self._handlers.append(M3UPlaylistFormat())
        self._handlers.append(PLSPlaylistFormat())

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

