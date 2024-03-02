from main import lexer
from constants import data_types, keywords


def check_variable(token_type, token, data_type):
    if 'VARIABLE' in token_type:
        variable_name = token
        variable_node = VariableNode(data_type, variable_name)
        data_type = None
        variable_name = None
        return variable_node

def check_function(token_type, token, data_type):

    if 'FUNCTION' in token_type:
        function_name = token

        function_node = FunctionNode(data_type, function_name)
        data_type = None
        function_name = None
        return function_node



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
    def __init__(self, name, node_type, parent=None, children=None):
        self.name = name
        self.type = node_type
        self.parent = parent
        self.children = children if children is not None else []

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def display(self, level=0):
        indent = "    " * level
        print(f"{indent}|- {self.type}: {self.name}")
        for child in self.children:
            child.display(level + 1)

    # def display(self, level=0):
    #     indent = "    " * level
    #     if self.type in {"Declare", "Array", "ForLoop", "Parameters", "Block"}:
    #         print(f"{indent}|- {self.type}: {self.name}")
    #     for child in self.children:
    #         child.display(level + 1)


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


class ArrayNode(Node):
    def __init__(self, data_type: None, name, size):
        if data_type is not None:
            super().__init__(f"{data_type} {name}[{size}]", "Array")
        else:
            super().__init__(f"{name}[{size}]", "Array")
        self.data_type = data_type
        self.name = name
        self.size = size

    def display(self, level=0):
        indent = "    " * level
        if self.data_type is not None:
            print(f"{indent}|- Array: {self.data_type} {self.name}[{self.size}]")
        else:
            print(f"{indent}|- Array: {self.name}[{self.size}]")


class VariableNode(Node):
    def __init__(self, data_type: None, name):
        if data_type is not None:
            super().__init__(f"{data_type} {name}", "Variable")
        else:
            super().__init__(f"{name}", "Variable")
        self.data_type = data_type
        self.name = name

    def display(self, level=0):
        indent = "    " * level
        if self.data_type:
            print(f"{indent}|- Declare: {self.data_type} {self.name}")
        else:
            print(f"{indent}|- Variable: {self.name}")


class ForNode(Node):
    def __init__(self, name, node_type):
        super().__init__(name, node_type)


class IfNode(Node):
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


class FunctionNode(Node):
        def __init__(self, data_type: None, name):
            if data_type is not None:
                super().__init__(f"{data_type} {name}", "Function")
            else:
                super().__init__(f"{name}", "Function")
            self.data_type = data_type
            self.name = name

        def display(self, level=0):
            indent = "    " * level
            if self.data_type:
                print(f"{indent}|- Function: {self.data_type} {self.name}")
            else:
                print(f"{indent}|- Function: {self.name}")


def build_syntax_tree(tokens):
    root = Node("Program", "ProgramType")
    current_node = root
    function_definitions = {}
    branch_stack = []
    param_stack = []
    bracket_stack = []
    inside_comment = False
    is_array_declaration = False
    array_name = None
    current_comment = ""

    for token, token_type in tokens:
        if token == "//":
            # Игнорируем комментарии в одну строку
            continue
        elif token == "/*":
            # Начало многострочного комментария
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

        if token in data_types:
            data_type = token
            data_list_node = Node(f'{data_type.upper()}', "DataType")
            while True:
                token, token_type = next(tokens)
                variable_node = check_variable(token_type, token, data_type)
                function_node = check_function(token_type, token, data_type)
                if function_node:
                    # data_list_node.add_child(function_node)
                    current_node.add_child(function_node)
                    # current_node = function_node
                    break
                if variable_node:
                    data_list_node.add_child(variable_node)
                if 'ARRAY' in token_type:
                    array_name = token
                    is_array_declaration = True
                if token == '[':
                    token, _ = next(tokens)
                    array_size = token
                if token == ']':
                    if is_array_declaration:
                        array_node = ArrayNode(data_type, array_name, array_size)
                        if array_node:
                            data_list_node.add_child(array_node)
                        is_array_declaration = False
                        data_type = None
                        array_name = None
                        array_size = None
                check_comma(token, data_list_node)
                if check_chto(token, data_list_node):
                    break
                if token == '}':
                    break
                if token == '=':
                    assignment_node = Node(token, 'Assignment')
                    data_list_node.add_child(assignment_node)
                if token_type in ('FLOAT', 'STRING', 'INTEGER'):
                    var_node = Node(token, 'Value')
                    data_list_node.add_child(var_node)
            if not function_node:
                current_node.add_child(data_list_node)
            continue

        if 'VARIABLE' in token_type:
            variable_node = check_variable(token_type, token, None)
            current_node.add_child(variable_node)

        if 'ARRAY' in token_type or 'CONTAINER' in token_type:
            array_name = token
        if token == '[':
            token, _ = next(tokens)
            array_size = token
        if token == ']':
            array_node = ArrayNode(None, array_name, array_size)
            current_node.add_child(array_node)
            data_type = None
            array_name = None
            array_size = None

        if token == "#include":
            preprocessor_directive_node = PreprocessorDirectiveNode(token, "PreprocessorDirective")
            current_node.add_child(preprocessor_directive_node)
            current_node = preprocessor_directive_node
        elif token == "class":
            class_node = ClassNode(token, "Class")
            current_node.add_child(class_node)
            current_node = class_node
        elif token == "public" or token == "private":
            access_modifier_node = Node(token, "AccessModifier")
            current_node.add_child(access_modifier_node)
            current_node = access_modifier_node
        elif token == "{":
            branch_stack.append(current_node)
            current_node = Node("Block", "Block")
        elif token == "}":
            parent_node = branch_stack.pop()
            parent_node.add_child(current_node)
            current_node = root
        elif token == "(":
            print(current_node.type)
            if current_node.type == "Function" or current_node.type == "ForLoop" or current_node.type == "ProgramType" or current_node.type == "WhileLoop" or current_node.type == "IfStatement":
                parameters_list_node = Node("Parameters", "Parameters")
                param_stack.append(current_node)
                current_node.add_child(parameters_list_node)
                current_node = parameters_list_node
            else:
                bracket_list_node = Node(token, "Bracket")
                bracket_stack.append(current_node)
                current_node.add_child(bracket_list_node)
                current_node = bracket_list_node
        elif token == ")":
            bracket_node = Node(token, 'Bracket')
            if current_node.type == 'Bracket':
                parent_node = bracket_stack.pop()
                current_node = parent_node
                current_node.add_child(bracket_node)
            elif current_node.type == "Parameters":
                current_node = param_stack.pop()
        if token_type in ('FLOAT', 'STRING', 'INTEGER'):
            var_node = Node(token, 'Value')
            current_node.add_child(var_node)
        if token in {"<", ">", "==", "!="}:
            comparison_node = check_comparison(token, current_node)
        elif token == ";":
            statement_node = StatementNode(token, "Statement")
            current_node.add_child(statement_node)
        elif token == "=":
            assignment_node = Node(token, "Assignment")
            current_node.add_child(assignment_node)
        elif token == ".":
            dot_node = Node(token, "DotOperator")
            current_node.add_child(dot_node)
        elif token == "const":
            const_node = Node(token, "ConstModifier")
            current_node.add_child(const_node)
        elif token == "return":
            return_node = Node(token, "ReturnStatement")
            current_node.add_child(return_node)

        elif token == "std" or token == "cout" or token == "endl":
            std_node = Node(token, "StdNamespace")
            current_node.add_child(std_node)
        elif token == "<<" or token == ">>":
            io_operator_node = Node(token, token_type)
            current_node.add_child(io_operator_node)
        elif token == "+" or token == "*" or token == "+=":
            arithmetic_operator_node = Node(token, "ArithmeticOperator")
            current_node.add_child(arithmetic_operator_node)
        elif token == "for":
            for_node = ForNode(token, "ForLoop")
            current_node.add_child(for_node)
            current_node = for_node
        elif token == "if":
            if_node = IfNode(token, "IfStatement")
            current_node.add_child(if_node)
            current_node = if_node
        elif token == "else":
            else_node = Node(token, "Else")
            parent_node = current_node.parent
            if isinstance(parent_node, IfNode):
                if_else_node = IfElseNode(token, "IfElseStatement")
                parent_node.add_child(if_else_node)
                current_node = if_else_node
            else:
                current_node.add_child(else_node)
        elif token == "while":
            while_node = WhileNode(token, "WhileLoop")
            current_node.add_child(while_node)
            current_node = while_node
        elif token in {"do", "switch", "case", "default"}:
            keyword_node = Node(token, "Keyword")
            current_node.add_child(keyword_node)
        elif token == "<<" or token == ">>":
            io_operator_node = Node(token, token_type)
            current_node.add_child(io_operator_node)
        elif token == "else":
            else_node = Node(token, "Else")
            current_node.add_child(else_node)
        elif token == "new":
            new_node = Node(token, "NewOperator")
            current_node.add_child(new_node)
        elif token == "delete":
            delete_node = Node(token, "DeleteOperator")
            current_node.add_child(delete_node)
        # else:
        #     identifier_node = Node(token, token_type)
        #     current_node.add_child(identifier_node)

    return root, function_definitions


tokens = lexer()
tokens_iter = iter(tokens)


syntax_tree, function_definitions = build_syntax_tree(tokens_iter)
syntax_tree.display()