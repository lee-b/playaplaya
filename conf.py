from ConfigParser import ConfigParser
import os

class Conf(object):
    def __init__(self, app_name, *args, **kwargs):
        super(Conf, self).__init__(*args, **kwargs)

        self._conf_dir = os.path.expanduser("~/.config/%s" % app_name)
        self._conf_fpath = os.path.join(self._conf_dir, "%s.conf" % app_name)

        self._cp = ConfigParser()

    def load(self):
        self._cp.read(self._conf_fpath)
        print "Conf loaded"

    def save(self):
        if not os.path.exists(self._conf_dir):
            os.mkdir(self._conf_dir)
        fp = open(self._conf_fpath, 'wb')
        self._cp.write(fp)
        fp.close()

    def __del__(self):
        self.save()
        super(Conf, self).__del__()

    def get_pos(self, playlist, default_fpath):
        playlist = os.path.abspath(playlist)
        if not self._cp.has_section(playlist) or not self._cp.has_option(playlist, 'current_pos'):
            fpath = default_fpath
            pos = 0.0
        else:
            fpath = self._cp.get(playlist, 'current_file')
            pos = self._cp.getfloat(playlist, 'current_pos')
        print "Loaded position for %s: %s @ %f" % (playlist, fpath, pos)
        return fpath, pos

    def get_playlist(self):
        if self._cp.has_section('global'):
            return self._cp.get('global', 'last_playlist')
        else:
            return None

    def set_playlist(self, playlist):
        playlist = os.path.abspath(playlist)

        if not self._cp.has_section('global'):
            self._cp.add_section('global')

        self._cp.set('global', 'last_playlist', playlist)

    def set_pos(self, playlist, fpath, pos):
        playlist = os.path.abspath(playlist)

        if not self._cp.has_section(playlist):
            self._cp.add_section(playlist)

        self._cp.set(playlist, 'current_file', fpath)
        self._cp.set(playlist, 'current_pos', pos)
        print "Save pos for %s: %s @ %f" % (playlist, fpath, pos)

