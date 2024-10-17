from typing import List, Dict, Optional
from what_not_how.model_data import (
    Process, DataObject, ModelGroup, DataIdentifier, ModelOptions)

# ------------------------------------------------------
#   Language definitions
# ------------------------------------------------------
group_kw = ['group', 'ns', 'namespace']
group_vars = ['implements']

options_kw = ['options']
options_vars = ['tool', 'title', 'filename', 'svg-name', 'recurse', 'flatten']

process_kw = ['process']
process_vars = ['desc', 'stackable']

data_kw = ['data', 'file', 'concept']
data_vars = ['desc']

id_list_kw = ['input', 'inputs', 'in', 'output', 'outputs', 'out']

str_list_kw = ['note', 'notes',
               # 'description', 'desc', 'descr',
               'assumptions',
               'pre-conditions', 'pre-condition',
               'post-conditions', 'post-condition',
               ]

input_kw = ['in', 'input', 'inputs']
output_kw = ['out', 'output', 'outputs']
notes_kw = ['note', 'notes']
assumption_kw = ['assumptions']
pre_cond_kw = ['preconditions', 'pre-conditions']
post_cond_kw = ['postconditions', 'post-conditions']
# desc_kw = ['desc', 'descr', 'description']


# fields_kw = ['fields', 'columns']


# ------------------------------------------------------
#   Error handling
# ------------------------------------------------------
class ErrorData:
    def __init__(self, message, line, line_no, col_no):
        self.message = message
        self.line = line
        self.line_no = line_no
        self.col_no = col_no


error_list: List[ErrorData] = []


def format_error(error: ErrorData) -> str:
    message = f"{error.line_no:4d}: [{error.line}] -> {error.message}"
    return message


def error_check(condition, message, line, line_no, col_no=None):
    if condition:
        error = ErrorData(message, line.strip(), line_no, col_no)
        error_list.append(error)
        print(format_error(error))
    return condition


def error_assert(condition, message, line, line_no, col_no=None):
    return not error_check(not condition, message, line, line_no, col_no)


# ------------------------------------------------------
#   Lexer / Tokenizer
# ------------------------------------------------------
def index_of_next_space(line, start) -> int:
    if start < 0 or start >= len(line):
        return -1
    special_char = None
    if line[start] in [':', ',']:
        special_char = line[start]
    for i in range(start, len(line)):
        if (not special_char) and line[i] in [' ', ':', ',']:
            return i
        elif special_char and line[i] != special_char:
            return i
    return -1


def index_of_next_non_space(line, start) -> int:
    for i in range(start, len(line)):
        if line[i] != " ":
            return i
    return -1


def next_token(line, start):
    if start < 0:
        return "", -1
    pos_1 = index_of_next_non_space(line, start)
    pos_2 = index_of_next_space(line, pos_1)
    if pos_2 > 0:
        return line[pos_1:pos_2], pos_2
    return line[pos_1:], -1


def smart_tokenize(line: str, line_no) -> List[str]:
    if len(line) < 1:
        return [""]
    if line[0] == "#":
        return [""]

    leading_spaces = 0
    for i in range(len(line)):
        error_check(line[i] == '\t', "Don't use tab characters. Use plain spaces.", line, line_no)
        if line[i] != ' ':
            leading_spaces = i
            break

    line = line.strip()
    tokens = [" " * leading_spaces]
    tok1, pos = next_token(line, 0)

    if len(tok1) > 0:
        # decide next actions based on first token on the line
        tok1 = tok1.lower()
        if tok1 in group_kw or tok1 in process_kw or tok1 in data_kw:
            # we expect an identifier and then maybe a colon, and nothing after a colon
            tokens.append(tok1)
            if error_assert(pos >= 0,
                            f"An identifier is expected after '{tok1}",
                            line, line_no):
                identifier, pos2 = next_token(line, pos)
                tokens.append(identifier)
                if pos2 > 0:
                    tok3, pos3 = next_token(line, pos2)
                    tokens.append(tok3)

                    if pos3 > 0:
                        start = index_of_next_non_space(line, pos3)
                        tok4 = line[start:]
                        tokens.append(tok4)
        elif tok1 in id_list_kw:
            # ID-LISTS, we expect a colon and optional one or more identifiers, separated by a comma if > 1 ident
            tokens.append(tok1)
            if error_assert(pos >= 0,
                            f"A colon is expected after '{tok1}",
                            line, line_no):
                colon, pos2 = next_token(line, pos)
                tokens.append(colon)
                pos3 = pos2
                while pos3 >= 0:
                    tok3, pos3 = next_token(line, pos3)
                    if len(tok3) > 0:
                        tokens.append(tok3)
        elif tok1 in str_list_kw:
            # STR-LISTS, we expect a colon and (if there is anything after the colon) it is a single token
            tokens.append(tok1)
            if not error_check(pos < 0,
                               f"A colon is expected after '{tok1}",
                               line, line_no):
                tok2, pos2 = next_token(line, pos)
                if tok2 == ':':
                    tokens.append(tok2)
                if pos2 > 0:
                    rest_of_line = line[pos2:].strip()
                    if len(rest_of_line) > 0:
                        tokens.append(rest_of_line)
        elif tok1 in options_kw:
            tokens.append(tok1)
            if not error_check(pos < 0,
                               f"A colon is expected after '{tok1}",
                               line, line_no):
                tok2, pos2 = next_token(line, pos)
                if tok2 == ':':
                    tokens.append(tok2)
        elif (tok1 in options_vars or tok1 in group_vars or
              tok1 in process_vars or tok1 in data_vars):
            tokens.append(tok1)
            if not error_check(pos < 0,
                               f"A colon is expected after '{tok1}",
                               line, line_no):
                tok2, pos2 = next_token(line, pos)
                if tok2 == ':':
                    tokens.append(tok2)
                if error_assert(pos2 > 0,
                                "Expecting a value after the colon.",
                                line, line_no):
                    rest_of_line = line[pos2:].strip()
                    tokens.append(rest_of_line)
        else:
            # Not starting with keyword, so whole line is the "token"
            tokens.append(line)
    return tokens


# ------------------------------------------------------
#   Parsing Predicate Functions
# ------------------------------------------------------
def keywords_predicate(keywords):
    return lambda t: t in keywords


def always_predicate(t):
    return True


def make_rule(predicate, action) -> Dict:
    return {'predicate': predicate, 'action': action}


# ------------------------------------------------------
#   Parsing Rule Actions
# ------------------------------------------------------
def group_action(tokens: List[str], node, _context, lines: List[str], line_no: int, this_indent: int):
    # this line is defining a new Model Group
    n_tokens = len(tokens)
    tok1 = tokens[1]
    if error_assert(n_tokens > 3 and tokens[3] == ':',
                    f"A line starting with '{tok1}' should be followed by an identifier and colon",
                    lines[line_no], line_no):
        identifier = tokens[2]
        if error_check(identifier in node.groups,
                       f"Group '{identifier}' is already defined in the current namespace.",
                       lines[line_no], line_no):
            while identifier in node.groups:
                identifier += "'"

        new_group = ModelGroup(identifier, parent=node)
        node.groups[identifier] = new_group
        return parse_group(lines, new_group, new_group, line_no + 1, this_indent)
    return line_no + 1


def options_action(tokens: List[str], node, context, lines: List[str], line_no: int, this_indent: int):
    # options takes place within a group -- often the implied top-level group.  It applies to all sub-groups
    #   where the settings are not overwritten (do I want that?)

    n_tokens = len(tokens)
    tok1 = tokens[1]
    if error_assert(n_tokens > 2 and tokens[2] == ':',
                    f"A line starting with '{tok1}' should be followed by a colon",
                    lines[line_no], line_no):
        new_options = ModelOptions()
        # node remains the current active group
        node.options = new_options
        return parse_options(lines, new_options, node, line_no + 1, this_indent)
    return line_no + 1


def data_action(tokens: List[str], node, context, lines: List[str], line_no: int, this_indent: int):
    # this line is defining a new Data Object
    n_tokens = len(tokens)
    tok1 = tokens[1]
    if error_assert(n_tokens > 2,
                    f"A line starting with '{tok1}' should be followed by an identifier",
                    lines[line_no], line_no):
        identifier = tokens[2]
        if error_check(identifier in node.data_objects,
                       f"Data object '{identifier}' is already defined in the current namespace.",
                       lines[line_no], line_no):
            while identifier in node.data_objects:
                identifier += "'"

        new_data = DataObject(kind=tok1.upper, name=identifier, parent=node)
        node.data_objects[identifier] = new_data
        return parse_data(lines, new_data, context, line_no + 1, this_indent)
    return line_no + 1


def process_action(tokens: List[str], node, context, lines: List[str], line_no: int, this_indent: int):
    # this line is defining a new Process
    n_tokens = len(tokens)
    tok1 = tokens[1]
    if error_assert(n_tokens > 3 and tokens[3] == ':',
                    f"A line starting with '{tok1}' should be followed by an identifier and colon",
                    lines[line_no], line_no):
        identifier = tokens[2]
        if error_check(identifier in node.processes,
                       f"Data object '{identifier}' is already defined in the current namespace.",
                       lines[line_no], line_no):
            while identifier in node.processes:
                identifier += "'"

        new_process = Process(name=identifier, parent=node)
        node.processes[identifier] = new_process
        return parse_process(lines, new_process, context, line_no + 1, this_indent)
    return line_no + 1


def find_or_create_data_object(context, identifier: str) -> DataObject:
    if identifier in context.data_objects:
        return context.data_objects[identifier]
    cur_context = context
    while cur_context.parent is not None:
        if identifier in cur_context.data_objects:
            return context.data_objects[identifier]
        cur_context = cur_context.parent

    # create an "undefined" type identifier
    undefined_data = DataObject(kind='UNDEFINED', name=identifier)
    context.data_objects[identifier] = undefined_data
    return undefined_data


def id_list_action(tokens: List[str], node, context, lines: List[str], line_no: int, this_indent: int):
    # this line is defining a new ID List
    n_tokens = len(tokens)
    tok1 = tokens[1]
    if error_assert(n_tokens > 2 and tokens[2] == ':',
                    f"A line starting with '{tok1}' should be followed by an identifier and colon",
                    lines[line_no], line_no):
        list_name = tokens[1]

        # if a list was already defined, use it -- even though that is unexpected
        if list_name in input_kw:
            target_list = node.inputs
        elif list_name in output_kw:
            target_list = node.outputs
        else:
            error_check(True, "Unknown id_list_type",
                        lines[line_no], line_no)
            target_list = []

        t_idx = 3
        # check for identifier tokens after the colon
        while t_idx < n_tokens:
            identifier_text = tokens[t_idx]
            assert len(identifier_text) > 0
            if identifier_text[-1] == '+':
                optional = False
                stackable = True
                identifier = identifier_text[:-1]
            elif identifier_text[-1] == '*':
                optional = True
                stackable = True
                identifier = identifier_text[:-1]
            elif identifier_text[-1] == '?':
                optional = True
                stackable = False
                identifier = identifier_text[:-1]
            else:
                identifier = identifier_text
                optional = False
                stackable = False

            data_obj: DataObject = find_or_create_data_object(context, identifier)
            target_list.append(DataIdentifier(identifier, data_obj.uid,
                                              optional, stackable))

            t_idx += 1
            if t_idx < n_tokens:
                if error_check(tokens[t_idx] != ',',
                               "If there are multiple identifiers after the colon, they must be " +
                               "separated by commas", lines[line_no], line_no):
                    break
            t_idx += 1
        return parse_id_list(lines, target_list, context, line_no + 1, this_indent)
    return line_no + 1


def str_list_action(tokens: List[str], node, context, lines: List[str], line_no: int, this_indent: int):
    # this line is defining a new String List
    n_tokens = len(tokens)
    tok1 = tokens[1]
    if error_assert(n_tokens > 2 and tokens[2] == ':',
                    f"A line starting with '{tok1}' should be followed by an identifier and colon",
                    lines[line_no], line_no):
        list_name = tokens[1]

        # if a list was already defined, use it -- even though that is unexpected
        if list_name in notes_kw:
            target_list = node.notes
        elif list_name in assumption_kw:
            target_list = node.assumptions
        elif list_name in pre_cond_kw:
            target_list = node.preconditions
        elif list_name in post_cond_kw:
            target_list = node.postconditions
        # elif list_name in desc_kw:
        #     target_list = node.desc
        else:
            error_check(True, "Unknown str_list_type",
                        lines[line_no], line_no)
            target_list = []

        if n_tokens > 3:
            target_list.append(tokens[3])

        return parse_str_list(lines, target_list, context, line_no + 1, this_indent)
    return line_no + 1


def identifiers_action(tokens: List[str], node, context, lines: List[str], line_no: int, this_indent: int):
    # this line is with one or more identifiers
    n_tokens = len(tokens)
    t_idx = 1

    # identifier tokens after the colon
    while t_idx < n_tokens:
        identifier_text = tokens[t_idx]
        assert len(identifier_text) > 0

        if identifier_text[0] == '[' and identifier_text[-1] == ']':
            identifier = identifier_text[1: -1]
            optional = True
        else:
            identifier = identifier_text
            optional = False

        data_obj: DataObject = find_or_create_data_object(context, identifier)
        node.append(DataIdentifier(identifier, data_obj.uid, optional))

        t_idx += 1
        if t_idx < n_tokens:
            if error_check(tokens[t_idx] != ',',
                           "If there are multiple identifiers on a line, they must be " +
                           "separated by commas", lines[line_no], line_no):
                break
        t_idx += 1

    return line_no + 1


def unquoted_string_action(tokens: List[str], node, _context, lines: List[str], line_no: int, this_indent: int):
    # this line is a single unquoted string
    n_tokens = len(tokens)
    error_check(n_tokens > 2, "This line should have a single, unquoted string",
                lines[line_no], line_no)
    node.append(tokens[1])
    return line_no + 1


def setting_action(tokens: List[str], node, _context, lines: List[str], line_no: int, _indent: int):
    # this is for a single-line variable = value statement
    n_tokens = len(tokens)
    error_check(n_tokens != 4 or tokens[2] != ':',
                "This line should have <variable name> : <value>",
                lines[line_no], line_no)
    variable = tokens[1]
    value = tokens[3]

    if variable == 'tool':
        if error_assert(value in ['mermaid', 'd2'],
                        "Tool needs to be either 'mermaid', or 'd2'",
                        lines[line_no], line_no):
            node.tool = value
    elif variable == 'title':
        node.title = value
    elif variable == 'filename':
        node.fname = value
    elif variable == 'svg-name':
        node.sbg_name = value
    elif variable == 'recurse':
        if error_assert(value in ['true', 'false'],
                        "Value can be either 'true' or 'false'.",
                        lines[line_no], line_no):
            node.recurse = (value == 'true')
    elif variable == 'flatten':
        if error_assert(value in ['none', 'all'] or
                        (value.isnumeric() and int(value) >= 0),
                        "Value can be a non-negative integer, 'none', or 'all'",
                        lines[line_no], line_no):
            if value == 'none':
                quantity = 0
            elif value == 'all':
                quantity = 999
            else:
                quantity = int(value)
            node.flatten = quantity
    elif variable == 'implements':
        node.implements = value
    elif variable == 'desc':
        node.desc = value
    elif variable == 'stackable':
        if error_assert(value in ['true', 'false'],
                        "Value can be either 'true' or 'false'.",
                        lines[line_no], line_no):
            node.stackable = (value == 'true')
    else:
        # skipping unknown variable
        pass

    return line_no + 1


# ------------------------------------------------------
#   Central Parsing Functions
# ------------------------------------------------------
def __parse_block(lines: List[str], node, context, start_line: int, start_indent: int, rules: List[Dict]):
    """
    We're parsing a sequence of lines from a model definition file, knowing that our current
    context is that we're in a ModelGroup node.  From this level, our children structures
    will be either additional ModelGroups, or Processes and DataObjects

    Parameters
    ----------
    lines : List[str]
        the master list of lines to be parsed, we'll look at the lines starting at 'start_line'
    node : ModelGroup
        the data structure for this model group that we'll be populating during the parse
    start_line : int
        the line (in the 'lines' list) where we will begin parsing.
    start_indent : int
        The indentation level at the next higher level.  This is used to see if we've properly
        indented, and if we've out-dented, meaning we're done at this level
    rules : List[Dict]
        a list of rules to apply to lines in a priority order.  Once one can be applied, no others
        need be checked.

    Returns
    -------
    int
        The line number of the next line to process in the calling parser

    """
    line_no = start_line
    this_indent = None
    while line_no < len(lines):
        current_line = lines[line_no]
        tokens = smart_tokenize(lines[line_no], line_no)
        tokens = smart_tokenize(lines[line_no], line_no)
        n_tokens = len(tokens)
        if n_tokens <= 1:
            # Skip empty rows
            line_no += 1
            continue
        indent = len(tokens[0])
        if indent <= start_indent:
            # we've "out-dented" and return to the calling parser level
            return line_no
        if this_indent is None:
            this_indent = indent
        error_assert(indent == this_indent, "Detected an unexpected change in indentation",
                     lines[line_no], line_no)

        # attempt to apply the rules one at a time, stopping when one can be applied.
        matched = False
        for rule in rules:
            if rule['predicate'](tokens[1]):
                matched = True
                line_no = rule['action'](tokens, node, context, lines, line_no, this_indent)
                break
        if not matched:
            print(f"Could not match line {line_no}: {lines[line_no]}")
            line_no += 1
    return line_no


# ------------------------------------------------------
#   Parsing Rule Sets
# ------------------------------------------------------
group_rules = [
    make_rule(
        predicate=keywords_predicate(group_kw),
        action=group_action),
    make_rule(
        predicate=keywords_predicate(data_kw),
        action=data_action),
    make_rule(
        predicate=keywords_predicate(process_kw),
        action=process_action),
    make_rule(
        predicate=keywords_predicate(options_kw),
        action=options_action),
    make_rule(
        predicate=keywords_predicate(group_vars),
        action=setting_action),
]

options_rules = [
    make_rule(
        predicate=keywords_predicate(options_vars),
        action=setting_action),
]

process_rules = [
    make_rule(
        predicate=keywords_predicate(id_list_kw),
        action=id_list_action),
    make_rule(
        predicate=keywords_predicate(str_list_kw),
        action=str_list_action),
    make_rule(
        predicate=keywords_predicate(process_vars),
        action=setting_action),
]

data_rules = [
    make_rule(
        predicate=keywords_predicate(str_list_kw),
        action=str_list_action),
    make_rule(
        predicate=keywords_predicate(data_vars),
        action=setting_action),
]

id_list_rules = [
    make_rule(
        predicate=always_predicate,
        action=identifiers_action),
]

str_list_rules = [
    make_rule(
        predicate=always_predicate,
        action=unquoted_string_action),
]


# ---------------------------------------------------------------------------------
#   Specific parsing functions, implemented with the general parse_block function
#   and specific rule sets for the different contexts
# ---------------------------------------------------------------------------------
def parse_group(lines: List[str], node, context, start_line: int = 0, start_indent: int = -1):
    return __parse_block(lines, node, context, start_line, start_indent, group_rules)


def parse_process(lines: List[str], node, context, start_line: int, start_indent: int):
    return __parse_block(lines, node, context, start_line, start_indent, process_rules)


def parse_data(lines: List[str], node, context, start_line: int, start_indent: int):
    return __parse_block(lines, node, context, start_line, start_indent, data_rules)


def parse_id_list(lines: List[str], node, context, start_line: int, start_indent: int):
    return __parse_block(lines, node, context, start_line, start_indent, id_list_rules)


def parse_str_list(lines: List[str], node, context, start_line: int, start_indent: int):
    return __parse_block(lines, node, context, start_line, start_indent, str_list_rules)


def parse_options(lines: List[str], node, context, start_line: int, start_indent: int):
    return __parse_block(lines, node, context, start_line, start_indent, options_rules)


# ------------------------------------------------------
#   Primary external interface
# ------------------------------------------------------
def parse_model(fname: Optional[str] = None, lines: Optional[List[str]] = None):
    """
    parse a functional-process model spec

    Parameters
    ----------
    fname : Optional[str]
    lines : Optional[List[str]]

    Returns
    -------
    model_data.Model
        a collection of process definitions and data objects consumed and produced
    """

    assert fname or lines, "Must provide either fname or lines"
    assert not (fname and lines), "Can't provide both fname and lines"

    if fname:
        with open(fname) as f:
            lines = f.readlines()

    no_cr_lines = [x.replace('\n', '').replace('\r', '') for x in lines]

    # DEBUG
    # for i, line in enumerate(lines):
    #     print(f"{i+1:2d}: {line}")

    model = ModelGroup(None)
    parse_group(no_cr_lines, model, model, 0, -1)

    return model, error_list
