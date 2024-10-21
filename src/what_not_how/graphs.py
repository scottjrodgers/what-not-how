"""
What, not How -- Graph generation

Assumptions about how a graph is put together in common tools such as Mermaid and D2:
    1. As is normal, a graph consists of Nodes and Edges
    2. Nodes can have an identifier, used in the definition of the graph, which is separate from the words
       shown on the node in the resulting graph
    3. Edges are defined by the connection of two nodes with some sort of line / arrow.
    4. Edges can also have text associated with the edge.
    5. Multiple edges can occur from the same two nodes
    6. Nodes can have different shapes (Hexagon, rect, circle, and a few others)
    7. Edges can be solid or dashed

Key functionality in the protocol for building a graph definition file / string:
    - Generating necessary header information - styles / overrides / global settings
    - Defining the direction the diagram should flow:  left-to-right, or top-to-bottom
    - Defining a node:  alias, text-in-the-box, shape, (possibly border type -- dashed or not)
    - Adding an edge: "from" and "to" node identifiers, type of line (solid / dashed), any text on the edge

The protocol (from external perspective) is just a single function:
    data ProcessModel:
        note: the top-level data structure of groups, processes, and data objects
    data GraphDefinition:
        notes:
            the definition of the data flow graph for the provided model in the language of one of the applicable
            code-to-diagram tools such as D2 and Mermaid.
    process BuildGraphDefinition:
        input: ProcessModel
        output: GraphDefinition

Or perhaps it's:
    process BuildDataFlowGraph:
        input: ProcessModel
        output: DataFlowDiagram_SVG
"""

from model_data import ModelGroup, Process, DataObject, ModelOptions, DataIdentifier
from typing import List, Tuple


def build_data_flow_graph(mdl: ModelGroup, output_basename: str, debug=False) -> None:
    # tool = get_options(mdl).tool
    # proc_list, obj_list = preprocess_graph_nodes(mdl)
    if mdl.options and mdl.options.tool == "mermaid":
        assert False, "Not fully implemented"
        # build_mermaid_graph(mdl)
    else:
        build_d2_graph(mdl, output_basename)


def get_options(mdl: ModelGroup) -> ModelOptions:
    m = mdl
    while m.options is None and m.parent is not None:
        m = m.parent
    if m.options is not None:
        return m.options
    else:
        return ModelOptions()


def preprocess_graph_nodes(mdl: ModelGroup) -> Tuple[List[Process], List[DataObject]]:
    """
    Collects the processes and data objects to place in the generated graph.  This function handles if the
    graph is to be generated starting at a lower level, or if it will flatten some number of layers

    Parameters
    ----------
    mdl: Model Group
        A collection of processes, data objects, and child model groups.  Together they define a system.

    Returns
    -------
    List[Process], List[DataObject]
        A list of the processes to include in this graph, and a list of data objects to include in this graph
    """
    process_list: List[Process] = []
    data_list: List[DataObject] = []

    max_depth = get_options(mdl).flatten
    collect_and_recurse(mdl, process_list, data_list, max_depth, 0)

    return process_list, data_list


def collect_and_recurse(mdl: ModelGroup,
                        process_list: List[Process],
                        data_list: List[DataObject],
                        max_depth: int = 0,
                        depth: int = 0) -> None:
    for o in mdl.data_objects.values():
        data_list.append(o)
    for p in mdl.processes.values():
        process_list.append(p)
    if depth < max_depth:
        for g in mdl.groups.values():
            collect_and_recurse(g, process_list, data_list, max_depth, depth + 1)


def build_d2_graph(mdl: ModelGroup, output_basename:str, debug=False) -> None:
    """

    Parameters
    ----------
    mdl : ModelGroup
        The top-level data structure for the objects to be encoded into a model

    output_basename : str
        the filename of the input file with the extension stripped off.
    Returns
    -------
    TBD
    """

    with open(f"{output_basename}.d2", "w") as f:
        f.write("vars: { \n")
        f.write("  d2-config: { \n")
        f.write("     theme-id: 1\n")
        f.write("  } \n")
        f.write("}\n")

        # step one: Extract and print out the identifier and text for each node
        for d in mdl.data_objects.values():
            identifier = f"D{d.uid}"
            if d.desc:
                label = d.desc
            else:
                label = d.name
            s = identifier + ": " + label
            f.write(s + "\n")
            if debug:
                print(s)

        for p in mdl.processes.values():
            identifier = f"P{p.uid}"
            if p.desc:
                label = p.desc
            else:
                label = p.name
            s = identifier + ": " + label
            f.write(s + "\n")
            if debug:
                print(s)
            s = f"{identifier}.shape: Hexagon"
            f.write(s + "\n")
            if debug:
                print(s)

            if p.stackable:
                s = f"{identifier}.style.multiple: true"
                f.write(s + "\n")
                if debug:
                    print(s)

        # step two: Extract and print out the information for each edge
        stackable_data = set()
        optional_data = set()
        for p in mdl.processes.values():
            process_id = f"P{p.uid}"
            for a_list, is_input in [(p.inputs, True), (p.outputs, False)]:
                for di in a_list:
                    data_id = f"D{di.identifier_id}"
                    stacked = di.stackable
                    optional = di.optional
                    if stacked:
                        stackable_data.add(data_id)
                    if optional:
                        optional_data.add(data_id)

                    if is_input:
                        s = f"{data_id} -> {process_id}"
                    else:
                        s = f"{process_id} -> {data_id}"
                    if optional:
                        s += " {style: {stroke-dash: 3}}"
                    f.write(s + "\n")
                    if debug:
                        print(s)
        for data_id in stackable_data:
            s = f"{data_id}.style.multiple: true"
            f.write(s + "\n")
            if debug:
                print(s)
        for data_id in optional_data:
            s = f"{data_id}.style.stroke-dash: 3"
            f.write(s + "\n")
            if debug:
                print(s)


# def build_mermaid_graph(mdl: ModelGroup) -> None:
#     """
#
#     Parameters
#     ----------
#     mdl : ModelGroup
#         The top-level data structure for the objects to be encoded into a model
#
#     Returns
#     -------
#     Unknown.
#     - Could be the path to an SVG file generated.
#     - Could be a call to an external tool to bring up the diagram in a browser
#     """
#
#     with open("output.mmd", "w") as f:
#         f.write("graph TB\n")
#
#         # step one: Extract and print out the identifier and text for each node
#         for d in mdl.data_objects.values():
#             identifier = f"D{d.uid}"
#             label = d.name
#             s = identifier + "[" + label + "]"
#             f.write("    " + s + "\n")
#             print(s)
#
#         for p in mdl.processes.values():
#             identifier = f"P{p.uid}"
#             label = p.name
#             s = identifier + "{{" + label + "}}"
#             f.write("    " + s + "\n")
#             print(s)
#
#         # step two: Extract and print out the information for each edge
#         for p in mdl.processes.values():
#             process_id = f"P{p.uid}"
#             for a_list, is_input in [(p.inputs, True), (p.outputs, False)]:
#                 for di in a_list:
#                     data_id = f"D{di.identifier_id}"
#                     if is_input:
#                         s = f"{data_id}-->{process_id}"
#                     else:
#                         s = f"{process_id}-->{data_id}"
#                     f.write("    " + s + "\n")
#                     print(s)
