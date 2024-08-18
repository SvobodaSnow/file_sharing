class FileInfo:
    def __init__(
            self,
            name_file,
            path_file,
            owner,
            task=None,
            id=None
    ):
        self.id = id
        self.task = task
        self.owner = owner
        self.path_file = path_file
        self.name_file = name_file

    def to_json(self):
        return {
            'id': self.id,
            'task': self.task,
            'owner': self.owner,
            'path_file': self.path_file,
            'name_file': self.name_file
        }


