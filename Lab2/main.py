from scanning import tokenize
from classification import classify_token
from function import read_code_from_file, write_output_to_file

file_path_input = 'test.cpp'
file_path_output = 'output.txt'

if __name__ == "__main__":
    code = read_code_from_file(file_path_input)
    tokens = tokenize(code)
    token_table = {}
    for i, token in enumerate(tokens):
        classification = classify_token(token, tokens[i - 1] if i > 0 else None,
                                                                        tokens[i + 1] if i < len(tokens) - 1 else None, token_table)

        print(token, classification)
    output = ''
    output += "+----------------------------------------------------------------+\n"
    output += "|   №  |  Элемент               |   Информация                   |\n"
    output += "+----------------------------------------------------------------+\n"
    for i, token in enumerate(tokens):
        classification = classify_token(token, tokens[i - 1] if i > 0 else None,
                                        tokens[i + 1] if i < len(tokens) - 1 else None, token_table)
        output += f"|  {i:<3}   |{token:<23}            |{classification:<30}                      \n"
    output += "+----------------------------------------------------------------+\n"

    print(token_table)
    write_output_to_file(output, file_path_output)
