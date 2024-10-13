import pytest
from fps.fps_parser import *


def _build(inputs, expected):
    return inputs, expected


@pytest.mark.parametrize("input_text, expected", [
    _build("", [""]),
    _build("   ", [""]),
    _build("               ", [""]),
    _build("group", ['', 'group']),
    _build(" group A", [' ', 'group', 'A']),
    _build("  group A:", ['  ', 'group', 'A', ':']),
    _build("   group A:extra", ['   ', 'group', 'A', ':', 'extra']),
    _build("group A: extra info: be aware", ['', 'group', 'A', ':', 'extra info: be aware']),
    _build("ns alpha :  ", ['', 'ns', 'alpha', ':']),
    _build("nas beta   :", ['', 'nas beta   :']),
    _build("namespace gamma:", ['', 'namespace', 'gamma', ':']),
    _build("  process A:", ['  ', 'process', 'A', ':']),
    _build("data A", ['', 'data', 'A']),
    _build("file X", ['', 'file', 'X']),
    _build("  concept Z:", ['  ', 'concept', 'Z', ':']),
    _build("inputs:", ['', 'inputs', ':']),
    _build("input:", ['', 'input', ':']),
    _build("  in  : ", ['  ', 'in', ':']),
    _build("output:", ['', 'output', ':']),
    _build("outputs:", ['', 'outputs', ':']),
    _build("out:", ['', 'out', ':']),
    _build("out: A, B, C", ['', 'out', ':', 'A', ',', 'B', ',', 'C']),
    _build("note:", ['', 'note', ':']),
    _build("notes:", ['', 'notes', ':']),
    _build("description:", ['', 'description', ':']),
    _build("descr:", ['', 'descr', ':']),
    _build("desc:", ['', 'desc', ':']),
    _build("assumptions:", ['', 'assumptions', ':']),
    _build("pre-conditions:", ['', 'pre-conditions', ':']),
    _build("pre-condition:", ['', 'pre-condition', ':']),
    _build("post-conditions:", ['', 'post-conditions', ':']),
    _build("post-condition:", ['', 'post-condition', ':']),
    _build("Not a list: A, B, C", ['', 'Not a list: A, B, C']),
    ])
def test_smart_tokenize(input_text, expected):
    assert smart_tokenize(input_text, 0) == expected


@pytest.mark.parametrize("inputs, expected", [
    _build([" ", 0], 0),
    _build(["", 0], -1),
    _build(["AA ", 1], 2),
    _build(["AAA", 1], -1),
    _build(["      ", 4], 4),
    _build(["BAD", 1], -1),
    _build(["BAD", 2], -1),
    _build(["A, ", 0], 1),
    _build(["B: ", 0], 1),
    _build(["A, ", 1], 2),
    _build(["B: ", 1], 2),
    _build([",: ", 0], 1),
    _build([":, ", 0], 1),
])
def test_index_of_next_space(inputs, expected):
    assert index_of_next_space(inputs[0], inputs[1]) == expected


@pytest.mark.parametrize("inputs, expected", [
    _build(["  A", 0], 2),
    _build([", A", 0], 0),
    _build([", A:", 1], 2),
    _build(["A: ", 0], 0),
    _build(["A: ", 1], 1),
])
def test_index_of_next_non_space(inputs, expected):
    assert index_of_next_non_space(inputs[0], inputs[1]) == expected
