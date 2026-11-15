

import os
import json
import base64
import secrets
import string
import hashlib

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class PasswordApp(App):

    def build(self):
        self.file = os.path.join(self.user_data_dir, "vault.json")
        self.entries = []
        self.key = None

        self.root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        self.title = Label(
            text="BACHARTELB PASSWORD GENERATOR PRO",
            font_size=20
        )
        self.root.add_widget(self.title)

        self.show_login()
        return self.root

    def clear(self):
        self.root.clear_widgets()
        self.root.add_widget(self.title)

    def field(self, hint, password=False):
        return TextInput(
            hint_text=hint,
            password=password,
            multiline=False,
            size_hint_y=None,
            height=48
        )

    def button(self, text, callback):
        b = Button(text=text, size_hint_y=None, height=48)
        b.bind(on_press=callback)
        self.root.add_widget(b)

    def derive_key(self, master, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=600000
        )
        return base64.urlsafe_b64encode(kdf.derive(master.encode()))

    def show_login(self):
        self.clear()

        if not os.path.exists(self.file):
            self.root.add_widget(Label(
                text="Crée ton coffre-fort"
            ))
            self.master = self.field(
                "Mot de passe principal",
                True
            )
            self.pin = self.field("PIN de 6 chiffres", True)
            self.root.add_widget(self.master)
            self.root.add_widget(self.pin)
            self.button("CREER MON COFFRE", self.create_vault)
        else:
            self.root.add_widget(Label(
                text="Déverrouiller le coffre"
            ))
            self.master = self.field(
                "Mot de passe principal",
                True
            )
            self.pin = self.field("PIN de 6 chiffres", True)
            self.root.add_widget(self.master)
            self.root.add_widget(self.pin)
            self.button("OUVRIR", self.unlock)

    def create_vault(self, instance):
        master = self.master.text
        pin = self.pin.text

        if len(master) < 12:
            self.message(
                "Le mot de passe principal doit avoir au moins 12 caractères."
            )
            return

        if len(pin) != 6 or not pin.isdigit():
            self.message("Le PIN doit contenir 6 chiffres.")
            return

        salt = secrets.token_bytes(16)
        self.key = self.derive_key(master, salt)
        self.entries = []

        data = Fernet(self.key).encrypt(
            json.dumps(self.entries).encode()
        )

        with open(self.file, "w") as f:
            json.dump({
                "salt": base64.b64encode(salt).decode(),
                "pin_hash": hashlib.sha256(pin.encode()).hexdigest(),
                "data": data.decode()
            }, f)

        self.show_home()

    def unlock(self, instance):
        try:
            with open(self.file, "r") as f:
                saved = json.load(f)

            pin = self.pin.text
            if hashlib.sha256(pin.encode()).hexdigest() != saved["pin_hash"]:
                self.message("PIN incorrect.")
                return

            salt = base64.b64decode(saved["salt"])
            self.key = self.derive_key(self.master.text, salt)

            encrypted = saved["data"].encode()
            plain = Fernet(self.key).decrypt(encrypted)
            self.entries = json.loads(plain.decode())

            self.show_home()

        except (InvalidToken, ValueError, KeyError):
            self.message("Mot de passe principal incorrect.")
        except Exception:
            self.message("Impossible d'ouvrir le coffre.")

    def save_vault(self):
        with open(self.file, "r") as f:
            saved = json.load(f)

        encrypted = Fernet(self.key).encrypt(
            json.dumps(self.entries).encode()
        )

        saved["data"] = encrypted.decode()

        with open(self.file, "w") as f:
            json.dump(saved, f)

    def show_home(self):
        self.clear()

        self.root.add_widget(Label(
            text="TON COFFRE-FORT"
        ))

        self.account = self.field("Nom du compte")
        self.password = self.field("Mot de passe", True)
        self.root.add_widget(self.account)
        self.root.add_widget(self.password)

        self.button("ENREGISTRER", self.add_entry)
        self.button("RECHERCHER", self.search_entry)
        self.button("GENERER UN MOT DE PASSE", self.generate)
        self.button("AFFICHER TOUS LES COMPTES", self.show_entries)
        self.button("VERROUILLER", self.lock)

    def add_entry(self, instance):
        name = self.account.text.strip()
        password = self.password.text

        if not name or not password:
            self.message("Remplis les deux champs.")
            return

        self.entries.append({
            "account": name,
            "password": password
        })

        self.save_vault()
        self.account.text = ""
        self.password.text = ""
        self.message("Mot de passe enregistré.")

    def search_entry(self, instance):
        query = self.account.text.strip().lower()

        matches = [
            item for item in self.entries
            if query in item["account"].lower()
        ]

        if not matches:
            self.message("Aucun compte trouvé.")
            return

        item = matches[0]
        self.password.text = item["password"]
        self.message("Compte trouvé : " + item["account"])

    def show_entries(self, instance):
        names = [
            item["account"] for item in self.entries
        ]
        self.message(
            "Comptes enregistrés :\n" +
            ("\n".join(names) if names else "Aucun compte")
        )

    def generate(self, instance):
        chars = string.ascii_letters + string.digits + "!@#$%&*"
        password = "".join(
            secrets.choice(chars) for _ in range(20)
        )
        self.password.text = password

    def lock(self, instance):
        self.key = None
        self.entries = []
        self.show_login()

    def message(self, text):
        popup = Popup(
            title="BACHARTELB",
            content=Label(text=text),
            size_hint=(0.85, 0.4)
        )
        popup.open()


if __name__ == "__main__":
    PasswordApp().run()
