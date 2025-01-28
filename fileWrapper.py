class File_Wrapper:
    def __init__(self, file_name, dir, hash: str):
        self.file_name = file_name
        self.dir = dir
        self.hash = hash
        self.found_similar = False
        pass

    def get_file_name(self):
        return self.file_name
    
    def get_dir(self):
        return self.dir
    
    def set_similar(self):
        self.found_similar = True
    
    def get_similar(self):
        return self.found_similar
    
    def get_hash(self):
        return self.hash
        