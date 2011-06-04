from format import PlaylistFormat
from xml.etree import ElementTree
from playaplayalib.book import Book
import os

class XSPFPlaylistFormat(PlaylistFormat):
    def name(self):
        return u"XSPF Playlists"

    def supported_extensions(self):
        return (
            u'.xspf',
        )

    def load_book(self, xspf_path):
        base_dir = os.path.dirname(os.path.realpath(xspf_path))

        namespace="http://xspf.org/ns/0/"
        et = ElementTree.parse(xspf_path)
        title = et.findtext('.//{%s}title' % namespace)
        tracks = et.findall('.//{%s}track' % namespace)
        locations = [ t.find('.//{%s}location' % namespace) for t in tracks ]
        uris = [ l.text for l in locations ]
        uris = [ self._absolute_uri(base_dir, u) for u in uris ]
        description = et.findtext('{ns0}info')
        cover_image = None
        book = Book(title, uris, description, cover_image)
        return book

if __name__ == "__main__":
    xspf = XSPFPlaylistFormat()
    xspf_book = xspf.load_book('tests/playlist.xspf')
    print xspf_book.get_files()

