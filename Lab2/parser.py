import itertools

from function import write_output_to_file
from main import lexer
from constants import data_types, keywords, standart_libraries, operators
import re

pattern = r'\((.*?)\)'
numbers = r'\d+'
commas = r','
semicolon = r';'

variable_types = {}
variable_scope = []

def check_variable(token_type, token, data_type):
    if 'VARIABLE' in token_type:
        variable_name = token
        variable_node = Node(data_type, variable_name)
        data_type = None
        variable_name = None
        return variable_node


def check_comma(token, current_node):
    if token == ',':
        comma_node = Node(",", "Comma")
        current_node.add_child(comma_node)

        return comma_node


def check_chto(token, current_node):
    if token == ';':
        chto_node = Node(token, "Chto")
        # current_node.add_child(data_list_node)  # Добавляем data_list_node в текущий узел
        current_node.add_child(chto_node)

        return chto_node


def check_comparison(token, current_node):
    comparison_node = ComparisonNode(token, "Comparison")
    current_node.add_child(comparison_node)
    return comparison_node


class Node:
    def __init__(self, name, node_type, data_type=None, array_in=None, parent=None, children=None):
        self.name = name
        self.type = node_type
        self.data_type = data_type
        self.array_in = array_in
        self.parent = parent
        self.children = children if children is not None else []

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def get_last_child(self):
        if self.children:
            return self.children[-1]
        else:
            return None


    def display(self, level=0):
        indent = "    " * level
        tree_structure = ""
        if self.data_type is not None and self.array_in is not None:
            tree_structure += f"{indent}|- {self.type}: {self.data_type} {self.name}[{self.array_in}]\n"
        if self.data_type is None and self.array_in is None:
            tree_structure += f"{indent}|- {self.type}: {self.name}\n"
        elif self.array_in is None:
            tree_structure += f"{indent}|- {self.type}: {self.data_type} {self.name}\n"
        elif self.data_type is None:
            tree_structure += f"{indent}|- {self.type}: {self.name}[{self.array_in}]\n"

        for child in self.children:
            tree_structure += child.display(level + 1)

        return tree_structure


class PreprocessorDirectiveNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)


class StatementNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)


class ClassNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)


class CommentNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)


class ForNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)


class IfNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)

class ElseNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)


class IfElseNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)


class WhileNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)


class ComparisonNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)

class AssignmentNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)

class ValueNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)


def find_chars_between(text, start_char, end_char):
    found_chars = []
    started = False

    for char in text:
        if char == start_char:
            started = True
            continue
        elif char == end_char:
            break

        if started:
            found_chars.append(char)

    return ' '.join(found_chars)

def build_syntax_tree(tokens):
    root = Node("Program", "ProgramType")
    current_node = root

    function_definitions = {}
    branch_stack = []
    square_stack = []
    param_stack = []
    bracket_stack = []
    include_stack = []
    access_stack = []
    data_stack = []
    variable_stack = []
    io_stack = []
    if_stack = []
    return_stack = []
    class_stack = []
    function_stack = []
    std_stack = []
    for_stack = []

    is_string_declaration = False
    is_value = False
    inside_comment = False
    is_array_declaration = False

    array_name = None
    data_type = None

    current_comment = ""

    for token, token_type, line in tokens:
        if token in data_types:
            data_stack.append(token)

        if token == "//":
            continue

        if token == "/*":
            inside_comment = True
            current_comment += token[2:] + " "
            continue
        elif token == "*/":
            inside_comment = False
            comment_node = CommentNode(current_comment[:-1], "Comment")
            current_node.add_child(comment_node)
            current_comment = ""
            continue
        elif inside_comment:
            current_comment += token + " "
            continue

        if 'VARIABLE' in token_type or 'POINTER' in token_type:
            if len(data_stack) != 0:
                variable_already_exists = any(child.name == token for child in current_node.children)
                if variable_already_exists:
                    semantic_error_node = Node(token,
                                                 f'Semantic error! Variable "{token}" has already been declared.')
                    current_node.add_child(semantic_error_node)
                    break
                variable_types[token] = data_stack[-1]
                if data_stack[-1] == 'STRING':
                    is_string_declaration = True
                if len(variable_scope) != 0:
                    temp_scope = False
                    for var, scope in variable_scope:
                        temp_parent_node = current_node.parent
                        if token == var and temp_parent_node.name == scope:
                            semantic_error_node = Node(token,
                                                       f'Semantic error! Variable "{token}" has already been declared.')
                            current_node.add_child(semantic_error_node)
                            temp_scope = True
                    if temp_scope:
                        break
                variable_node = Node(token, 'Declare', data_stack[-1].lower())
                data_stack.pop()
                is_value = True
            else:
                if token not in variable_types:
                    first_children = current_node.children[-1]
                    second_children = current_node.children[-2]

                    if first_children.type == 'Comma':
                        print('True')
                        if second_children.type == 'Declare':
                            variable_node = Node(token, 'Declare', second_children.data_type)
                            variable_types[token] = second_children.data_type

                else:
                    is_string_declaration = False
                    variable_node = Node(token, 'Variable', variable_types.get(token))
                    is_value = True

            temp_parent_node = current_node.parent
            variable_scope.append((token, temp_parent_node.name))

            variable_stack.append(current_node)
            current_node.add_child(variable_node)
            current_node = variable_node
            parent_node = current_node.parent

            semicolon_present = False
            for tok, _, ln in tokens:
                if ln == line and tok == ";" and parent_node.type in (
                        'ProgramType', 'Block', 'Declare', 'AccessModifier', 'ReturnStatement') or parent_node.type in (
                        'Parameters', 'Function', 'Function Call','Colon', 'Variable', 'Operator Input', 'Array', 'Square Block'):
                    semicolon_present = True
                    break

            if not semicolon_present:
                syntax_error_node = Node(f"Semicolon missing after variable declaration.",
                                         f'Syntax error!')
                current_node.add_child(syntax_error_node)
                break

        if 'ARRAY' in token_type:
            if len(data_stack) != 0:
                array_already_exists = any(child.name == token for child in current_node.children)
                if array_already_exists:
                    semantic_error_node = Node(token,
                                                 f'Semantic error! Variable "{token}" has already been declared.')
                    current_node.add_child(semantic_error_node)
                    break
                variable_types[token] = data_stack[-1]
                if data_stack[-1] == 'STRING':
                    is_string_declaration = True
                if len(variable_scope) != 0:
                    temp_scope = False
                    for var, scope in variable_scope:
                        temp_parent_node = current_node.parent
                        if token == var and temp_parent_node.name == scope:
                            semantic_error_node = Node(token,
                                                       f'Semantic error! Variable "{token}" has already been declared.')
                            current_node.add_child(semantic_error_node)
                            temp_scope = True
                    if temp_scope:
                        break
                variable_node = Node(token, 'Declare Array', data_stack[-1].lower())
                data_stack.pop()
                is_value = True
            else:
                is_string_declaration = False
                variable_node = Node(token, 'Array', variable_types.get(token))
                is_value = True

            if current_node.parent:
                temp_parent_node = current_node.parent
                variable_scope.append((token, temp_parent_node.name))
            else:
                variable_scope.append((token, current_node.name))

            variable_stack.append(current_node)
            current_node.add_child(variable_node)
            current_node = variable_node
            parent_node = current_node.parent

            semicolon_present = False
            for tok, _, ln in tokens:
                if ln == line and tok == ";" and parent_node.type in (
                        'ProgramType', 'Block', 'Declare', 'AccessModifier', 'ReturnStatement') or parent_node.type in (
                        'Parameters', 'Function', 'Function Call','Colon', 'Operator Input', 'Variable', 'Array'):
                    semicolon_present = True
                    break

            if not semicolon_present:
                syntax_error_node = Node(f"Semicolon missing after variable declaration.",
                                         f'Syntax error!')
                current_node.add_child(syntax_error_node)
                break

        if token == '[':
            square_node = Node(current_node.name, 'Square Block')
            square_stack.append(current_node)
            current_node.add_child(square_node)
            current_node = square_node

        if token == ']':
            if current_node.type == 'Square Block':
                temp_list = []
                temp_list.extend(current_node.children)
                semantic_error = False
                for i in temp_list:
                    if i.data_type != 'int':
                        semantic_error = True
                if semantic_error:
                    semantic_error_node = Node(token, 'Semantic error! In array')
                    current_node.add_child(semantic_error_node)
                    break
            current_node = square_stack.pop()

        if token == "#include":
            preprocessor_directive_node = PreprocessorDirectiveNode(token, "PreprocessorDirective")
            include_stack.append(current_node)
            current_node.add_child(preprocessor_directive_node)
            current_node = preprocessor_directive_node

        if token in standart_libraries or token_type == 'HEADER FILE':
            header_file_node = Node(token, 'Header file')
            current_node.add_child(header_file_node)
            current_node = include_stack.pop()

        if token_type == "CLASS":
            class_node = ClassNode(token, "Class")
            class_stack.append(current_node)
            current_node.add_child(class_node)
            current_node = class_node

        if 'FUNCTION' in token_type:
            if len(data_stack) != 0:
                function_already_exists = any(child.name == token for child in current_node.children)
                if function_already_exists:
                    semantic_error_node = Node(token,
                                               f'Semantic error! Variable "{token}" has already been declared.')
                    current_node.add_child(semantic_error_node)
                    break
                function_node = Node(token, 'Function', data_stack[-1].lower())
                data_stack.pop()
            else:
                function_node = Node(token, 'Function Call', None)

            function_stack.append(current_node)
            current_node.add_child(function_node)
            current_node = function_node

        if 'OBJECT OF' in token_type:
            object_node = Node(token, 'Object')
            param_stack.append(current_node)
            current_node.add_child(object_node)
            current_node = object_node

        if token_type == 'METHOD':
            method_node = Node(token, 'Method f')
            param_stack.append(current_node)
            current_node.add_child(method_node)
            current_node = method_node

        if token_type == 'CONSTUCTURE':
            constructure_node = Node(token, 'Constructure')
            branch_stack.append(current_node)
            current_node.add_child(constructure_node)
            current_node = constructure_node

        if token == "public" or token == "private" or token == 'protected':
            if len(access_stack) == 0:
                access_modifier_node = Node(token, "AccessModifier")
                access_stack.append(current_node)
                current_node.add_child(access_modifier_node)
                current_node = access_modifier_node
            else:
                current_node = access_stack.pop()
                access_modifier_node = Node(token, "AccessModifier")
                current_node.add_child(access_modifier_node)
                current_node = access_modifier_node

        if token == "{":
            sum = 0
            for i in variable_stack:
                if current_node.type in ('Variable', 'Declare'):
                    sum += 1
            if sum > 0:
                while sum != 0:
                    current_node = variable_stack.pop()
                    sum -= 1
            temp_node = current_node
            if current_node.type == 'Function':
                branch_list_node = Node(temp_node.data_type, "Block")
                branch_stack.append(current_node)
                current_node.add_child(branch_list_node)
                current_node = branch_list_node
            else:
                branch_list_node = Node(current_node.type, "Block")
                branch_stack.append(current_node)
                current_node.add_child(branch_list_node)
                current_node = branch_list_node

        if token == "}":
            temp_node = current_node.parent
            if temp_node.type == 'Declare Array' or temp_node.type == 'Array':
                temp_list = []
                temp_list.extend(current_node.children)
                sum_comma = 0
                sum_values = 0
                for i in temp_list:
                    if i.name == ',':
                        sum_comma += 1
                    else:
                        sum_values += 1
                if sum_comma >= sum_values or (sum_values - sum_comma) >= 2:
                    syntax_error_node = Node('Missing comma', f'Syntax error!')
                    current_node.add_child(syntax_error_node)
                    break

            current_node = branch_stack.pop()
            if current_node.type == 'ForLoop':
                current_node = for_stack.pop()
            if current_node.type == 'Constructure':
                current_node = branch_stack.pop()
            if current_node.type == 'IfStatement':
                current_node = if_stack.pop()
            if current_node.type == 'Function':
                current_node = function_stack.pop()

        if token == "(":
            if current_node.type == "Function" or current_node.type == 'Function Call' or current_node.type == 'ForLoop' or current_node.type == 'Method f' or current_node.type == 'Object' or current_node.type == 'Constructure' or current_node.type == "ProgramType" or current_node.type == "WhileLoop" or current_node.type == "IfStatement":
                parameters_list_node = Node("Parameters", "Parameters")
                param_stack.append(current_node)
                current_node.add_child(parameters_list_node)
                current_node = parameters_list_node
            else:
                bracket_list_node = Node(token, "Bracket")
                bracket_stack.append(current_node)
                current_node.add_child(bracket_list_node)
                current_node = bracket_list_node

        if token == ")":
            sum = 0
            for i in variable_stack:
                if current_node.type in ('Variable', 'Declare', 'Declare Array', 'Array'):
                    sum += 1
            if sum > 0:
                while sum != 0:
                    current_node = variable_stack.pop()
                    sum -= 1
            bracket_node = Node(token, 'Bracket')

            if current_node.type == 'Bracket':
                parent_node = bracket_stack.pop()
                current_node = parent_node
                current_node.add_child(bracket_node)
            elif current_node.type == "Parameters":
                parent_node = current_node.parent
                if parent_node.type == 'ForLoop':
                    temp_list = []
                    temp_list.extend(current_node.children)
                    sum_semicolon = 0
                    sum_etc = 0
                    for i in temp_list:
                        if i.name == ';':
                            sum_semicolon += 1
                        else:
                            sum_etc += 1
                    if sum_semicolon != 2:
                        syntax_error_node = Node(token, f'Syntax error! ForLoop')
                        current_node.add_child(syntax_error_node)
                        break
                current_node = param_stack.pop()
                if current_node.type == 'Function Call':
                    current_node = function_stack.pop()
                if current_node.type == 'ForLoop':
                    for var, scope in variable_scope:
                        if scope == 'for':
                            variable_scope.remove((var, scope))
                if current_node.type == 'Method f' or current_node.type == 'Object':
                    if len(param_stack) != 0:
                        current_node = param_stack.pop()

        if token_type in ('FLOAT', 'STRING', 'INTEGER', 'BOOLEAN'):
            if current_node.data_type in ('int', 'long long', 'long', 'short', 'unsigned short', 'unsigned int', \
                                          'unsigned long long', 'unsigned long'):
                if token_type in ('FLOAT', 'STRING', 'BOOLEAN'):
                    semantic_error_node = Node(token, f'Semantic error! Type {current_node.data_type}')
                    current_node.add_child(semantic_error_node)
                    break
            if current_node.data_type in ('float', 'double', 'long double'):
                if token_type in ('STRING', 'BOOLEAN'):
                    semantic_error_node = Node(token, f'Semantic error! Type {current_node.data_type}')
                    current_node.add_child(semantic_error_node)
                    break
            if current_node.data_type in ('signed char', 'char', 'unsigned char', 'wchar_t', 'char8_t', 'char16_t', 'char32_t'):
                if token_type in ('FLOAT', 'INTEGER', 'BOOLEAN'):
                    semantic_error_node = Node(token, f'Semantic error! Type {current_node.data_type}')
                    current_node.add_child(semantic_error_node)
                    break
                if token_type == 'STRING' and token.startswith('"') and len(token) > 3:
                    semantic_error_node = Node(token, f'Semantic error! Type {current_node.data_type}')
                    current_node.add_child(semantic_error_node)
                    break
            if current_node.data_type == 'string':
                if token_type in ('FLOAT', 'INTEGER', 'BOOLEAN'):
                    semantic_error_node = Node(token, f'Semantic error! Type {current_node.data_type}')
                    current_node.add_child(semantic_error_node)
                    break
            if current_node.data_type == 'bool':
                if token_type in ('FLOAT', 'INTEGER', 'STRING'):
                    semantic_error_node = Node(token, f'Semantic error! Type {current_node.data_type}')
                    current_node.add_child(semantic_error_node)
                    break
            if token_type == 'INTEGER':
                var_node = Node(token, 'Value', 'int')
                current_node.add_child(var_node)
            elif token_type == 'FLOAT':
                var_node = Node(token, 'Value', 'float')
                current_node.add_child(var_node)
            elif token_type == 'STRING':
                var_node = Node(token, 'Value', 'str')
                current_node.add_child(var_node)
            elif token_type == 'BOOLEAN':
                var_node = Node(token, 'Value', 'bool')
                current_node.add_child(var_node)

            if len(io_stack) != 0:
                current_node = io_stack.pop()
            sum = 0
            for i in io_stack:
                sum += 1
            if sum > 0:
                while sum != 0:
                    current_node = io_stack.pop()
                    sum -= 1

        if token in {"<", ">", "==", "!=", '<=', '>='}:
            comparison_node = check_comparison(token, current_node)

        if token == ',':
            if current_node.type in ('Variable', 'Declare', 'Square Bloсk'):
                current_node = variable_stack.pop()
            comma_node = Node(token, 'Comma')
            current_node.add_child(comma_node)

        if token == ";":
            if len(variable_stack) != 0:
                sum = 0
                for i in variable_stack:
                    if current_node.type in ('Variable', 'Declare', 'ReturnStatement', 'Declare Array', 'Array'):
                        sum += 1
                if sum > 0:
                    while sum != 0:
                        current_node = variable_stack.pop()
                        sum -= 1

            if len(std_stack) != 0:
                current_node = std_stack.pop()
            sum_std = 0
            for i in std_stack:
                sum_std += 1
            if sum_std > 0:
                while sum_std != 0:
                    current_node = std_stack.pop()
                    sum_std -= 1

            if current_node.type == 'Class':
                if len(class_stack) != 0:
                    current_node = class_stack.pop()
                sum_class = 0
                for i in class_stack:
                    sum_class += 1
                if sum_class > 0:
                    while sum_class != 0:
                        current_node = class_stack.pop()
                        sum_class -= 1

            if current_node.type == 'Function':
                if len(function_stack) != 0:
                    current_node = function_stack.pop()
                sum_func = 0
                for i in function_stack:
                    sum_func += 1
                if sum_func > 0:
                    while sum_func != 0:
                        current_node = function_stack.pop()
                        sum_func -= 1

            if current_node.type == 'Method f':
                if len(param_stack) != 0:
                    current_node = param_stack.pop()
                sum_param = 0
                for i in param_stack:
                    sum_param += 1
                if sum_param > 0:
                    while sum_param != 0:
                        current_node = param_stack.pop()
                        sum_param -= 1

            statement_node = StatementNode(token, "Statement")
            current_node.add_child(statement_node)

            if len(data_stack) != 0:
                data_stack.pop()
            else:
                continue

        if token == "=":
            assignment_node = Node(token, "Assignment")
            current_node.add_child(assignment_node)

        if token == ".":
            dot_node = Node(token, "DotOperator")
            current_node.add_child(dot_node)

        if token == "const":
            const_node = Node(token, "ConstModifier")
            current_node.add_child(const_node)

        if token == "return":
            semicolon_present = False
            for tok, _, ln in tokens:
                if ln == line and tok == ";":
                    semicolon_present = True
                    break
            if not semicolon_present:
                syntax_error_node = Node("Syntax error: !!!Semicolon missing after return statement",
                                         f'Syntax error! {line}')
                current_node.add_child(syntax_error_node)
                break

            parent_node = current_node
            return_node = Node(token, "ReturnStatement")
            return_stack.append(current_node)
            current_node.add_child(return_node)
            current_node = return_node

        if token == "std":
            std_node = Node(token, "StdNamespace")
            std_stack.append(current_node)
            current_node.add_child(std_node)
            parent_node = current_node
            current_node = std_node

            semicolon_present = False
            for tok, _, ln in tokens:
                if ln == line and tok == ";" and parent_node.type in ('ProgramType', 'Block', 'Operator Input', 'Object'):
                    semicolon_present = True
                    break

            if not semicolon_present:
                syntax_error_node = Node(f"123Syntax error: Semicolon missing after variable declaration.",
                                         f'Syntax error! {line}')
                current_node.add_child(syntax_error_node)
                break

        if token == '::':
            colon_node = Node(token, 'Colon')
            std_stack.append(current_node)
            current_node.add_child(colon_node)
            current_node = colon_node

        if token in ('cout', 'endl', 'cin') and token_type == "METHOD":
            method_node = Node(token, "Method")
            current_node.add_child(method_node)
            current_node = std_stack.pop()
            if len(std_stack) != 0:
                current_node = std_stack.pop()
            sum = 0
            for i in std_stack:
                sum += 1
            if sum > 0:
                while sum != 0:
                    current_node = std_stack.pop()
                    sum -= 1

        if token in ('cout', 'endl', 'cin') and token_type == "KEYWORD":
            method_node = Node(token, "Method")
            current_node.add_child(method_node)
            # current_node = io_stack.pop()
            if len(io_stack) != 0:
                current_node = io_stack.pop()
            sum = 0
            for i in io_stack:
                sum += 1
            if sum > 0:
                while sum != 0:
                    current_node = io_stack.pop()
                    sum -= 1

        if token == "<<" or token == ">>":
            io_operator_node = Node(token, 'Operator Input')
            io_stack.append(current_node)
            current_node.add_child(io_operator_node)
            current_node = io_operator_node
            # current_node.add_child(io_operator_node)

        if token in operators and token_type == 'ARITHMETIC OPERATOR':
            # if token == '+':
            #     print(left_operand.name, right_operand.name)
            #     if left_operand.data_type in ('int', 'long long', 'long', 'short', 'unsigned short', 'unsigned int', \
            #                               'unsigned long long', 'unsigned long') and right_operand.data_type in ('signed char', 'char', 'unsigned char', 'wchar_t', 'char8_t', 'char16_t', 'char32_t'):
            #         semantic_error_node = Node("Incompatible types for addition", "Semantic Error")
            #         current_node.add_child(semantic_error_node)
            #         break
            arithmetic_operator_node = Node(token, "Operator")
            current_node.add_child(arithmetic_operator_node)

        if token == "for" and token_type == 'KEYWORD':
            for_node = ForNode(token, "ForLoop")
            for_stack.append(current_node)
            current_node.add_child(for_node)
            current_node = for_node

        if token == "if" and token_type == 'KEYWORD':
            if_node = IfNode(token, "IfStatement")
            if_stack.append(current_node)
            current_node.add_child(if_node)
            current_node = if_node
        elif token == 'if' and token_type != 'KEYWORD':
            syntax_error_node = Node(token, f'Syntax error! In line {line}')
            current_node.add_child(syntax_error_node)
            break

        if token == "else" and token_type == 'KEYWORD':
            else_node = ElseNode(token, "Else")
            parent_node = current_node.parent
            if isinstance(parent_node, IfNode):
                if_else_node = IfElseNode(token, "IfElseStatement")
                parent_node.add_child(if_else_node)
                current_node = if_else_node
                current_node = branch_stack.pop()
            else:
                current_node.add_child(else_node)
        elif token == 'else' and token_type != 'KEYWORD':
            syntax_error_node = Node(token, f'Syntax error! In line {line}')
            current_node.add_child(syntax_error_node)
            break

        if token == "while" and token_type == 'KEYWORD':
            while_node = WhileNode(token, "WhileLoop")
            current_node.add_child(while_node)
            current_node = while_node
        elif token == 'while' and token_type != 'KEYWORD':
            syntax_error_node = Node(token, f'Syntax error! In line {line}')
            current_node.add_child(syntax_error_node)
            break

        if token == "new" and token_type == 'KEYWORD':
            new_node = Node(token, "NewOperator")
            current_node.add_child(new_node)
        elif token == 'new' and token_type != 'KEYWORD':
            syntax_error_node = Node(token, f'Syntax error! In line {line}')
            current_node.add_child(syntax_error_node)
            break

        if token == "delete":
            delete_node = Node(token, "DeleteOperator")
            current_node.add_child(delete_node)
        elif token == 'delete' and token_type != 'KEYWORD':
            syntax_error_node = Node(token, f'Syntax error! In line {line}')
            current_node.add_child(syntax_error_node)
            break

        if token == "break":
            delete_node = Node(token, "Break")
            current_node.add_child(delete_node)
        elif token == 'break' and token_type != 'KEYWORD':
            syntax_error_node = Node(token, f'Syntax error! In line {line}')
            current_node.add_child(syntax_error_node)
            break

        if token == "continue":
            delete_node = Node(token, "Continue")
            current_node.add_child(delete_node)
        elif token == 'continue' and token_type != 'KEYWORD':
            syntax_error_node = Node(token, f'Syntax error! In line {line}')
            current_node.add_child(syntax_error_node)
            break

        if 'LEXICAL ERROR' in token_type:
            lexical_error_node = Node(token, f'{token_type} In line {line}')
            current_node.add_child(lexical_error_node)
            break

        if 'SYNTAX ERROR' in token_type:
            syntax_error_node = Node(token, token_type)
            current_node.add_child(syntax_error_node)
            break

        if 'SEMANTIC ERROR' in token_type:
            semantic_error_node = Node(token, token_type)
            current_node.add_child(semantic_error_node)
            break
    return root


tokens = lexer()
tokens_iter = tokens
syntax_tree = build_syntax_tree(tokens_iter)

file_path_output = 'output_parser.txt'

write_output_to_file(syntax_tree.display(), file_path_output)
