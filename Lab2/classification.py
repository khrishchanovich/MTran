from constants import keywords, data_types, operators, standart_function, standart_libraries, containers,classes
from type_cheking import is_integer_type, is_character_type, is_float_type, is_bool, is_string

list_data_types = []
lexical_error_tokens = []


def classify_token(token, prev_token, next_token, token_table):
    if token in keywords:
        return keywords[token]
    elif token in standart_function:
        return standart_function[token]
    elif token in standart_libraries:
        return standart_libraries[token]
    elif token in containers:
        return containers[token]
    elif token in classes:
        return classes[token]
    elif token in operators:
        if token in ('<<', '>>'):
            if prev_token in ('cout', 'cin') or next_token in ('endl'):
                return 'I/O OPERATOR'
            elif prev_token.isdigit() or prev_token.isidentifier():
                return 'BITWISE OPERATOR'
            elif next_token in ('cout', 'cin'):
                return 'I/O OPERATOR'
            else:
                return 'I/O OPERATOR'
        if token == '~':
            if token_table[next_token] == 'ClASS':
                token_table[token] = 'TILDA'
                return 'TILDA'
            else:
                return 'BITWISE OPERATOR'
        if token == '<':
            if prev_token == 'template':
                return 'SIGN'
            else:
                return 'COMPARISON OPERATOR'
        if token == '*':
            if len(list_data_types) != 0:
                if prev_token in data_types or (next_token in token_table and f'VARIABLE ({list_data_types[-1].upper()})' in token_table[next_token]) \
                    or (next_token in token_table and f'FUNCTION (POINTER {list_data_types[-1].upper()})' in token_table[next_token]) \
                    or (next_token in token_table and f'POINTER ({list_data_types[-1].upper()})' in token_table[next_token]) \
                    or (next_token in token_table and f'METHOD OF CLASS'):
                    token_table[token] = 'ASTERIK'
                    return 'ASTERIK'
                elif prev_token in token_table and token_table[prev_token] == 'CLASS':
                    token_table[token] = 'CLASS POINTER'
                    return 'CLASS POINTER'
            else:
                return 'ARITHMETIC OPERATOR'
        if token == '&':
            if prev_token in data_types:
                token_table[token] = 'REFERENCE OPERATOR'
                return 'REFERENCE OPERATOR'
            else:
                token_table[token] = 'BITWISE OPERATOR'
                return 'BITWISE OPERATOR'
        token_table[token] = operators[token]
        return operators[token]
    elif token in data_types:
        if prev_token in ('/*', '//'):
            return 'STRING OF COMMENT'
        list_data_types.append(token)
        return data_types[token]
    elif token.endswith('[]'):
        return 'ARRAY'
    elif is_string(token):
        if prev_token == '#include':
            return 'FILE'
        return 'STRING'
    elif is_integer_type(token):
        return 'INTEGER'
    elif is_float_type(token):
        return 'FLOAT'
    elif is_bool(token):
        return 'BOOLEAN'
    elif is_character_type(token):
        return 'CHAR'
    elif token.isidentifier():
        if token in token_table:
            if next_token == '(' and token_table[token] == 'CLASS':
                return 'CONSTUCTURE'
            # if token_table[token].startswith('VARIABLE'):
            #     current_data_type = token_table[token].split('(')[1].split(')')[0]
            #     if current_data_type != list_data_types[-1].upper():
            #         token_table[token] = f'VARIABLE ({list_data_types[-1].upper()})'
            # if token_table[token].startswith('POINTER'):
            #     current_data_type = token_table[token].split('(')[1].split(')')[0]
            #     if current_data_type != list_data_types[-1].upper():
            #         token_table[token] = f'POINTER ({list_data_types[-1].upper()})'
            # if token_table[token].startswith('FUNCTION'):
            #     current_data_type = token_table[token].split('(')[1].split(')')[0]
            #     if current_data_type != list_data_types[-1].upper():
            #         token_table[token] = f'FUNCTION ({list_data_types[-1].upper()})'
            # if token_table[token].startswith('FUNCTION (POINTER'):
            #     current_data_type = token_table[token].split('(')[1].split(')')[0]
            #     if current_data_type != list_data_types[-1].upper():
            #         token_table[token] = f'FUNCTION (POINTER {list_data_types[-1].upper()})'
            return token_table[token]
        else:
            if prev_token == '~' and next_token == '(':
                return 'DESCTRUCTURE'
            if prev_token == '::':
                return 'METHOD'
            elif prev_token == 'using':
                token_table[token] = ''
            elif next_token == '(':
                if prev_token in data_types:
                    token_table[token] = f'FUNCTION ({list_data_types[-1].upper()})'
                    return f'FUNCTION ({list_data_types[-1].upper()})'
                elif prev_token == '*':
                    if prev_token in token_table and token_table[prev_token] == 'CLASS POINTER':
                        token_table[token] = f'METHOD OF CLASS'
                        return f'METHOD OF CLASS'
                    token_table[token] = f'FUNCTION (POINTER {list_data_types[-1].upper()})'
                    return f'FUNCTION (POINTER {list_data_types[-1].upper()})'
            else:
                if prev_token == '*' and (prev_token in token_table and token_table[prev_token] == 'CLASS POINTER'):
                    token_table[token] = f'METHOD OF CLASS'
                    return f'METHOD OF CLASS'
                if prev_token in data_types or prev_token == ',':
                    token_table[token] = f'VARIABLE ({list_data_types[-1].upper()})'
                    return f'VARIABLE ({list_data_types[-1].upper()})'
                elif prev_token == '*':
                    if len(list_data_types) != 0:
                        token_table[token] = f'POINTER ({list_data_types[-1].upper()})'
                        return f'POINTER ({list_data_types[-1].upper()})'
                    else:
                        token_table[token] = 'IDENTIFICATOR'
                        return 'IDENTIFICATOR'
            if next_token == '{':
                if prev_token in 'class':
                    token_table[token] = 'CLASS'
                    return 'CLASS'
                if prev_token in 'struct':
                    token_table[token] = 'STRUCTURE'
                    return 'STRUCTURE'
            # elif prev_token in data_types or prev_token == ',':
            #     token_table[token] = f'VARIABLE ({list_data_types[-1].upper()})'
            #     return f'VARIABLE ({list_data_types[-1].upper()})'
            # elif prev_token == '*' and ('*' in token_table and token_table['*'] == 'ASTERIK'):
            #     token_table[token] = f'POINTER ({list_data_types[-1].upper()})'
            #     return f'POINTER ({list_data_types[-1].upper()})'
            elif prev_token in token_table and token_table[prev_token] == 'CLASS' or prev_token in classes:
                token_table[token] = f'OBJECT OF {prev_token}'
                return f'OBJECT OF {prev_token}'

            else:
                token_table[token] = 'IDENTIFIER'
                return 'IDENTIFIER'
    else:
        if prev_token in ('/*', '//'):
            return 'STRING OF COMMENT'
        elif prev_token == '#include':
            return 'BIBLE'
        elif prev_token == '.':
            return 'METHOD'
        elif token.endswith(('LL', 'll', 'UL', 'ul')):
            if is_integer_type(token[:-2]):
                return 'INTEGER'
            elif is_float_type(token[:-2]):
                return 'FLOAT'
            else:
                print(token)
                print(token[0].isdigit())
                if token[0].isdigit():
                    return 'LEXICAL ERROR! Identifier cannot start with a digit.'
                token_table[token] = 'IDENTIFICATOR'
                return 'IDENTIFICATOR'
        elif token.endswith(('ULL', 'ull')):
            if is_integer_type(token[:-3]):
                return 'INTEGER'
            elif is_float_type(token[:-3]):
                return 'FLOAT'
            else:
                print(token)
                print(token[0].isdigit())
                if token[0].isdigit():
                    return 'LEXICAL ERROR! Identifier cannot start with a digit.'
                token_table[token] = 'IDENTIFICATOR'
                return 'IDENTIFICATOR'
        elif token.endswith(('L', 'l', 'F', 'f', 'D', 'd')):
            if is_integer_type(token[:-1]):
                return 'INTEGER'
            elif is_float_type(token[:-1]):
                return 'FLOAT'
            else:
                if token[0].isdigit():
                    return 'LEXICAL ERROR! Identifier cannot start with a digit.'
                token_table[token] = 'IDENTIFICATOR'
                return 'IDENTIFICATOR'
        else:
            lexical_error_tokens.append(token)
            return f'LEXICAL ERROR! {token}'
