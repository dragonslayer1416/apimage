class Imagen:
    def __init__(self, id, filename, filedata, filetype) -> None:
        self.id = id
        self.filename = filename
        self.filedata = filedata    
        self.filetype = filetype

    def to_json(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'filedata': self.filedata,
            'filetype': self.filetype
        }

