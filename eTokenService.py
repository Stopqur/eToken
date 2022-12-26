import binascii
import pkcs11

from resources import DLL_PATH, TOKEN_LABEL, DESCRIPTION
from exceptions import TokenDisconnected


class ETokenService:
    def __init__(self):
        self.lib = pkcs11.lib(DLL_PATH)
        self.token = None
        self.session = None
        self.key = None

    def initialize(self):
        try:
            self.token = self.lib.get_token(token_label=TOKEN_LABEL)
            return self.token
        except pkcs11.exceptions.NoSuchToken:
            self.token = None
            return None

    def is_token_active(self) -> bool:
        # неявно создаем объект токена
        try:
            self.token = self.lib.get_token(token_label=TOKEN_LABEL)
            return True
        except pkcs11.exceptions.NoSuchToken:
            self.token = None
            return False

    def get_slots_description(self) -> str:
        if not self.is_token_active():
            raise TokenDisconnected
        slots = self.lib.get_slots_description()
        messages = [
            f'Id: {slot.slot_id}\n'
            f'{DESCRIPTION}: {slot.slot_description}\n\n'
            for slot in slots
            if slot  # if slot is None: continue
            if slot.slot_description
        ]
        return '\n'.join(messages)

    def get_slot_description(self):
        if not self.is_token_active():
            raise TokenDisconnected
        return str(self.token.slot)

    def get_token_description(self):
        if not self.is_token_active():
            raise TokenDisconnected
        return (
            f'manufacturer_id: {self.token.manufacturer_id}\n'
            f'model: {self.token.model}\n'
            f'serial: {self.token.serial.decode()}'
        )

    def login(self):
        if not self.is_token_active():
            raise TokenDisconnected
        self.session = self.token.open(rw=True, user_pin='1234567890')
        return self.session

    def generate_key(self):
        if not self.is_token_active():
            raise TokenDisconnected
        self.key = self.session.generate_key(pkcs11.KeyType.DES3)
        return self.key

    def encrypt(self, input_data):
        if not self.is_token_active():
            raise TokenDisconnected

        cypher_text = self.key.encrypt(input_data.encode())
        hex_encrypted_data = binascii.hexlify(cypher_text)
        return hex_encrypted_data.decode()

    def decrypt(self, hex_input_data):
        if not self.is_token_active():
            raise TokenDisconnected

        data_to_decode = binascii.unhexlify(hex_input_data.encode())
        decrypted_data = self.key.decrypt(data_to_decode)
        return decrypted_data.decode()

    def logout(self):
        if not self.is_token_active():
            raise TokenDisconnected
        self.session.close()
        self.session = None
        self.key = None
