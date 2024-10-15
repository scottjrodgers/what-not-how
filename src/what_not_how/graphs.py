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

from model_data import ModelGroup, Process, DataObject, DataIdentifier


def build_data_flow_graph(mdl: ModelGroup):
    """

    Parameters
    ----------
    mdl : ModelGroup
        The top-level data structure for the objects to be encoded into a model

    Returns
    -------
    Unknown.
    - Could be the path to an SVG file generated.
    - Could be a call to an external tool to bring up the diagram in a browser
    """

    with open("output.mmd", "w") as f:
        f.write("graph TB\n")

        # step one: Extract and print out the identifier and text for each node
        for d in mdl.data_objects.values():
            identifier = f"D{d.uid}"
            label = d.name
            s = identifier + "[" + label + "]"
            f.write("    " + s + "\n")
            print(s)

        for p in mdl.processes.values():
            identifier = f"P{p.uid}"
            label = p.name
            s = identifier + "{{" + label + "}}"
            f.write("    " + s + "\n")
            print(s)

        # step two: Extract and print out the information for each edge
        for p in mdl.processes.values():
            process_id = f"P{p.uid}"
            for a_list, is_input in [(p.inputs, True), (p.outputs, False)]:
                for di in a_list:
                    data_id = f"D{di.identifier_id}"
                    if is_input:
                        s = f"{data_id}-->{process_id}"
                    else:
                        s = f"{process_id}-->{data_id}"
                    f.write("    " + s + "\n")
                    print(s)
