import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор Паролей Pro")
        self.root.geometry("600x450")
        self.root.resizable(True, True)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        self.configure_styles()

    def configure_styles(self):
        self.style.configure('TFrame', background='#F5F5F5')
        self.style.configure('TLabel', background='#F5F5F5', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'), foreground='#2C3E50')
        self.style.configure('Result.TEntry', font=('Courier', 12), padding=5)
        self.style.configure('History.TFrame', background='#FFFFFF', borderwidth=1, relief='sunken')

    def create_widgets(self):
        # Основной контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Заголовок
        header = ttk.Label(main_frame, text="Генератор Безопасных Паролей", style='Header.TLabel')
        header.pack(pady=(0, 15))

        # Параметры генерации
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=5)

        self.length_var = tk.IntVar(value=12)
        ttk.Label(options_frame, text="Длина пароля:").grid(row=0, column=0, sticky=tk.W)
        self.length_spin = ttk.Spinbox(options_frame, from_=4, to=128, textvariable=self.length_var, width=5)
        self.length_spin.grid(row=0, column=1, padx=5, sticky=tk.W)

        self.include_upper = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Верхний регистр (A-Z)", variable=self.include_upper).grid(row=1, column=0, columnspan=2, sticky=tk.W)

        self.include_lower = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Нижний региров (a-z)", variable=self.include_lower).grid(row=2, column=0, columnspan=2, sticky=tk.W)

        self.include_digits = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Цифры (0-9)", variable=self.include_digits).grid(row=3, column=0, columnspan=2, sticky=tk.W)

        self.include_symbols = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Символы (!@#...)", variable=self.include_symbols).grid(row=4, column=0, columnspan=2, sticky=tk.W)

        # Кнопки генерации
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Сгенерировать", command=self.generate_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Копировать", command=self.copy_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить", command=self.clear_history).pack(side=tk.LEFT, padx=5)

        # Поле результата
        self.result_var = tk.StringVar()
        result_entry = ttk.Entry(main_frame, textvariable=self.result_var, style='Result.TEntry', width=40)
        result_entry.pack(pady=10)
        result_entry.bind('<FocusIn>', self.select_all_text)

        # История паролей
        history_frame = ttk.Frame(main_frame, style='History.TFrame')
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=6, wrap=tk.WORD, 
                                                    font=('Consolas', 9), padx=10, pady=10)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        self.history_text.configure(state='disabled')

    def generate_password(self):
        try:
            length = self.length_var.get()
            if length < 4:
                messagebox.showwarning("Ошибка", "Минимальная длина пароля - 4 символа")
                return

            characters = []
            if self.include_upper.get(): characters.extend(string.ascii_uppercase)
            if self.include_lower.get(): characters.extend(string.ascii_lowercase)
            if self.include_digits.get(): characters.extend(string.digits)
            if self.include_symbols.get(): characters.extend("!@#$%^&*()_+-=[]{}|;:,.<>?")

            if not characters:
                messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов")
                return

            password = ''.join(random.choices(characters, k=length))
            self.result_var.set(password)
            self.update_history(password)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def copy_password(self):
        password = self.result_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")

    def clear_history(self):
        self.history_text.configure(state='normal')
        self.history_text.delete(1.0, tk.END)
        self.history_text.configure(state='disabled')

    def update_history(self, password):
        self.history_text.configure(state='normal')
        self.history_text.insert(tk.END, f"- {password}\n")
        self.history_text.see(tk.END)
        self.history_text.configure(state='disabled')

    def select_all_text(self, event):
        event.widget.select_range(0, tk.END)
        return 'break'

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
