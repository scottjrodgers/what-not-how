from typing import Optional, Dict, List


_next_unique_id: int = 1


class ModelGroup:
    def __init__(self, name=None, parent=None):
        global _next_unique_id
        self.uid = _next_unique_id
        _next_unique_id += 1

        self.name: str = name
        self.processes: Dict[str, Process] = {}
        self.data_objects: Dict[str, DataObject] = {}
        self.groups: Dict[str, ModelGroup] = {}
        self.parent: Optional[ModelGroup] = parent
        self.implements: Optional[str] = None
        self.options: Optional[ModelOptions] = None


class Process:
    def __init__(self, name=None, parent=None):
        global _next_unique_id
        self.uid: int = _next_unique_id
        _next_unique_id += 1

        self.name: int = name
        self.inputs: List[DataIdentifier] = []
        self.outputs: List[DataIdentifier] = []
        self.notes: List[str] = []
        self.pre_conditions: List[str] = []
        self.post_conditions: List[str] = []
        self.parent: Optional[ModelGroup] = parent
        self.desc: Optional[str] = None
        self.stackable: bool = False
        self.implemented_by: Optional[ModelGroup] = None


class DataObject:
    def __init__(self, kind, name=None, parent=None):
        global _next_unique_id
        self.uid: int = _next_unique_id
        _next_unique_id += 1

        self.name: str = name
        self.kind: str = kind
        self.notes: List[str] = []
        self.assumptions: List[str] = []
        self.fields = []  # Not yet used
        self.parent: Optional[ModelGroup] = parent
        self.desc: Optional[str] = None


class DataIdentifier:
    def __init__(
        self, name: str, uid: int, optional: bool = False, stackable: bool = False
    ):
        self.identifier_id: int = uid
        self.name: str = name
        self.optional: bool = optional
        self.stackable: bool = stackable

    def __repr__(self):
        val = f"{self.name}"
        if self.optional:
            val += " (opt)"
        return val


class ModelOptions:
    def __init__(self):
        self.tool: str = "mermaid"
        self.title: str = ""
        self.fname: str = "output"
        self.svg_name: Optional[str] = None
        self.recurse: bool = True
        self.flatten: int = 0
