
def tokenize(code):
    tokens = []
    current_token = ''
    inside_string = False
    line_number = 1
    char_position = 0

    i = 0
    while i < len(code):
        char = code[i]
        char_position += 1
        if char == '\n':
            line_number += 1
            char_position = 0

        # Обработка экранированных последовательностей
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
        elif char in ('(', ')', '{', '}', '[', ']', ',', ';') and not inside_string:
            if current_token:
                tokens.append(current_token)
            tokens.append(char)
            current_token = ''
        elif char.isspace() and not inside_string:
            if current_token:
                tokens.append(current_token)
                current_token = ''
        elif char == '"' and not inside_string:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            current_token += char
            inside_string = True
        elif char == '"' and inside_string:
            current_token += char
            tokens.append(current_token)
            current_token = ''
            inside_string = False
        elif char.isdigit() and not inside_string:
            if current_token and '.' not in current_token and current_token[-1].isdigit():
                current_token += char
            elif current_token and '.' in current_token:
                current_token += char
            else:
                if current_token:
                    tokens.append(current_token)
                current_token = char
        elif char in ('+', '-') and (not current_token or current_token[-1] not in ('+', '-', ' ')):
            if current_token:
                tokens.append(current_token)
                current_token = ''
            current_token += char
        elif char.isalnum() or char == '_':
            current_token += char
        else:
            current_token += char

            # Разделение токена, если это многосимвольный оператор или идентификатор
            if current_token in ('++', '--', '<<', '>>'):
                tokens.append(current_token)
                current_token = ''

        i += 1

    if current_token:
        tokens.append(current_token)

    # Объединяем типы данных 'long long', 'unsigned char', 'unsigned short', 'unsigned int',
    # 'unsigned long', 'unsigned long long', 'long double', 'signed char' в один токен
    combined_tokens = []
    i = 0
    while i < len(tokens):
        if tokens[i:i+3] == ['unsigned', 'long', 'long']:
            combined_tokens.append('unsigned long long')
            i += 3
        elif tokens[i:i+2] == ['unsigned', 'char']:
            combined_tokens.append('unsigned char')
            i += 2
        elif tokens[i:i+2] == ['unsigned', 'short']:
            combined_tokens.append('unsigned short')
            i += 2
        elif tokens[i:i+2] == ['unsigned', 'int']:
            combined_tokens.append('unsigned int')
            i += 2
        elif tokens[i:i+2] == ['unsigned', 'long']:
            combined_tokens.append('unsigned long')
            i += 2
        elif tokens[i:i+4] == ['unsigned', 'long', 'long', 'double']:
            combined_tokens.append('unsigned long long double')
            i += 4
        elif tokens[i:i+2] == ['long', 'long']:
            combined_tokens.append('long long')
            i += 2
        elif tokens[i:i+2] == ['long', 'double']:
            combined_tokens.append('long double')
            i += 2
        elif tokens[i:i+2] == ['signed', 'char']:
            combined_tokens.append('signed char')
            i += 2
        else:
            combined_tokens.append(tokens[i])
            i += 1

    return combined_tokens