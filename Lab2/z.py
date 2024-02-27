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
