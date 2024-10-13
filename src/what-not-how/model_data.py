class ModelGroup:
    def __init__(self, name=None):
        self.name = name
        self.processes = {}
        self.data_objects = {}
        self.groups = {}


class Process:
    def __init__(self, name=None):
        self.name = name
        # self.inputs = []
        # self.outputs = []
        self.lists = {}


class DataObject:
    def __init__(self, kind, name=None):
        self.name = name
        self.kind = kind
        self.lists = {}


class DataIdentifier:
    def __init__(self, name, optional=False):
        self.name = name
        self.optional = optional

    def __repr__(self):
        val = f"{self.name}"
        if self.optional:
            val += " (opt)"
        return val
