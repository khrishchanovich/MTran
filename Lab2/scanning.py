def tokenize(code):
    tokens = []
    current_token = ''
    inside_string = False
    inside_comment = False
    line_number = 1
    char_position = 0

    i = 0
    while i < len(code):
        char = code[i]
        char_position += 1

        if char == '\n':
            line_number += 1
            char_position = 0
            inside_comment = False

        if char == '\\':
            if i + 1 < len(code):
                next_char = code[i + 1]
                if next_char in ('r', 'n', 't', '\\'):
                    current_token += char + next_char
                    i += 1
                else:
                    current_token += char
            else:
                current_token += char
        elif (char == '"' or char == "'") and not inside_string:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            current_token += char
            inside_string = True
        elif (char == '"' or char == "'") and inside_string:
            current_token += char
            tokens.append(current_token)
            current_token = ''
            inside_string = False
        elif inside_string:
            current_token += char
        elif char == '/' and i + 1 < len(code) and code[i + 1] == '/':
            if current_token:
                tokens.append(current_token)
                current_token = ''
            current_token += char + code[i + 1]
            i += 1
            tokens.append(current_token)
            current_token = ''
            i += 1
            while i < len(code) and code[i] != '\n':
                current_token += code[i]
                i += 1
            tokens.append(current_token.strip())
            current_token = ''
        elif char == '/' and i + 1 < len(code) and code[i + 1] == '*':
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append('/*')
            inside_comment = True
            i += 1
        elif char == '*' and i + 1 < len(code) and code[i + 1] == '/':
            if current_token:
                tokens.append(current_token)
                current_token = ''
            current_token = '*/'
            inside_comment = False
            tokens.append(current_token)
            current_token = ''
            i += 1
        elif inside_comment:
            current_token += char
        elif char == '#':
            current_token += char
            i += 1
            while i < len(code) and not code[i].isspace():
                current_token += code[i]
                i += 1
            tokens.append(current_token)
            current_token = ''
        elif char in ('(', ')', '{', '}', '[', ']', ',', ';', '<', '>'):
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
        elif char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ''
        elif char in ('(', ')', '{', '}', '[', ']', ',', ';', '<', '>'):
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
        elif char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ''
        elif char == '.':
            if current_token.isdigit() and i + 1 < len(code) and code[i + 1].isdigit():
                current_token += char
            elif current_token:
                tokens.append(current_token)
                tokens.append(char)
                current_token = ''
            else:
                tokens.append(char)
        elif char.isalnum() or char == '_':
            current_token += char
        elif char.isdigit() and i + 1 < len(code) and code[i + 1] in ('e', 'E'):
            current_token += char
            current_token += code[i + 1]
            i += 1
            if i + 1 < len(code) and code[i + 1] in ('+', '-'):
                current_token += code[i + 1]
                i += 1
            while i + 1 < len(code) and code[i + 1].isdigit():
                current_token += code[i + 1]
                i += 1
            tokens.append(current_token)
            current_token = ''
        elif char.isdigit() and current_token.endswith(('l', 'L', 'u', 'U')):
            tokens.append(current_token[:-1])
            tokens.append(current_token[-1])
            current_token = ''
            current_token += char
        elif current_token.endswith(('ll', 'LL', 'uu', 'UU', 'el', 'EL')):
            print('ct', current_token)
            tokens.append(current_token[:-2])
            tokens.append(current_token[-2])
            current_token = ''
            current_token += char
        else:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)

        i += 1

    if current_token:
        tokens.append(current_token)

    combined_tokens = []
    i = 0

    while i < len(tokens):
        if tokens[i - 1] == '#include' and tokens[i] == '<' and tokens[i + 1] != '<':
            end_index = i + 1
            while end_index < len(tokens) and tokens[end_index] != '>':
                end_index += 1

            if end_index < len(tokens) and tokens[end_index] == '>':
                combined_tokens.append('<' + ''.join(tokens[i + 1:end_index]) + '>')
                i = end_index + 1
        if tokens[i:i + 2] == ['<', '<']:
            combined_tokens.append('<<')
            i += 2
        elif tokens[i:i + 2] == ['>', '>']:
            combined_tokens.append('>>')
            i += 2
        elif tokens[i:i + 2] == [':', ':']:
            combined_tokens.append('::')
            i += 2
        elif tokens[i:i + 2] == ['-', '>']:
            combined_tokens.append('->')
            i += 2
        elif tokens[i:i + 2] == ['+', '+']:
            combined_tokens.append('++')
            i += 2
        elif tokens[i:i + 2] == ['-', '-']:
            combined_tokens.append('--')
            i += 2
        elif tokens[i:i + 2] == ['+', '=']:
            combined_tokens.append('+=')
            i += 2
        elif tokens[i:i + 2] == ['-', '=']:
            combined_tokens.append('-=')
            i += 2
        elif tokens[i:i + 2] == ['*', '=']:
            combined_tokens.append('*=')
            i += 2
        elif tokens[i:i + 2] == ['/', '=']:
            combined_tokens.append('/=')
            i += 2
        elif tokens[i:i + 2] == ['%', '=']:
            combined_tokens.append('%=')
            i += 2
        elif tokens[i:i + 2] == ['=', '=']:
            combined_tokens.append('==')
            i += 2
        elif tokens[i:i + 2] == ['!', '=']:
            combined_tokens.append('!=')
            i += 2
        elif tokens[i:i + 2] == ['>', '=']:
            combined_tokens.append('>=')
            i += 2
        elif tokens[i:i + 2] == ['<', '=']:
            combined_tokens.append('<=')
            i += 2
        elif tokens[i:i + 2] == ['>', '>']:
            combined_tokens.append('!=')
            i += 2
        elif tokens[i:i + 2] == ['&', '&']:
            combined_tokens.append('&&')
            i += 2
        elif tokens[i:i + 2] == ['|', '|']:
            combined_tokens.append('||')
            i += 2
        elif tokens[i:i + 3] == ['>', '>', '=']:
            combined_tokens.append('>>=')
            i += 3
        elif tokens[i:i + 3] == ['<', '<', '=']:
            combined_tokens.append('<<=')
            i += 3
        elif tokens[i:i + 2] == ['&', '=']:
            combined_tokens.append('&=')
            i += 2
        elif tokens[i:i + 2] == ['|', '=']:
            combined_tokens.append('|=')
            i += 2
        elif tokens[i:i + 2] == ['^', '=']:
            combined_tokens.append('^=')
            i += 2
        elif tokens[i:i + 2] == ['/', '/']:
            combined_tokens.append('//')
            i += 2
        elif tokens[i:i + 2] == ['/', '*']:
            combined_tokens.append('/*')
            i += 2
        elif tokens[i:i + 2] == ['*', '/']:
            combined_tokens.append('*/')
            i += 2
        elif tokens[i:i + 3] == ['unsigned', 'long', 'long']:
            combined_tokens.append('unsigned long long')
            i += 3
        elif tokens[i:i + 2] == ['unsigned', 'char']:
            combined_tokens.append('unsigned char')
            i += 2
        elif tokens[i:i + 2] == ['unsigned', 'short']:
            combined_tokens.append('unsigned short')
            i += 2
        elif tokens[i:i + 2] == ['unsigned', 'int']:
            combined_tokens.append('unsigned int')
            i += 2
        elif tokens[i:i + 2] == ['unsigned', 'long']:
            combined_tokens.append('unsigned long')
            i += 2
        elif tokens[i:i + 4] == ['unsigned', 'long', 'long', 'double']:
            combined_tokens.append('unsigned long long double')
            i += 4
        elif tokens[i:i + 2] == ['long', 'long']:
            combined_tokens.append('long long')
            i += 2
        elif tokens[i:i + 2] == ['long', 'int']:
            combined_tokens.append('long int')
            i += 2
        elif tokens[i:i + 2] == ['short', 'int']:
            combined_tokens.append('short int')
            i += 2
        elif tokens[i:i + 2] == ['long', 'double']:
            combined_tokens.append('long double')
            i += 2
        elif tokens[i:i + 2] == ['signed', 'char']:
            combined_tokens.append('signed char')
            i += 2
        else:
            combined_tokens.append(tokens[i])
            i += 1

    return combined_tokens
