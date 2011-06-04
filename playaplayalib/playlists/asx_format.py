from format import PlaylistFormat
from xml.etree import ElementTree
from playaplayalib.book import Book
import os

class ASXPlaylistFormat(PlaylistFormat):
    def name(self):
        return u"ASX Playlists"

    def supported_extensions(self):
        return (
            u'.asx',
        )

    def load_book(self, asx_path):
        base_dir = os.path.dirname(os.path.realpath(asx_path))

        et = ElementTree.parse(asx_path)
        ElementTree.dump(et)
        title = None
        description = None
        entries = et.findall('.//ENTRY')
        uris = []
        for e in entries:
            if not title:
                title = e.findtext('.//TITLE')
            if not description:
                description = title
            refs = e.findall('.//REF')
            for ref in refs:
                uri = ref.attrib['HREF']
                uri = self._absolute_uri(base_dir, uri)
                uris.append(uri)
                print "Appended '%s'" % uri

        cover_image = None
        book = Book(title, uris, description, cover_image)
        return book

if __name__ == "__main__":
    asx = ASXPlaylistFormat()
    asx_book = asx.load_book('tests/playlist.asx')
    print asx_book.get_files()

