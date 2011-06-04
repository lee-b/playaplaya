import urllib

def prettify_uri(uri):
    parts = uri.split('/')
    basename = urllib.unquote(parts[-1])
    basename.replace('_', ' ')
    basename = basename.split('.')[0]
    if len(basename) > 45:
        basename = basename[:21] + "..." + basename[-21:]
    return basename

