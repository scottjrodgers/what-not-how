from what_not_how.dsl_parser import parse_model
from what_not_how.graphs import build_data_flow_graph
from what_not_how.model_processing import post_load_processing
import subprocess


def generate_graph(fname: str):
    mdl, err_list = parse_model(fname)
    post_load_processing(mdl)
    output_basename = fname[:(fname.rfind('.'))]
    build_data_flow_graph(mdl, output_basename)
    subprocess.run(['d2', f"{output_basename}.d2", f"{output_basename}.png"])


if __name__ == "__main__":
    model_file = 'examples/what_not_how/what_not_how.what'
    # model_file = 'examples/optimizer_tool_sample/optimizer.what'
    # model_file = 'examples/node_types_example/node_types.what'
    # model_file = 'examples/cookie_recipe/cookies.what'
    generate_graph(model_file)

    print("Boom! done.")
