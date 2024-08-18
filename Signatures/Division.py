class Division:
    def __init__(self, title, id=None):
        self.id = id
        self.title = title

    def to_json(self):
        return {'id': self.id, 'title': self.title}
