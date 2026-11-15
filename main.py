
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
import secrets
import string


class PasswordApp(App):
    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        layout.add_widget(Label(
            text="BACHAR PASSWORD GENERATOR PRO",
            font_size=22
        ))

        self.length = TextInput(
            hint_text="Longueur du mot de passe",
            input_filter="int",
            multiline=False
        )
        layout.add_widget(self.length)

        self.result = Label(text="Votre mot de passe")
        layout.add_widget(self.result)

        generate_button = Button(text="GENERER")
        generate_button.bind(on_press=self.generate)
        layout.add_widget(generate_button)

        copy_button = Button(text="COPIER LE MOT DE PASSE")
        copy_button.bind(on_press=self.copy_password)
        layout.add_widget(copy_button)

        self.password = ""

        return layout

    def generate(self, instance):
        try:
            n = int(self.length.text)

            if n < 12 or n > 128:
                self.result.text = "Choisissez entre 12 et 128"
                self.password = ""
                return

            chars = string.ascii_letters + string.digits + "!@#$%&*"
            self.password = ''.join(
                secrets.choice(chars) for _ in range(n)
            )
            self.result.text = self.password

        except ValueError:
            self.result.text = "Entrez une longueur valide"
            self.password = ""

    def copy_password(self, instance):
        if self.password:
            Clipboard.copy(self.password)
            self.result.text = "Mot de passe copié !"
        else:
            self.result.text = "Générez d'abord un mot de passe"


if __name__ == "__main__":
    PasswordApp().run()
