from kivy.app import App
from kivy.uix.label import Label
from cryptography.fernet import Fernet

class TestApp(App):
    def build(self):
        key = Fernet.generate_key()
        return Label(text="Cryptography fonctionne !")

TestApp().run()
