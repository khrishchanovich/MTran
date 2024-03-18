from parser import parser


class Translator:
    def __init__(self):
        self.code_python = ''
        self.private_member = []
        self.variable_list = []
        self.temp_list = ''
        self.in_class = False
        self.in_if = False
        self.depth = 0
        self.temp_depth = 0
        self.count_compare = 0

    def declare_translator(self, node):
        self.code_python += '\t' * self.depth
        variable_exists = False
        for name, _ in self.variable_list:
            if node.name == name:
                variable_exists = True
                break

        if not variable_exists:
            if self.in_class:
                self.variable_list.append((node.name, True))
            else:
                self.variable_list.append((node.name, False))

        for name, check in self.variable_list:
            if node.name == name:
                if check:
                    self.code_python += f'self.{node.name}'
                else:
                    self.code_python += f'{node.name}'
                break

        for member_declare in node.children:
            if member_declare.type == 'Assignment':
                assignment_node = member_declare.name
                self.code_python += f' {assignment_node} '
            if member_declare.type == 'Value':
                value_node = member_declare.name
                self.code_python += f' {value_node}'
            if member_declare.type == 'Variable':
                self.declare_translator(member_declare)
            if member_declare.type == 'Operator':
                operator_node = member_declare.name
                self.code_python += f' {operator_node}'
            if member_declare.type == 'DotOperator':
                self.code_python += member_declare.name
            if member_declare.type == 'Method f':
                self.code_python += member_declare.name
                self.function_translator(member_declare)
            if member_declare.type == 'Comparison':
                if self.in_for and not self.in_if:
                    self.code_python = self.code_python[:-1]
                else:
                    self.code_python += member_declare.name
            if member_declare.type == 'Block' and (member_declare.name == 'Declare Array' or member_declare.name == 'Array'):
                self.code_python += '['
                self.block_translator(member_declare)
            if member_declare.type == 'End Block':
                self.code_python += ']'
            if member_declare.type == 'Square Block' and node.type == 'Array':
                self.code_python += '['
                self.block_translator(member_declare)
            if member_declare.type == 'End Square Block' and node.type == 'Array':
                self.code_python += ']'
            if member_declare.type == 'Array':
                self.declare_translator(member_declare)
            if 'Semantic' in member_declare.type:
                self.code_python += member_declare.type
                break

    def parameters_translator(self, node):
        for member_param in node.children:
            if member_param.type == 'Variable':
                self.declare_translator(member_param)
            if member_param.type == 'Declare':
                if self.in_class:
                    self.in_class = False
                    self.declare_translator(member_param)
                    self.in_class = True
                else:
                    self.declare_translator(member_param)
            if member_param.type == 'Array':
                self.declare_translator(member_param)
            if member_param.type == 'Comma':
                self.code_python += member_param.name
            if member_param.type == 'Value':
                self.declare_translator(member_param)

    def function_translator(self, node):
        for member_function in node.children:
            if member_function.type == 'Parameters':
                self.temp_depth = self.depth
                self.depth = 0
                if self.in_class:
                    self.code_python += '(self, '
                    self.parameters_translator(member_function)
                    self.code_python += ')'
                else:
                    self.code_python += '('
                    self.parameters_translator(member_function)
                    self.code_python += ')'
                self.depth = self.temp_depth
            if member_function.type == 'Block':
                self.depth += 1
                self.code_python += f':\n'
                self.block_translator(member_function)
            if member_function.type == 'End Block':
                self.depth -= 1
                self.code_python += '\n'

    def main_translator(self, node):
        for member_function in node.children:
            if member_function.type == 'Block':
                self.depth += 1
                self.code_python += f':\n'
                self.block_translator(member_function)
            if member_function.type == 'End Block':
                self.depth -= 1
                self.code_python += '\n'

    def access_specifier_translator(self, node):
        for member_access in node.children:
            if member_access.type == 'Declare':
                self.declare_translator(member_access)
            if member_access.type == 'Statement':
                self.code_python += '\n'
            if member_access.type == 'Constructure':
                self.code_python += '\t' * self.depth
                self.code_python += f'def __init__'
                self.function_translator(member_access)
            if member_access.type == 'Function':
                self.code_python += '\t' * self.depth
                self.code_python += f'def {member_access.name}'
                self.function_translator(member_access)

    def return_translator(self, node):
        for member_return in node.children:
            if member_return.type == 'Variable':
                self.declare_translator(member_return)
            if member_return.type == 'Statement':
                self.code_python += '\n'
            if member_return.type == 'Value':
                self.declare_translator(member_return)

    def object_translator(self, node):
        for member_object in node.children:
            if member_object.type == 'DotOperator':
                self.code_python += member_object.name
            if member_object.type == 'Function Call':
                self.code_python += member_object.name
                self.function_translator(member_object)

    def print_translator(self, node):
        for member_print in node.children:
            if member_print.type == 'Value':
                self.declare_translator(member_print)
                self.code_python += ', '
            if member_print.type == 'Object':
                self.code_python += member_print.name
                self.object_translator(member_print)
                self.code_python += ', '
            if member_print.type == 'Variable':
                self.declare_translator(member_print)
                self.code_python += ', '
            if member_print.type == 'Array':
                self.declare_translator(member_print)
                self.code_python += ', '

    def for_param_translator(self, node):
        count = 0
        count_comparison = 0
        for member_param in node.children:
            if member_param.type == 'Statement':
                count += 1
            if count == 0:
                if member_param.type in ('Declare', 'Variable'):
                    self.code_python += member_param.name
            if count == 1:
                if member_param.type in ('Declare', 'Variable'):
                    self.code_python += ' in range('
                    self.declare_translator(member_param)
                    self.code_python += ')'

    def for_translator(self, node):
        for member_for in node.children:
            if member_for.type == 'Parameters':
                self.for_param_translator(member_for)
            if member_for.type == 'Block':
                self.depth += 1
                self.code_python += f':\n'
                self.block_translator(member_for)
            if member_for.type == 'End Block':
                self.depth -= 1
                self.in_for = False
                self.code_python += '\n'

    def if_translator(self, node):
        for member_if in node.children:
            if member_if.type == 'Parameters':
                self.parameters_translator(member_if)
            if member_if.type == 'Block':
                self.depth += 1
                self.code_python += f':\n'
                self.block_translator(member_if)
            if member_if.type == 'End Block':
                self.in_if = False
                self.depth -= 1
                self.code_python += '\n'


    def block_translator(self, node):
        parent_node = node.parent
        for member_block in node.children:
            if member_block.name in ('public', 'protected', 'private'):
                self.access_specifier_translator(member_block)
            if member_block.type == 'Variable':
                self.declare_translator(member_block)
            if member_block.type == 'Declare':
                if member_block.children:
                    self.declare_translator(member_block)
                else:
                    self.code_python += '\t' * self.depth

                    variable_exists = False
                    for name, _ in self.variable_list:
                        if member_block.name == name:
                            variable_exists = True
                            break

                    if not variable_exists:
                        if self.in_class:
                            self.variable_list.append((member_block.name, True))
                        else:
                            self.variable_list.append((member_block.name, False))

                    for name, check in self.variable_list:
                        if member_block.name == name:
                            if check:
                                self.code_python += f'self.{member_block.name}'
                            else:
                                self.code_python += f'{member_block.name}'
                            break

                    if member_block.data_type in ('int', 'long long', 'long', 'short', 'unsigned short', 'unsigned int', \
                                          'unsigned long long', 'unsigned long', 'float', 'double', 'long double'):
                        self.code_python += f' = 0'
                    if member_block.data_type in ('str', 'string', 'signed char', 'char', 'unsigned char', 'wchar_t', 'char8_t', 'char16_t', 'char32_t'):
                        self.code_python += f"= ''"
            if member_block.type == 'Declare Array':
                self.declare_translator(member_block)
            if member_block.type == 'Array':
                self.declare_translator(member_block)
            if member_block.type == 'Statement':
                self.code_python += '\n'
            if member_block.type == 'ReturnStatement':
                self.code_python += '\t' * self.depth
                if parent_node.name != 'main':
                    self.code_python += f'{member_block.name} '
                    self.return_translator(member_block)
                else:
                    continue
            if member_block.type == 'Function Call':
                self.code_python += '\t' * self.depth
                self.code_python += member_block.name
                self.function_translator(member_block)
            if member_block.type == 'Class':
                self.temp_list = member_block
                self.class_translator(member_block)
            if member_block.type == 'Cout':
                self.code_python += '\t' * self.depth
                self.code_python += 'print('
                self.print_translator(member_block)
            if member_block.type == 'Endl':
                if self.code_python[-2] == ',' and self.code_python[-1] == ' ':
                    self.code_python = self.code_python[:-2] + ')'
                else:
                    self.code_python += ')'
            if member_block.type == 'Object':
                self.code_python += '\t' * self.depth
                self.code_python += member_block.name
                self.object_translator(member_block)
            if member_block.type == 'ForLoop':
                self.code_python += '\t' * self.depth
                self.in_for = True
                self.code_python += 'for '
                self.for_translator(member_block)
            if member_block.type == 'IfStatement':
                self.code_python += '\t' * self.depth
                self.in_if = True
                self.code_python += 'if '
                self.if_translator(member_block)
            if member_block.type == 'ElseStatement':
                self.code_python += '\t' * self.depth
                self.code_python += 'else '
                self.if_translator(member_block)
            if member_block.type == 'Break':
                self.code_python += '\t' * self.depth
                self.code_python += 'break'
            if member_block.type == 'Value':
                self.declare_translator(member_block)
            if member_block.type == 'Comma':
                self.code_python += ', '


    def class_translator(self, node):
        for member_class in node.children:
            if member_class.type == 'Block':
                self.depth += 1
                self.code_python += f':\n'
                self.block_translator(member_class)
            if member_class.type == 'End Block':
                self.depth -= 1
                self.in_class = False
                self.code_python += '\n'
            if member_class.type == 'Object':
                self.code_python += '\t' * self.depth
                self.code_python += f'{member_class.name} =  {self.temp_list.name}'
                self.function_translator(member_class)

    def translator(self, syntax_tree):
        root = syntax_tree.children
        for member_root in root:
            if member_root.type == 'Class':
                self.in_class = True
                self.code_python += f'class {member_root.name}'
                self.class_translator(member_root)
            if member_root.type == 'Statement':
                self.code_python += '\n'
            if member_root.type == 'Function':
                if member_root.name == 'main':
                    self.code_python += f'if __name__ == "__main__"'
                    self.main_translator(member_root)
                else:
                    self.code_python += '\t' * self.depth
                    self.code_python += f'def {member_root.name}'
                    self.function_translator(member_root)
            if member_root.type == 'Declare':
                self.code_python += '\t' * self.depth
                self.declare_translator(member_root)
            if member_root.type == 'Declare array':
                self.code_python += '\t' * self.depth
                self.declare_translator(member_root)
            if 'Semantic' in member_root.type:
                self.code_python += member_root.type
                break


translator = Translator()
translator.translator(parser())
print(translator.code_python)
exec(translator.code_python)




