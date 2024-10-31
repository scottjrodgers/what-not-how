from what_not_how.dsl_parser import parse_model
from what_not_how.diagrams import build_data_flow_graph
from what_not_how.model_processing import post_load_processing
import subprocess
import sys


def generate_graph(fname: str):
    mdl, err_list = parse_model(fname)
    post_load_processing(mdl)
    output_basename = fname[:(fname.rfind('.'))]
    build_data_flow_graph(mdl, output_basename)
    # subprocess.run(['d2', f"{output_basename}.d2", f"{output_basename}.png"])
    subprocess.run(['dot', f"{output_basename}.gv", "-Tpng", "-o", f"{output_basename}.png"])


def main(argv):
    if len(argv) < 2:
        print("What, not How")
        print("A DSL for coding a data-flow or process diagram.\n")
        print("Usage:  what <model-file>\n")
        sys.exit(1)
    else:
        model_file = argv[1]
    generate_graph(model_file)


if __name__ == "__main__":
    main(sys.argv)

    # model_file = 'examples/what_not_how/what_not_how.what'
    # model_file = 'examples/optimizer_tool_sample/optimizer.what'
    # model_file = 'examples/node_types_example/node_types.what'
    # model_file = 'examples/simple/simple.what'
    # model_file = 'examples/cookie_recipe/cookies.what'

    # print("Boom! done.")
