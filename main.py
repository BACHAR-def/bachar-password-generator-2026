from kivy.app import App
from kivy.uix.label import Label
from cryptography.fernet import Fernet

class TestApp(App):
    def build(self):
        key = Fernet.generate_key()
        cipher = Fernet(key)

        return Label(
            text="Cryptography fonctionne !",
            font_size=25
        )

if __name__ == "__main__":
    TestApp().run()
    
