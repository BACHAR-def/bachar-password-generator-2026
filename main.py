
import os
import json
import string
import secrets

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window

from cryptography.fernet import Fernet


class BacharApp(App):

    def build(self):
        self.title = "BACHARTELB PASSWORD GENERATOR PRO"

        Window.clearcolor = (0.04, 0.04, 0.06, 1)

        os.makedirs(self.user_data_dir, exist_ok=True)

        self.key_file = os.path.join(
            self.user_data_dir, "secret.key"
        )
        self.history_file = os.path.join(
            self.user_data_dir, "history.dat"
        )

        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)

        self.crypto = Fernet(key)
        self.history = []
        self.load_history()

        root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        root.add_widget(Label(
            text="[b]BACHARTELB[/b]",
            markup=True,
            font_size=30,
            color=(1, 0.75, 0, 1),
            size_hint_y=None,
            height=60
        ))

        root.add_widget(Label(
            text="PASSWORD GENERATOR PRO",
            font_size=17,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=35
        ))

        self.password_input = TextInput(
            hint_text="Votre mot de passe",
            multiline=False,
            size_hint_y=None,
            height=55,
            font_size=17
        )
        root.add_widget(self.password_input)

        self.status = Label(
            text="Bienvenue dans BACHARTELB PRO",
            size_hint_y=None,
            height=40
        )
        root.add_widget(self.status)

        self.add_button(
            root, "GENERER UN MOT DE PASSE",
            self.generate_password
        )

        self.add_button(
            root, "ENREGISTRER",
            self.save_password
        )

        self.add_button(
            root, "COPIER",
            self.copy_password
        )

        self.add_button(
            root, "SHOW HISTORY",
            self.show_history
        )

        root.add_widget(Label(
            text="SECURED WITH FERNET ENCRYPTION",
            color=(1, 0.75, 0, 1),
            font_size=12
        ))

        return root

    def add_button(self, layout, text, callback):
        btn = Button(
            text=text,
            size_hint_y=None,
            height=55,
            background_normal="",
            background_color=(0.55, 0.38, 0.05, 1),
            color=(1, 1, 1, 1),
            font_size=15
        )
        btn.bind(on_press=callback)
        layout.add_widget(btn)

    def generate_password(self, instance):
        characters = (
            string.ascii_letters
            + string.digits
            + "!@#$%&*?"
        )

        password = "".join(
            secrets.choice(characters)
            for _ in range(20)
        )

        self.password_input.text = password
        self.status.text = "Mot de passe genere !"

    def save_password(self, instance):
        password = self.password_input.text.strip()

        if not password:
            self.status.text = "Entrez un mot de passe !"
            return

        self.history.append(password)
        self.save_history()
        self.status.text = "Mot de passe enregistre !"

    def copy_password(self, instance):
        password = self.password_input.text

        if password:
            Clipboard.copy(password)
            self.status.text = "Mot de passe copie !"
        else:
            self.status.text = "Aucun mot de passe !"

    def save_history(self):
        data = json.dumps(self.history).encode("utf-8")
        encrypted = self.crypto.encrypt(data)

        with open(self.history_file, "wb") as f:
            f.write(encrypted)

    def load_history(self):
        if not os.path.exists(self.history_file):
            return

        try:
            with open(self.history_file, "rb") as f:
                encrypted = f.read()

            data = self.crypto.decrypt(encrypted)
            self.history = json.loads(
                data.decode("utf-8")
            )
        except Exception:
            self.history = []

    def show_history(self, instance):
        content = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        history_text = "\n\n".join(self.history[-20:])

        if not history_text:
            history_text = "Aucun mot de passe enregistre."

        display = TextInput(
            text=history_text,
            readonly=True,
            multiline=True
        )

        content.add_widget(display)

        close_btn = Button(
            text="FERMER",
            size_hint_y=None,
            height=50
        )

        content.add_widget(close_btn)

        popup = Popup(
            title="PASSWORD HISTORY",
            content=content,
            size_hint=(0.9, 0.8)
        )

        close_btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    BacharApp().run()

    
