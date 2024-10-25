from what_not_how.dsl_parser import parse_model
from what_not_how.graphs import build_data_flow_graph
from what_not_how.model_processing import post_load_processing
import subprocess


def generate_graph(fname: str):
    print(f"Parsing model file: '{fname}'...")
    mdl, err_list = parse_model(fname)
    print("Pre-processing model...")
    post_load_processing(mdl)
    output_basename = fname[:(fname.rfind('.'))]
    print("Building diagram code and resulting image...")
    build_data_flow_graph(mdl, output_basename)
    subprocess.run(['d2', f"{output_basename}.d2", f"{output_basename}.png"])
    print(f"Generated diagram image: {output_basename}.png")


# TASK: Add CLI interface


if __name__ == "__main__":
    diagram = 4

    if diagram == 1 or diagram <= 0:
        model_file = 'examples/what_not_how/what_not_how.what'
        generate_graph(model_file)

    if diagram == 2 or diagram <= 0:
        model_file = 'examples/node_types_example/node_types.what'
        generate_graph(model_file)

    if diagram == 3 or diagram <= 0:
        model_file = 'examples/optimizer_tool_sample/optimizer.what'
        generate_graph(model_file)

    if diagram == 4 or diagram <= 0:
        model_file = 'examples/cookie_recipe/cookies.what'
        generate_graph(model_file)

    print("Boom! done.")
