import pkcs11  # Библиотека для работы с Etoken
import binascii
from tkinter import (
    messagebox,
    NORMAL,
    DISABLED,
    COMMAND,
    END,
)
from resources import (
    ERROR_TITLE,
    INFO_TITLE,
    DESCRIPTION,
    STATE,
    EMPTY_INPUT_ERROR_MESSAGE,
    E_TOKEN_NOT_FOUND_MESSAGE,
    SESSION_OPEN_MESSAGE,
    KEY_WAS_CREATED_MESSAGE,
    INVALID_CYPHERTEXT_MESSAGE,
    SESSION_CLOSED_MESSAGE,
)
from eTokenService import ETokenService
from ui import LabUI
from exceptions import TokenDisconnected, EmtpyInputError


class ExceptDecorator:
    @staticmethod
    def except_token_disconnected(func):
        def inner(self):
            try:
                func(self)
            except TokenDisconnected:
                ExceptDecorator.show_token_not_found_error()
                self.open_session_button[STATE] = NORMAL
                self.generate_key_button[STATE] = DISABLED
                self.encrypt_button[STATE] = DISABLED
                self.decrypt_button[STATE] = DISABLED
                self.close_session_button[STATE] = DISABLED
                self.clear_inputs()
        return inner

    @staticmethod
    def show_token_not_found_error() -> None:
        messagebox.showerror(ERROR_TITLE, E_TOKEN_NOT_FOUND_MESSAGE)


class UiLogicalExtension(LabUI):
    def __init__(self, eToken_service: ETokenService) -> None:
        super().__init__()
        self.lib = pkcs11.lib('C:\\Windows\\System32\\eTPKCS11.dll')
        self.eToken_service = eToken_service
        self.slots_button[COMMAND] = self.show_slots
        self.slot_button[COMMAND] = self.show_slot
        self.token_button[COMMAND] = self.show_token
        self.open_session_button[COMMAND] = self.open_session
        self.generate_key_button[COMMAND] = self.generate_key
        self.encrypt_button[COMMAND] = self.encrypt
        self.decrypt_button[COMMAND] = self.decrypt
        self.close_session_button[COMMAND] = self.close_session

    @staticmethod
    def show_error(message: str) -> None:
        messagebox.showerror(ERROR_TITLE, message)

    @staticmethod
    def show_empty_input_error() -> None:
        messagebox.showerror(ERROR_TITLE, EMPTY_INPUT_ERROR_MESSAGE)

    @staticmethod
    def show_info(message: str) -> None:
        messagebox.showinfo(INFO_TITLE, message)

    @ExceptDecorator.except_token_disconnected
    def show_slot(self) -> None:
        self.show_info(self.eToken_service.get_slot_description())

    @ExceptDecorator.except_token_disconnected
    def show_slots(self) -> None:
        self.show_info(self.lib.get_slots())

    @ExceptDecorator.except_token_disconnected
    def show_token(self) -> None:
        self.show_info(self.eToken_service.get_token_description())

    @ExceptDecorator.except_token_disconnected
    def open_session(self) -> None:
        self.eToken_service.login()
        self.show_info(SESSION_OPEN_MESSAGE)
        self.generate_key_button[STATE] = NORMAL
        self.close_session_button[STATE] = NORMAL
        self.open_session_button[STATE] = DISABLED

    @ExceptDecorator.except_token_disconnected
    def generate_key(self) -> None:
        self.eToken_service.generate_key()
        self.show_info(KEY_WAS_CREATED_MESSAGE)
        self.encrypt_button[STATE] = NORMAL
        self.decrypt_button[STATE] = NORMAL

    @ExceptDecorator.except_token_disconnected
    def encrypt(self) -> None:
        try:
            plain_text = self.encrypt_input.get()
            if not plain_text:
                raise EmtpyInputError
            hex_encrypted_data = self.eToken_service.encrypt(plain_text)
            self.show_info(hex_encrypted_data)

            self.clipboard_clear()
            self.clipboard_append(hex_encrypted_data)
        except EmtpyInputError:
            self.show_empty_input_error()

    @ExceptDecorator.except_token_disconnected
    def decrypt(self) -> None:
        try:
            hex_cypher_text = self.decrypt_input.get()
            if not hex_cypher_text:
                raise EmtpyInputError
            decrypted_text = self.eToken_service.decrypt(hex_cypher_text)
            self.show_info(decrypted_text)

            self.clipboard_clear()
            self.clipboard_append(decrypted_text)
        except EmtpyInputError:
            self.show_empty_input_error()
        except binascii.Error:
            self.show_error(INVALID_CYPHERTEXT_MESSAGE)

    @ExceptDecorator.except_token_disconnected
    def close_session(self) -> None:
        self.eToken_service.logout()
        self.show_info(SESSION_CLOSED_MESSAGE)
        self.open_session_button[STATE] = NORMAL
        self.generate_key_button[STATE] = DISABLED
        self.encrypt_button[STATE] = DISABLED
        self.decrypt_button[STATE] = DISABLED
        self.close_session_button[STATE] = DISABLED
        self.clear_inputs()

    def clear_inputs(self):
        self.encrypt_input.delete(0, END)
        self.decrypt_input.delete(0, END)
        self.tab_encrypt.focus_set()


if __name__ == '__main__':
    eToken_service = ETokenService()
    eToken_service.initialize()
    app = UiLogicalExtension(eToken_service)
    app.move_to_foreground()
    app.mainloop()
