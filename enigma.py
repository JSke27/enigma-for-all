import streamlit as st

# -----------------------------
#   Konfiguration
# -----------------------------

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

rotors = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",  # Rotor I
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",  # Rotor II
    "BDFHJLCPRTXVZNYEIWGAKMUSQO",  # Rotor III
    "ESOVPZJAYQUIRHXLNFTGKDCMWB",  # Rotor IV
    "VZBRGITYUPSDNHLXAWMJQOFECK"   # Rotor V
]

reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


# -----------------------------
#   Funktionen
# -----------------------------

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

    # Vorwärts durch die 3 Rotoren
    for i in range(3):
        letter = encode_through_rotor(letter, rotor_set[i], positions[i], ring_settings[i], reverse=False)

    # Reflektor
    letter = reflect(letter)

    # Rückwärts durch die Rotoren
    for i in reversed(range(3)):
        letter = encode_through_rotor(letter, rotor_set[i], positions[i], ring_settings[i], reverse=True)

    letter = plugboard_swap(letter, plugboard_pairs)
    return letter


def encrypt_message(message, rotor_set, start_positions, ring_settings, plugboard_pairs):
    encrypted = ""
    positions = start_positions[:]

    for char in message:
        if char in alphabet:
            encrypted += encrypt_letter(char, rotor_set, positions, ring_settings, plugboard_pairs)
            rotate_rotors(positions)

    return encrypted


# -----------------------------
#   Streamlit UI
# -----------------------------

st.title("🔐 Enigma Maschine – Simulation in Python")

st.write("Diese Version basiert direkt auf deinem Originalcode, angepasst für Streamlit.")

# Rotorwahl
st.header("1) Rotoren auswählen")
available_rotors = ["Rotor I", "Rotor II", "Rotor III", "Rotor IV", "Rotor V"]

rotor_selection = st.multiselect(
    "Wähle genau 3 Rotoren:",
    options=list(range(1, 6)),
    format_func=lambda x: available_rotors[x-1],
    default=[1, 2, 3]
)

if len(rotor_selection) != 3:
    st.warning("Bitte genau 3 Rotoren auswählen!")
    st.stop()

rotor_set = [rotors[n - 1] for n in rotor_selection]

# Ringstellungen
st.header("2) Ringstellungen (01–26)")
ring_settings = []
cols = st.columns(3)
for i in range(3):
    r = cols[i].number_input(f"Ring {i+1}", 1, 26, 1)
    ring_settings.append(r - 1)

# Startpositionen
st.header("3) Startpositionen (A–Z)")
start_positions = []
cols = st.columns(3)
for i in range(3):
    pos = cols[i].text_input(f"Start {i+1}", "A")
    if len(pos) != 1 or pos.upper() not in alphabet:
        st.error("Ungültige Startposition!")
        st.stop()
    start_positions.append(alphabet.index(pos.upper()))

# Plugboard
st.header("4) Steckerbrett")
plug_input = st.text_input("Paare (Beispiel: AB CD EF)")

plugboard_pairs = []
used_letters = set()

if plug_input.strip():
    for pair in plug_input.upper().split():
        if len(pair) == 2 and pair[0] in alphabet and pair[1] in alphabet:
            if pair[0] in used_letters or pair[1] in used_letters:
                st.warning(f"Buchstaben bereits verbunden: {pair}")
                continue
            plugboard_pairs.append(pair)
            used_letters.update(pair)
        else:
            st.warning(f"Ungültiges Paar: {pair}")

# Nachricht
st.header("5) Nachricht")
msg = st.text_area("Nachricht (A–Z)", "").upper()
msg = ''.join([c for c in msg if c in alphabet])

# Start encryption
if st.button("🔐 Verschlüsseln"):
    if not msg:
        st.error("Bitte eine Nachricht eingeben!")
    else:
        verschlüsselt = encrypt_message(msg, rotor_set, start_positions, ring_settings, plugboard_pairs)
        st.success("Verschlüsselte Nachricht:")
        st.code(verschlüsselt)
