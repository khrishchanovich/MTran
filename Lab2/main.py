from scanning import tokenize
from classification import classify_token
from function import read_code_from_file, write_output_to_file


file_path_input = 'test.cpp'
file_path_output = 'output.txt'


def balance_check(code):
    double_quotes_count = 0
    single_quotes_count = 0
    parentheses_count = 0
    curly_braces_count = 0
    comment_open_count = 0
    comment_close_count = 0

    in_string = False
    in_comment = False

    i = 0
    while i < len(code):
        char = code[i]

        if char == '"' and not in_comment:
            double_quotes_count += 1
            in_string = not in_string
        elif char == "'" and not in_comment:
            single_quotes_count += 1
            in_string = not in_string
        elif char == '(' and not in_comment and not in_string:
            parentheses_count += 1
        elif char == ')' and not in_comment and not in_string:
            parentheses_count -= 1
        elif char == '{' and not in_comment and not in_string:
            curly_braces_count += 1
        elif char == '}' and not in_comment and not in_string:
            curly_braces_count -= 1
        elif char == '/' and i < len(code) - 1 and code[i + 1] == '*' and not in_string:
            comment_open_count += 1
            in_comment = True
            i += 1
        elif char == '*' and i < len(code) - 1 and code[i + 1] == '/' and in_comment and not in_string:
            comment_close_count += 1
            in_comment = False
            i += 1

        i += 1

    if (double_quotes_count % 2 == 0 and
            single_quotes_count % 2 == 0 and
            parentheses_count == 0 and
            curly_braces_count == 0 and
            comment_open_count == comment_close_count):
        return True
    else:
        return False

def lexer():
    code = read_code_from_file(file_path_input)
    tokens = tokenize(code)
    token_table = {}
    table = dict()
    token_classification_list = []

    balance_errors = balance_check(code)
    if not balance_errors:
        print("SYNTAX ERROR")
    else:

        tokens = tokenize(code)
        token_table = {}
        for i, token in enumerate(tokens):
            classification = classify_token(token, tokens[i - 1] if i > 0 else None,
                                            tokens[i + 1] if i < len(tokens) - 1 else None, token_table)

            table[token] = classification


            token_classification_list.append((token, classification))
            #print(token, classification)
        output = ''
        output += "+----------------------------------------------------------------+\n"
        output += "|   №  |  Элемент               |   Информация                   |\n"
        output += "+----------------------------------------------------------------+\n"
        for i, token in enumerate(tokens):
            classification = classify_token(token, tokens[i - 1] if i > 0 else None,
                                         tokens[i + 1] if i < len(tokens) - 1 else None, token_table)
            output += f"|  {i:<3}   |{token:<23}            |{classification:<30}                      \n"
        output += "+----------------------------------------------------------------+\n"

        #print(token_table)
        write_output_to_file(output, file_path_output)

    return token_classification_list

if __name__ == "__main__":
    lexer()