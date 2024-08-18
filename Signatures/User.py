class User:
    def __init__(self, name, email, division, position, date_employment, id=None):
        self.position = position
        self.date_employment = date_employment
        self.id = id
        self.division = division
        self.email = email
        self.name = name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'division': self.division.to_json(),
            'position': self.position.to_json(),
            'date_employment': self.date_employment
        }





