def read_code_from_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code

def write_output_to_file(output, file_path):
    with open(file_path, 'w') as file:
        file.write(output)