from typing import List, Dict, Optional
from what_not_how.model_data import (
    Process,
    DataObject,
    ModelGroup,
    DataIdentifier,
    ModelOptions,
)


def post_load_processing(mdl: ModelGroup) -> None:
    connect_groups_to_implemented_processes(mdl)
    # check_processes_with_same_inputs
    # check_processes_with_same_outputs
    # check_input_output_counts


def connect_groups_to_implemented_processes(mdl: ModelGroup) -> None:
    # connect groups implementing a process to the implemented process
    for group in mdl.groups.values():
        impl_proc = group.implements
        if impl_proc is not None:
            if impl_proc in mdl.processes:
                proc = mdl.processes[impl_proc]
                if proc.implemented_by is None:
                    proc.implemented_by = group
                else:
                    print("Process already implemented")
            else:
                print(f"Implemented process '{impl_proc}' is not defined.")
        # recurse
        connect_groups_to_implemented_processes(group)
