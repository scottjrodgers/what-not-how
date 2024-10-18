# import pytest
from typing import List
from what_not_how.dsl_parser import parse_model


input_file = """
data X
data W
concept U
process A:
    input: X
    output: W
        U
file C:
    notes: notes on same line
data D:
    notes:
        note 1
        note 2
# skip this comment
process B: extraneous
    input: C, E
    output: D
        F,G, H
"""


def __generate_input_lines() -> List[str]:
    lines = input_file.split("\n")
    if len(lines[0]) == 0:
        lines = lines[1:]
    if len(lines[-1]) == 0:
        lines = lines[:-1]
    for i in range(len(lines) - 1):
        lines[i] += "\n"
    return lines


def test_parse_file():
    line_list = __generate_input_lines()
    mdl, err_list = parse_model(lines=line_list)
    print("asefaseF")
