from what_not_how.dsl_parser import parse_model
from what_not_how.graphs import build_data_flow_graph
from what_not_how.model_processing import post_load_processing

if __name__ == "__main__":
    # mdl, err_list = parse_model(fname='../../sample_documents/example_process.what')
    # mdl, err_list = parse_model(fname='../../sample_documents/example_2.what')
    # mdl, err_list = parse_model(fname='../../sample_documents/what_not_how.what')
    # mdl, err_list = parse_model(fname='../../sample_documents/ns.what')
    # mdl, err_list = parse_model(fname='../../sample_documents/simple_test.what')
    # mdl, err_list = parse_model(fname='../../sample_documents/example_3_simplified.what')
    # mdl, err_list = parse_model(fname="../../sample_documents/example_3.what")
    # mdl, err_list = parse_model(fname='../../sample_documents/example_3_flattened.what')
    mdl, err_list = parse_model(fname='sample_documents/cookies.what')
    post_load_processing(mdl)

    build_data_flow_graph(mdl)
    print("Boom! done.")
