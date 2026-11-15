import secrets
import string

def generer_mot_de_passe(longueur=16):
    caracteres = (
        string.ascii_letters
        + string.digits
        + "!@#$%&*"
    )
    return ''.join(
        secrets.choice(caracteres)
        for _ in range(longueur)
    )

print("=== BACHAR PASSWORD GENERATOR ===")
longueur = int(input("Longueur du mot de passe : "))

if longueur < 12:
    print("Choisissez au moins 12 caracteres.")
else:
    print("Votre mot de passe :",
          generer_mot_de_passe(longueur))
  
