from typing import Optional, Dict, List
from pydantic import BaseModel, Field


_next_unique_id: int = 1


def get_uid() -> int:
    global _next_unique_id
    my_id = _next_unique_id
    _next_unique_id += 1
    return my_id


class ModelGroup (BaseModel):
    uid: int = Field(default_factory=get_uid)
    name: str
    processes: Dict[str, 'Process'] = {}
    data_objects: Dict[str, 'DataObject'] = {}
    groups: Dict[str, 'ModelGroup'] = {}
    parent: Optional['ModelGroup'] = None
    implements: Optional[str] = None
    options: Optional['ModelOptions'] = None


class DataObject (BaseModel):
    uid: int = Field(default_factory=get_uid)
    name: str
    kind: str
    notes: List[str] = []
    assumptions: List[str] = []
    fields: List[str] = []
    parent: Optional[ModelGroup] = None
    desc: Optional[str] = None


class Process (BaseModel):
    uid: int = Field(default_factory=get_uid)
    name: str
    inputs: List['DataIdentifier'] = []
    outputs: List['DataIdentifier'] = []
    notes: List[str] = []
    assumptions: List[str] = []
    pre_conditions: List[str] = []
    post_conditions: List[str] = []
    parent: Optional[ModelGroup] = None
    desc: Optional[str] = None
    stackable: bool = False
    implemented_by: Optional[ModelGroup] = None


class DataIdentifier (BaseModel):
    name: str
    identifier_id: int
    optional: bool
    stackable: bool


class ModelOptions (BaseModel):
    tool: str = "d2"
    title: str = ""
    fname: str = "output"
    recurse: bool = True
    flatten: int = 0


ModelGroup.model_rebuild()
Process.model_rebuild()
