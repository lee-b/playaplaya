from ConfigParser import ConfigParser
import os

class Conf(object):
    def __init__(self, app_name, *args, **kwargs):
        super(Conf, self).__init__(*args, **kwargs)

        self._conf_dir = os.path.expanduser("~/.config/%s" % app_name)

        from playaplayalib.git_tag import git_tag
        if git_tag == "%d":
            self._app_version = "(development version)"
            self._is_dev = True
        else:
            self._app_version = git_tag
            self._is_dev = False

        if self._is_dev:
            self._conf_fpath = os.path.join(self._conf_dir, "%s_dev.conf" % app_name)
        else:
            self._conf_fpath = os.path.join(self._conf_dir, "%s.conf" % app_name)

        self._cp = ConfigParser()

    def load(self):
        self._cp.read(self._conf_fpath)

    def save(self):
        if not os.path.exists(self._conf_dir):
            os.mkdir(self._conf_dir)
        fp = open(self._conf_fpath, 'wb')
        self._cp.write(fp)
        fp.close()

    def __del__(self):
        self.save()
        super(Conf, self).__del__()

    def get_version(self):
        return self._app_version

    def is_dev_version(self):
        return self._is_dev

    def get_pos(self, playlist, default_fpath):
        playlist = os.path.abspath(playlist)
        if not self._cp.has_section(playlist) or not self._cp.has_option(playlist, 'current_pos'):
            fpath = default_fpath
            pos = 0.0
        else:
            fpath = self._cp.get(playlist, 'current_file')
            pos = self._cp.getfloat(playlist, 'current_pos')
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

