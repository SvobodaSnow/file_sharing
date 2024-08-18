class Task:
    def __init__(
            self,
            title,
            description,
            status,
            project,
            owner,
            executor,
            reviewers,
            observers,
            time_create,
            time_change,
            time_fulfilment,
            id=None
    ):
        self.reviewers = reviewers
        self.time_fulfilment = time_fulfilment
        self.time_change = time_change
        self.time_create = time_create
        self.observers = observers
        self.executor = executor
        self.owner = owner
        self.project = project
        self.id = id
        self.status = status
        self.description = description
        self.title = title

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.to_json(),
            'project': self.project.to_json(),
            'owner': self.owner.to_json(),
            'executor': self.list_to_json(self.executor),
            'reviewers': self.list_to_json(self.reviewers),
            'observers': self.list_to_json(self.observers),
            'time_create': self.time_create,
            'time_change': self.time_change,
            'time_fulfilment': self.time_fulfilment
        }

    @staticmethod
    def list_to_json(lis):
        new_l = []
        for li in lis:
            new_l.append(li.to_json())
        return new_l








