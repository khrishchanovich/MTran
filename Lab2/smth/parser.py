from enum import Enum

# Типы токенов
class TokenType(Enum):
    PreprocessorDirective = 1
    Function = 2
    Declaration = 3
    Block = 4
    VariableDeclaration = 5
    Expression = 6
    IfStatement = 7
    ElseBlock = 8
    ForLoop = 9
    Initialization = 10
    Condition = 11
    Increment = 12
    ReturnStatement = 13
    Identifier = 14
    Literal = 15

# Структура программы
class Program:
    def __init__(self):
        self.directives = []
        self.functions = []

# Структура функции
class Function:
    def __init__(self, name):
        self.name = name
        self.declarations = []
        self.statements = []

# Структура оператора
class Statement:
    def __init__(self, type):
        self.type = type
        self.children = []

# Функция для синтаксического анализа
def parse(tokens):
    program = Program()
    current_function = None
    current_statement = None

    for token, token_type in tokens:
        if token_type == TokenType.PreprocessorDirective:
            program.directives.append(token)
        elif token_type == TokenType.Function:
            current_function = Function(token)
            program.functions.append(current_function)
        elif token_type == TokenType.Declaration:
            if current_function:
                current_statement = Statement(TokenType.Declaration)
                current_function.declarations.append(current_statement)
        # Добавьте остальные условия для других типов операторов

    return program

# Пример использования
tokens = [
    ("#include <iostream>", TokenType.PreprocessorDirective),
    ("main", TokenType.Function),
    ("{", TokenType.Block),
    ("int", TokenType.Declaration),
    ("a", TokenType.Identifier),
    ("=", TokenType.Expression),
    ("5", TokenType.Literal),
    # Добавьте остальные токены здесь
    ("}", TokenType.Block)
]

parsed_program = parse(tokens)
print(parsed_program)
