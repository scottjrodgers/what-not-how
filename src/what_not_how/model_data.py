_next_unique_id: int = 1


class ModelGroup:
    def __init__(self, name=None, parent=None):
        global _next_unique_id
        self.uid = _next_unique_id
        _next_unique_id += 1

        self.name = name
        self.processes = {}
        self.data_objects = {}
        self.groups = {}
        self.parent = parent


class Process:
    def __init__(self, name=None, parent=None):
        global _next_unique_id
        self.uid = _next_unique_id
        _next_unique_id += 1

        self.name = name
        # self.inputs = []
        # self.outputs = []
        self.lists = {}
        self.parent = parent


class DataObject:
    def __init__(self, kind, name=None, parent=None):
        global _next_unique_id
        self.uid = _next_unique_id
        _next_unique_id += 1

        self.name = name
        self.kind = kind
        self.lists = {}
        self.parent = parent


class DataIdentifier:
    def __init__(self, name: str, uid: int, optional=False):
        self.identifier_id = uid
        self.name = name
        self.optional = optional

    def __repr__(self):
        val = f"{self.name}"
        if self.optional:
            val += " (opt)"
        return val
