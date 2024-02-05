from constants import keywords, data_types, operators
from type_cheking import is_integer_type, is_character_type, is_float_type, is_bool, is_string


def classify_token(token, prev_token, next_token, token_table):
    if token in keywords:
        return keywords[token]
    elif token in operators:
        if token in ('<<', '>>'):
            if prev_token == 'std::cout' or next_token == 'std::endl':
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
    elif token.startswith('#include <') and token.endswith('>'):
        return 'HEADER FILE'
    elif token.startswith('<') and token.endswith('>'):
        return 'LIBRARY'
    elif token.startswith('std::'):
        return 'STL STRUCTURE'
    elif token.isidentifier():
        if token in token_table:
            return token_table[token]
        else:
            if next_token == '(':
                if prev_token in data_types:
                    token_table[token] = f'FUNCTION OF TYPE {prev_token}'
                    return f'FUNCTION OF TYPE {prev_token.upper()}'
                else:
                    token_table[token] = 'Function'
                    return 'FUNCTION'
            elif prev_token in data_types:
                token_table[token] = f'VARIABLE OF TYPE {prev_token}'
                return f'VARIABLE OF TYPE {prev_token.upper()}'
            elif token in data_types:
                token_table[token] = data_types[token]
                return data_types[token]
            elif token == 'class':
                token_table[token] = 'CLASS'
                return 'CLASS'
            elif token == 'struct':
                token_table[token] = 'SRTUCTURE'
                return 'SRTUCTURE'
            else:
                token_table[token] = 'IDENTIFIER'
                return 'IDENTIFIER'
    elif '.' in token:
        return 'METHOR'
    elif token.endswith(':'):
        if prev_token == 'case':
            return 'CASE LABEL'
        elif prev_token == 'default':
            return 'DEFAULT LABEL'
        else:
            return 'CLASS MEMBER INITIALIZATION'
    else:
        return f'LEXICAL ERROR {token}'
