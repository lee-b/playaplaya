class Book(object):
    def __init__(self, title, files, description, cover_image_uri):
        self._title = title
        self._files = files
        self._description = description
        self._cover_image_uri = cover_image_uri

    def title(self):
        return self._title

    def get_cover_image_uri(self):
        return self._cover_image_uri

    def next_file(self, current_file_path):
        pass
        
    def prev_file(self, current_file_path):
        pass

    def num_files(self):
        pass

    def file_duration(self, file_path):
        pass

    def get_files(self):
        return self._files

