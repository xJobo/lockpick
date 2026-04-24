import re
import math

# liste noire de mots de passe trop courants (rockyou + fr)
COMMON_PASSWORDS = [
    # top mondial
    "123456", "password", "123456789", "12345678", "12345",
    "1234567", "1234567890", "qwerty", "abc123", "111111",
    "password1", "iloveyou", "sunshine", "princess", "football",
    "monkey", "shadow", "master", "666666", "qwertyuiop",
    "123321", "letmein", "696969", "dragon", "1234",
    "baseball", "trustno1", "batman", "access", "hello",
    "charlie", "donald", "loveme", "michael", "654321",
    "superman", "qazwsx", "jordan", "passw0rd", "welcome",
    "login", "admin", "starwars", "solo", "mustang",
    "lovely", "whatever", "000000", "121212", "888888",
    "password123", "zaq12wsx", "hunter2", "freedom", "killer",
    "soccer", "hockey", "ranger", "buster", "thomas",
    "tigger", "robert", "joshua", "matrix", "ginger",
    "pepper", "summer", "hammer", "george", "harley",
    "andrew", "cheese", "jessica", "mercedes", "phoenix",
    "andrea", "maverick", "nicole", "ashley", "thunder",
    "cowboy", "midnight", "chicken", "silver", "diamond",
    "cookie", "corvette", "samantha", "steelers", "joseph",
    "merlin", "london", "falcon", "garden", "kitten",
    "guitar", "butter", "dakota", "sparky", "computer",
    "yankees", "panther", "winter", "jackson", "compaq",
    # francais
    "azerty", "motdepasse", "soleil", "bonjour", "marseille",
    "nicolas", "jetaime", "chocolat", "camille", "doudou",
    "loulou", "paris", "amour", "coucou", "salut",
    "france", "alexandre", "maxime", "antoine", "julien",
    "pierre", "marine", "azertyuiop", "1234azerty", "azerty123",
    "mdp123", "motdepasse1", "chouchou", "papillon", "famille",
    "nathalie", "isabelle", "qwerty123", "pokemon", "naruto",
    "samsung", "internet",
    # classiques faibles
    "test", "test123", "pass", "pass123", "root",
    "toor", "changeme", "default", "guest", "temp",
    "temp123", "user", "demo", "qwer1234", "asdf1234",
]

def check_length(password):
    length = len(password)
    if length < 8:
        return 0, f"Trop court ({length} caractères — minimum 8)"
    elif length < 12:
        return 1, f"Longueur acceptable ({length} caractères)"
    elif length < 16:
        return 2, f"Bonne longueur ({length} caractères)"
    else:
        return 3, f"Excellente longueur ({length} caractères)"

def check_complexity(password):
    score = 0
    details = []

    if re.search(r'[a-z]', password):
        score += 1
        details.append("minuscules OK")
    else:
        details.append("pas de minuscules")

    if re.search(r'[A-Z]', password):
        score += 1
        details.append("majuscules OK")
    else:
        details.append("pas de majuscules")

    if re.search(r'[0-9]', password):
        score += 1
        details.append("chiffres OK")
    else:
        details.append("pas de chiffres")

    if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
        score += 1
        details.append("caractères spéciaux OK")
    else:
        details.append("pas de caractères spéciaux")

    return score, details

def estimate_crack_time(password):
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[0-9]', password): charset += 10
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password): charset += 32

    if charset == 0:
        return "instantané"

    # hypothese : 10 milliards de tentatives/sec (GPU moderne type hashcat)
    combinations = charset ** len(password)
    speed = 10_000_000_000
    seconds = combinations / speed

    if seconds < 1:
        return "moins d'une seconde"
    elif seconds < 60:
        return f"environ {seconds:.0f} secondes"
    elif seconds < 3600:
        return f"environ {seconds/60:.0f} minutes"
    elif seconds < 86400:
        return f"environ {seconds/3600:.1f} heures"
    elif seconds < 31536000:
        return f"environ {seconds/86400:.0f} jours"
    elif seconds < 3.15e9:
        return f"environ {seconds/31536000:.0f} ans"
    else:
        years = seconds / 31536000
        if years > 1e12:
            return "plus longtemps que l'âge de l'univers"
        return f"environ {years:.2e} ans"

def suggest_improvements(password, complexity_details):
    suggestions = []

    if len(password) < 12:
        suggestions.append("Allonge ton mot de passe à au moins 12 caractères")
    if "pas de majuscules" in complexity_details:
        suggestions.append("Ajoute au moins une lettre majuscule (ex: A, B, C...)")
    if "pas de chiffres" in complexity_details:
        suggestions.append("Ajoute des chiffres (ex: 1, 42, 99...)")
    if "pas de caractères spéciaux" in complexity_details:
        suggestions.append("Ajoute des caractères spéciaux (ex: @, #, !, $...)")
    if len(password) > 6 and password.lower() in [p.lower() for p in COMMON_PASSWORDS]:
        suggestions.append("Ce mot de passe est trop courant — change-le complètement")

    return suggestions

def analyze_password(password):
    print("\n" + "=" * 50)
    print(f"  Analyse : '{password}'")
    print("=" * 50)

    # verif blacklist
    if password.lower() in [p.lower() for p in COMMON_PASSWORDS]:
        print("\n[!] ALERTE : Ce mot de passe est dans la liste des plus utilisés !")
        print("    Il serait cracké en moins d'une seconde par dictionnaire.\n")

    total_score = 0

    # longueur
    length_score, length_msg = check_length(password)
    total_score += length_score
    print(f"\n[Longueur]     {length_msg}")

    # complexite
    complexity_score, complexity_details = check_complexity(password)
    total_score += complexity_score
    print(f"[Complexité]   {', '.join(complexity_details)}")

    # temps de crack
    crack_time = estimate_crack_time(password)
    print(f"[Temps crack]  {crack_time}")

    # score final /7
    if total_score <= 2:
        niveau = "FAIBLE"
    elif total_score <= 4:
        niveau = "MOYEN"
    elif total_score <= 6:
        niveau = "FORT"
    else:
        niveau = "TRÈS FORT"

    print(f"\n[Score]        {total_score}/7 — {niveau}")

    # conseils
    suggestions = suggest_improvements(password, complexity_details)
    if suggestions:
        print("\n[Conseils]")
        for s in suggestions:
            print(f"  • {s}")
    else:
        print("\n[Conseils]     Aucun — excellent mot de passe !")

    print("=" * 50 + "\n")

def main():
    print("\n=== Lockpick — testeur de robustesse ===")
    print("Tape 'quitter' pour arrêter.\n")

    while True:
        password = input("Mot de passe à tester : ")
        if password.lower() == "quitter":
            print("Au revoir !")
            break
        if not password:
            print("Mot de passe vide, réessaie.")
            continue
        analyze_password(password)

if __name__ == "__main__":
    main()
