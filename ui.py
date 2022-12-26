"""
    В данном файле находится верстка
"""
from tkinter import (
    Button,
    Entry,
    Tk,
    ttk,
    DISABLED,
    BOTH
)
from resources import (
    STATE,
    SLOTS_BUTTON_TEXT,
    SLOT_BUTTON_TEXT,
    TOKEN_BUTTON_TEXT,
    OPEN_SESSION_BUTTON_TEXT,
    GENERATE_KEY_BUTTON_TEXT,
    ENCRYPT_BUTTON_TEXT,
    DECRYPT_BUTTON_TEXT,
    BUTTON_TEXT,
    LAB_TITLE,
    TAB_INFO_TEXT,
    TAB_ENCRYPT_TEXT,
)


class LabUI(Tk):
    def __init__(self):
        super().__init__()
        self.title(LAB_TITLE)

        self.tabs_container = ttk.Notebook(self)  # Менеджер табов
        self.tab_info = ttk.Frame(self.tabs_container)  # Вкладка с инфой о токене
        self.tab_encrypt = ttk.Frame(self.tabs_container)  # Вкладка с шифрованием
        self.tabs_container.add(self.tab_info, text=TAB_INFO_TEXT)
        self.tabs_container.add(self.tab_encrypt, text=TAB_ENCRYPT_TEXT)
        self.tabs_container.pack(expand=1, fill=BOTH)

        self.slots_button = Button(self.tab_info, text=SLOTS_BUTTON_TEXT)
        self.slots_button.grid(column=0, row=0, padx=15, pady=15)

        self.slot_button = Button(self.tab_info, text=SLOT_BUTTON_TEXT)
        self.slot_button.grid(column=0, row=1, padx=15, pady=15)

        self.token_button = Button(self.tab_info, text=TOKEN_BUTTON_TEXT)
        self.token_button.grid(column=0, row=2, padx=15, pady=15)

        self.open_session_button = Button(self.tab_encrypt, text=OPEN_SESSION_BUTTON_TEXT)
        self.open_session_button.grid(column=1, row=0, padx=15, pady=15)

        self.generate_key_button = Button(self.tab_encrypt, text=GENERATE_KEY_BUTTON_TEXT)
        self.generate_key_button.grid(column=2, row=0, padx=15, pady=15)
        self.generate_key_button[STATE] = DISABLED

        self.encrypt_input = Entry(self.tab_encrypt, width=50)  # Текствое поле
        self.encrypt_input.grid(column=1, row=1, padx=15, pady=15)
        self.encrypt_button = Button(self.tab_encrypt, text=ENCRYPT_BUTTON_TEXT)
        self.encrypt_button.grid(column=2, row=1, padx=15, pady=15)
        self.encrypt_button[STATE] = DISABLED

        self.decrypt_input = Entry(self.tab_encrypt, width=50)  # Текствое поле
        self.decrypt_input.grid(column=1, row=2, padx=15, pady=15)
        self.decrypt_button = Button(self.tab_encrypt, text=DECRYPT_BUTTON_TEXT)
        self.decrypt_button.grid(column=2, row=2, padx=15, pady=15)
        self.decrypt_button[STATE] = DISABLED

        self.close_session_button = Button(self.tab_encrypt, text=BUTTON_TEXT)
        self.close_session_button.grid(column=1, row=7, padx=15, pady=15)
        self.close_session_button[STATE] = DISABLED

        self.resizable(False, False)

    def move_to_foreground(self): # вывести окно на первый план
        self.lift()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes, '-topmost', False)
