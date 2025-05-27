
import string

ALPHABET = string.ascii_uppercase

# Historical Enigma I rotors and Reflector B
ROTOR_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

def shift_index(i, shift):
    return (i + shift) % 26

def apply_plugboard(char, plugboard):
    return plugboard.get(char, char)

def enigma_letter(char, r1, r2, r3, reflector, pos1, pos2, pos3, plugboard):
    # Plugboard IN
    c = apply_plugboard(char, plugboard)

    i = ALPHABET.index(c)

    i = shift_index(i, pos1)
    l = r1[i]
    i = shift_index(ALPHABET.index(l), -pos1)

    i = shift_index(i, pos2)
    l = r2[i]
    i = shift_index(ALPHABET.index(l), -pos2)

    i = shift_index(i, pos3)
    l = r3[i]
    i = shift_index(ALPHABET.index(l), -pos3)

    l = reflector[i]
    i = ALPHABET.index(l)

    i = shift_index(i, pos3)
    i = r3.index(ALPHABET[i])
    i = shift_index(i, -pos3)

    i = shift_index(i, pos2)
    i = r2.index(ALPHABET[i])
    i = shift_index(i, -pos2)

    i = shift_index(i, pos1)
    i = r1.index(ALPHABET[i])
    i = shift_index(i, -pos1)

    # Plugboard OUT
    return apply_plugboard(ALPHABET[i], plugboard)

def true_enigma_run(text, rotor1, rotor2, rotor3, reflector, start1=0, start2=0, start3=0, plugboard=None):
    if plugboard is None:
        plugboard = {}

    output = []
    pos1, pos2, pos3 = start1, start2, start3

    for char in text:
        if char not in ALPHABET:
            continue

        encoded = enigma_letter(char, rotor1, rotor2, rotor3, reflector, pos1, pos2, pos3, plugboard)
        output.append(encoded)

        pos1 += 1
        if pos1 == 26:
            pos1 = 0
            pos2 += 1
        if pos2 == 26:
            pos2 = 0
            pos3 += 1
        if pos3 == 26:
            pos3 = 0

    return ''.join(output)

def build_plugboard(pairs):
    plugboard = {}
    for pair in pairs:
        if len(pair) != 2:
            continue
        a, b = pair[0].upper(), pair[1].upper()
        if a in ALPHABET and b in ALPHABET:
            plugboard[a] = b
            plugboard[b] = a
    return plugboard

if __name__ == "__main__":
    print("=== Enhanced Enigma I Simulator ===")
    text = input("Enter UPPERCASE text: ").strip().upper()

    try:
        start1 = int(input("Rotor I start position (0-25): "))
        start2 = int(input("Rotor II start position (0-25): "))
        start3 = int(input("Rotor III start position (0-25): "))
    except:
        start1, start2, start3 = 0, 0, 0

    raw_pairs = input("Enter plugboard pairs (e.g., AZ BY CX): ").strip().upper().split()
    plugboard = build_plugboard(raw_pairs)

    result = true_enigma_run(
        text,
        ROTOR_I,
        ROTOR_II,
        ROTOR_III,
        REFLECTOR_B,
        start1=start1,
        start2=start2,
        start3=start3,
        plugboard=plugboard
    )
    print("Output:", result)
