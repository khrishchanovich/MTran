from constants import keywords, data_types, operators
from type_cheking import is_integer_type, is_character_type, is_float_type, is_bool, is_string


def classify_token(token, prev_token, next_token, token_table):
    if token in keywords:
        return keywords[token]
    elif token in operators:
        if token in ('<<', '>>'):
            if prev_token in ('cout', 'cin') or next_token in ('endl'):
                return 'I/O OPERATOR'
            elif prev_token.isdigit() or prev_token.isidentifier():
                return 'BITWISE OPERATOR'
            elif next_token in ('cout', 'cin'):
                return 'I/O OPERATOR'
        return operators[token]
    elif token in data_types:
        return data_types[token]
    elif token.endswith('[]'):
        return 'ARRAY'
    elif is_string(token):
        return 'STRING'
    elif is_integer_type(token):
        return 'INTEGER'
    elif is_float_type(token):
        return 'FLOAT'
    elif is_bool(token):
        return 'BOOLEAN'
    elif is_character_type(token):
        return 'CHAR'
    elif token.startswith('/*') and token.endswith('*/') and '/*' not in token[1:-1]:
        return 'INSIDE COMMENT'  # Updated classification
    elif token.startswith('#include <') and token.endswith('>') and '<' not in token[1:-1]:
        return 'HEADER FILE'  # Updated classification
    elif token.startswith('<') and token.endswith('>') and '<' not in token[1:-1]:
        return 'LIBRARY'
    elif token.startswith('//'):
        return 'COMMENT'
    elif token.isidentifier():
        if token in token_table:
            return token_table[token]
        else:
            if prev_token in token_table and token_table[prev_token] == 'CLASS':
                token_table[token] = 'OBJECT OF CLASS'
                return 'OBJECT OF CLASS'
            elif next_token == '(':
                if prev_token in data_types:
                    token_table[token] = f'FUNCTION OF TYPE {prev_token.upper()}'
                    return f'FUNCTION OF TYPE {prev_token.upper()}'
                else:
                    token_table[token] = 'Function'
                    return 'FUNCTION'
            elif next_token == '{':
                if prev_token in 'class':
                    token_table[token] = 'CLASS'
                    return 'CLASS'
            elif prev_token in data_types:
                token_table[token] = f'VARIABLE OF TYPE {prev_token.upper()}'
                return f'VARIABLE OF TYPE {prev_token.upper()}'
            elif token in data_types:
                token_table[token] = data_types[token]
                return data_types[token]
            elif token == 'class':
                pass
            elif token == 'struct':
                token_table[token] = 'STRUCTURE'
                return 'STRUCTURE'
            else:
                token_table[token] = 'IDENTIFIER'
                return 'IDENTIFIER'
    elif '.' in token:
        return 'METHOD'
    elif token.endswith(':'):
        if prev_token == 'case':
            return 'CASE LABEL'
        elif prev_token == 'default':
            return 'DEFAULT LABEL'
        else:
            return 'COLON'
    else:
        return f'LEXICAL ERROR {token}'
