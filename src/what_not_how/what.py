from what_not_how.dsl_parser import parse_model


if __name__ == '__main__':
    mdl, err_list = parse_model(fname='../../sample_documents/example_process.what')
    # mdl, err_list = parse_model(fname='../../sample_documents/example_2.what')
    # mdl, err_list = parse_model(fname='../../sample_documents/what_not_how.what')
    # mdl, err_list = parse_model(fname='../../sample_documents/ns.what')
    # mdl, err_list = parse_model(fname='../../sample_documents/simple_test.what')

    print("Boom! done.")