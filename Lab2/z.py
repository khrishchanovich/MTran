import tkinter as tk
import requests
import json

def send_request():
    url = url_entry.get()
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на наличие ошибок в ответе
        content_type = response.headers.get('Content-Type')
        if 'application/json' in content_type:
            response_json = response.json()
            response_window = tk.Toplevel(root)
            response_window.title("Response")
            response_label = tk.Label(response_window, text=json.dumps(response_json, indent=4))
            response_label.pack()
        else:
            response_window = tk.Toplevel(root)
            response_window.title("Response")
            response_text = tk.Text(response_window)
            response_text.insert(tk.END, response.text)
            response_text.pack(fill=tk.BOTH, expand=True)
    except requests.exceptions.RequestException as e:
        error_label.config(text=str(e))
    except json.JSONDecodeError:
        error_label.config(text="Invalid JSON")


# Создание главного окна
root = tk.Tk()
root.title("HTTP Client")

# Создание элементов интерфейса
url_label = tk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=5, pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

send_button = tk.Button(root, text="Send Request", command=send_request)
send_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

error_label = tk.Label(root, text="", fg="red")
error_label.grid(row=2, column=0, columnspan=2)

# Запуск главного цикла приложения
root.mainloop()





def check_constants(token_table):
    constant_types = {'INTEGER', 'FLOAT', 'STRING'}
    constants = []

    for token, token_type in token_table:
        if token_type in constant_types:
            print('Constants:')
            print(f"{token} {token_type}")

    return constants

def check_variable(token_table):
    variables = []

    current_data_type = None
    current_variables = []

    i = 0
    while i < len(token_table):
        token, token_type = token_table[i]

        if token_type == 'DATA TYPE':
            current_data_type = token
        elif current_data_type is not None and token_type == f'VARIABLE ({current_data_type.upper()})':
            if current_data_type is not None:
                current_variables.append(token)
            else:
                print('SYNTAX ERROR!')
        elif token == ',':
            # Продолжаем собирать переменные в текущей группе
            if current_data_type is None:
                print('SYNTAX ERROR!')
            else:
                current_variables.append(token)
        elif token == ';':
            # Завершаем текущую группу объявления переменных и добавляем их в список
            if current_data_type is None or not current_variables:
                print('SYNTAX ERROR!')
            else:
                for var in current_variables:
                    variables.append((current_data_type, var))
                current_variables = []

        i += 1

    # Проверяем, что все группы завершены точкой с запятой
    if current_variables:
        print('SYNTAX ERROR!')

    print("Variable Declarations:")
    for data_type, variable in variables:
        print(f"{data_type} {variable}")



def check_function(token_table):
    variables = []

    current_data_type = None
    current_functions = []

    i = 0
    while i < len(token_table):
        token, token_type = token_table[i]
        if token_type == 'DATA TYPE':
            current_data_type = token
        elif token_type in (f'FUNCTION ({current_data_type.upper()})', f'FUNCTION (POINTER {current_data_type.upper()})'):
            current_functions.append(token)
        elif token == ';':
            for var in current_functions:
                variables.append((current_data_type, var))
            current_functions = []

        i += 1

    print("Variable Declarations:")
    for data_type, variable in variables:
        print(f"{data_type} {variable}")

# check_include(token_table)
# check_constants(token_table)
# check_variable(token_table)

def parse_program(token_table):
    check_include(token_table)
    check_constants(token_table)
    check_variable(token_table)
    check_function(token_table)

# parse_program(token_table)
