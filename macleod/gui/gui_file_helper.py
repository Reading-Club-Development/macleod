class GUI_file_helper():
    def __init__(self):
        self.hashes = dict()
        self.paths = dict()

    def add_path(self, UI_element, path):
        self.paths.update({UI_element : path})

    def update_path(self, UI_element, path):
        self.paths[UI_element] = path

    def get_path(self, UI_element):
        if not self.paths.__contains__(UI_element):
            return None
        return self.paths[UI_element]

    def add_clean_hash(self, text_element, plain_text):
        self.hashes.update({text_element : hash(plain_text)})

    def update_clean_hash(self, UI_element, plain_text):
        self.hashes[UI_element] = hash(plain_text)

    def is_dirty(self, text_element, plain_text):
        if not self.hashes.__contains__(text_element):
            return False
        return self.hashes[text_element] != hash(plain_text)