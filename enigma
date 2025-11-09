# Konfiguration
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

rotors = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # Rotor I
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # Rotor II
    "BDFHJLCPRTXVZNYEIWGAKMUSQO",  # Rotor III
    "ESOVPZJAYQUIRHXLNFTGKDCMWB",  # Rotor IV
    "VZBRGITYUPSDNHLXAWMJQOFECK"   # Rotor V
]

reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# Funktionen
def encode_through_rotor(letter, rotor, position, ring_setting, reverse=False):
    index = alphabet.index(letter)
    shifted_index = (index + position - ring_setting) % 26
    if reverse:
        step_letter = alphabet[shifted_index]
        mapped_index = rotor.index(step_letter)
        output_index = (mapped_index - position + ring_setting + 26) % 26
    else:
        step_letter = rotor[shifted_index]
        output_index = (alphabet.index(step_letter) - position + ring_setting + 26) % 26
    return alphabet[output_index]

def reflect(letter):
    index = alphabet.index(letter)
    return reflector[index]

def plugboard_swap(letter, plugboard_pairs):
    for pair in plugboard_pairs:
        if letter in pair:
            return pair[1] if letter == pair[0] else pair[0]
    return letter

def rotate_rotors(positions):
    positions[0] = (positions[0] + 1) % 26
    if positions[0] == 0:
        positions[1] = (positions[1] + 1) % 26
        if positions[1] == 0:
            positions[2] = (positions[2] + 1) % 26

def encrypt_letter(letter, rotor_set, positions, ring_settings, plugboard_pairs):
    letter = plugboard_swap(letter, plugboard_pairs)

    for i in range(3):
        letter = encode_through_rotor(letter, rotor_set[i], positions[i], ring_settings[i], reverse=False)

    letter = reflect(letter)

    for i in reversed(range(3)):
        letter = encode_through_rotor(letter, rotor_set[i], positions[i], ring_settings[i], reverse=True)

    letter = plugboard_swap(letter, plugboard_pairs)
    return letter

def encrypt_message(message, rotor_set, start_positions, ring_settings, plugboard_pairs):
    encrypted = ""
    positions = start_positions[:]  # aktuelle Rotor-Positionen (veränderbar)

    for char in message:
        if char in alphabet:
            encrypted += encrypt_letter(char, rotor_set, positions, ring_settings, plugboard_pairs)
            rotate_rotors(positions)
    return encrypted

# Benutzereingaben
while True:
    rotor_input = input("Wähle drei Rotoren aus fünf (z.B. 1 3 4): ")
    rotor_nums = [int(n) for n in rotor_input.strip().split()]
    if len(rotor_nums) == 3 and all(1 <= n <= 5 for n in rotor_nums):
        break
    print("Ungültige Eingabe. Bitte drei Zahlen von 1 bis 5 eingeben.")

rotor_set = [rotors[n - 1] for n in rotor_nums]

while True:
    ring_input = input("Gib die drei Ringstellungen der Rotoren ein von 01 bis 26 (z.B. 16 04 23): ")
    ring_settings = [int(r) - 1 for r in ring_input.strip().split()]
    if len(ring_settings) == 3 and all(0 <= r <= 25 for r in ring_settings):
        break
    print("Ungültige Ringstellungen.")

while True:
    start_input = input("Gib die drei Startpositionen (A-Z) der Rotoren ein (z.B. A B C): ").upper()
    try:
        start_positions = [alphabet.index(c) for c in start_input.strip().split()]
        if len(start_positions) == 3:
            break
    except:
        pass
    print("Ungültige Startpositionen.")

plug_input = input("Gib bis 13 Steckerbrett-Paare (z. B. AB CD EF), oder leer lassen. Jeden Buchstaben max. einmnal verwenden. :").upper().strip()
plugboard_pairs = []
used_letters = set()

if plug_input:
    pairs = plug_input.split()
    for pair in pairs:
        if len(pair) == 2 and pair[0] in alphabet and pair[1] in alphabet:
            if pair[0] in used_letters or pair[1] in used_letters:
                print(f"Buchstabe {pair} doppelt verwendet! Ignoriere.")
                continue
            plugboard_pairs.append(pair)
            used_letters.update(pair)
        else:
            print(f"Ungültiges Paar: {pair}")

nachricht = input("Gib deine Nachricht ein (nur A-Z, ohne Umlaute): ").upper()
nachricht = ''.join([c for c in nachricht if c in alphabet])

verschlüsselt = encrypt_message(nachricht, rotor_set, start_positions, ring_settings, plugboard_pairs)
print("Verschlüsselte Nachricht:", verschlüsselt)

