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
        self.implements = None
        self.options = None


class Process:
    def __init__(self, name=None, parent=None):
        global _next_unique_id
        self.uid = _next_unique_id
        _next_unique_id += 1

        self.name = name
        self.inputs = []
        self.outputs = []
        self.notes = []
        self.pre_conditions = []
        self.post_conditions = []
        self.parent = parent
        self.desc = None
        self.stackable = False


class DataObject:
    def __init__(self, kind, name=None, parent=None):
        global _next_unique_id
        self.uid = _next_unique_id
        _next_unique_id += 1

        self.name = name
        self.kind = kind
        self.notes = []
        self.assumptions = []
        self.fields = []
        self.parent = parent
        self.desc = None


class DataIdentifier:
    def __init__(self, name: str, uid: int,
                 optional=False, stackable=False):
        self.identifier_id = uid
        self.name = name
        self.optional = optional
        self.stackable = stackable

    def __repr__(self):
        val = f"{self.name}"
        if self.optional:
            val += " (opt)"
        return val


class ModelOptions:
    def __init__(self):
        self.tool = 'mermaid'
        self.title = ""
        self.fname = "output"
        self.svg_name = None
        self.recurse = True
        self.flatten = 0
