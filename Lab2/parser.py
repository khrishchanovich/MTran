import constants
from main import lexer
from constants import *

token_table = lexer()
print(token_table)

def check_include(token_table):
    found_include = False
    for token, token_type in token_table:
        if token == '#include':
            if token_type == 'PREPROCESSOR DIRECTIVE':
                found_include = True
            else:
                print('LEXICAL ERROR!')
                return
        elif found_include:
            if token_type == 'HEADER FILE':
                print(f'#include {token}')
                return
            else:
                print('SYNTAX ERROR! NO DATA FOUND AFTER #include')
                return
    if found_include:
        print('SYNTAX ERROR! NO DATA FOUND AFTER #include')

def check_constants(token_table):
    constant_types = {'INTEGER', 'FLOAT', 'STRING'}
    constants = set()

    for token, token_type in token_table:
        if token_type in constant_types:
            constants.add((token, token_type))

    return constants

def check_variable(token_table):
    data_types = {'int', 'long long', 'float', 'string'}
    variables = []

    current_data_type = None
    current_variables = []

    i = 0
    while i < len(token_table):
        token, token_type = token_table[i]

        if token_type == 'DATA TYPE':
            current_data_type = token
        elif token_type == f'VARIABLE ({current_data_type.upper()})':
            current_variables.append(token)
        elif token == ';' or token == ',':
            for var in current_variables:
                variables.append((current_data_type, var))
            current_variables = []

        i += 1

    print("Variable Declarations:")
    for data_type, variable in variables:
        print(f"{data_type} {variable}")

check_include(token_table)
check_constants(token_table)
check_variable(token_table)
