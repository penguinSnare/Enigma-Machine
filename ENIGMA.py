#
#   System overview:
# - This is a minimal Enigma I simulator: three serial rotors, one reflector,
#   optional plugboard, and simple rotor stepping (fast→middle→slow).
# - Alphabet indices: 0..25 map to 'A'..'Z'. Rotor positions are offsets applied
#   before and after wiring lookups. Reflector wiring is involutive (self-inverse).
# - Encryption equals decryption when configuration and initial positions match.
#
#   Big picture:
# - Imagine three spinning wheels that scramble letters, a mirror that bounces
#   the signal back, and a simple cable board that swaps a few letter pairs.
#   Set the starting spots on the wheels, type a message, and you get secret text.
#
#   Key components (by function name):
# - shift_index(i, shift): modular arithmetic for ring buffer indices (mod 26).
# - apply_plugboard(char, plugboard): constant-time substitution via dict.
# - enigma_letter(...): single-character path through plugboard → rotors →
#   reflector → inverse rotors → plugboard; positions applied as cyclic offsets.
# - true_enigma_run(...): orchestrates rotor stepping and per-char encoding; O(N).
# - build_plugboard(pairs): constructs symmetric mapping from letter pairs.
#
#    What the pieces do:
# - shift_index: move around a 26-slot circle and wrap around the ends.
# - apply_plugboard: swap a letter with its partner if it has one.
# - enigma_letter: send one letter through the swaps and wheels, bounce, return.
# - true_enigma_run: do that for every letter and turn the wheels as you go.
# - build_plugboard: make the swap list from pairs like 'AB' and 'CD'.
#
#   Configuration quick notes:
# - ALPHABET: canonical symbol set 'A'..'Z'.
# - ROTOR_*: 26-char permutations (historical wirings).
# - REFLECTOR_*: 26-char involutive permutations (B reflector variant used here).
# - start1/start2/start3: initial offsets [0..25], rightmost rotor is fastest.
# - plugboard: symmetric dict {'A':'B','B':'A', ...}, optional.
# -----------------------------------------------------------------------------

# Easter Egg: RWOECHBUPEDPGTZNYRIZMVHQWZRNVKVZVIERCRIOOQRSQFYMWFIFSDMWJVGUVPYKHXECYJOVARGAEFOQSBZFUJKTVJHSXLIMJXPJQIBSQNXEJ

# Rotor I start position (0-25): 6
# Rotor II start position (0-25): 18
# Rotor III start position (0-25): 2
# Enter plugboard pairs (e.g., AZ BY CX): UI

# -----------------------------------------------------------------------------

import string  # We use this to get the alphabet A-Z easily

# ALPHABET is a string that has the letters A to Z in order.
ALPHABET = string.ascii_uppercase

# Below are the secret wheels used by a real historical machine called the Enigma.
# Each wheel (called a 'rotor') jumbles letters in a special fixed way.
# The reflector bounces the signal back through the rotors so encryption can be reversed.
ROTOR_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

def shift_index(i, shift):
    """
    Think of the alphabet as a circle from 0 to 25.
    This moves a position i around the circle by 'shift' steps, wrapping around as needed.
    """
    return (i + shift) % 26

def apply_plugboard(char, plugboard):
    """
    The plugboard is like a set of letter-swap cables on the front of the machine.
    If a letter has a swap partner, we return the partner; otherwise we keep it the same.
    """
    return plugboard.get(char, char)

def enigma_letter(char, r1, r2, r3, reflector, pos1, pos2, pos3, plugboard):
    """
    Encrypt ONE letter by passing it through:
      1) the plugboard,
      2) rotor 1, rotor 2, rotor 3 (right to left),
      3) the reflector (bounces it),
      4) then back through rotor 3, rotor 2, rotor 1 (left to right),
      5) and finally through the plugboard again.
    The pos1/pos2/pos3 numbers say how much each rotor is rotated right now.
    """
    # 1) Plugboard IN (maybe swap the letter before it enters the rotors)
    c = apply_plugboard(char, plugboard)

    # Turn the letter into a number 0..25 so it's easy to move around.
    i = ALPHABET.index(c)

    # Forward path through the rotors (right -> left)
    # Go into rotor 1 using its current position (pos1).
    i = shift_index(i, pos1)
    l = r1[i]
    i = shift_index(ALPHABET.index(l), -pos1)

    # Now rotor 2 using pos2.
    i = shift_index(i, pos2)
    l = r2[i]
    i = shift_index(ALPHABET.index(l), -pos2)

    # Now rotor 3 using pos3.
    i = shift_index(i, pos3)
    l = r3[i]
    i = shift_index(ALPHABET.index(l), -pos3)

    # Hit the reflector: it turns the signal around.
    l = reflector[i]
    i = ALPHABET.index(l)

    # Backward path through the rotors (left -> right)
    # Back through rotor 3.
    i = shift_index(i, pos3)
    i = r3.index(ALPHABET[i])
    i = shift_index(i, -pos3)

    # Back through rotor 2.
    i = shift_index(i, pos2)
    i = r2.index(ALPHABET[i])
    i = shift_index(i, -pos2)

    # Back through rotor 1.
    i = shift_index(i, pos1)
    i = r1.index(ALPHABET[i])
    i = shift_index(i, -pos1)

    # 5) Plugboard OUT (maybe swap the letter again before it leaves).
    return apply_plugboard(ALPHABET[i], plugboard)

def true_enigma_run(text, rotor1, rotor2, rotor3, reflector, start1=0, start2=0, start3=0, plugboard=None):
    """
    Encrypt a whole message, one letter at a time.
    The rotors start at positions start1/start2/start3 (like setting three dials).
    After each letter, the rotors step forward like an odometer:
      - rotor 1 moves every letter,
      - when rotor 1 wraps around, rotor 2 moves 1,
      - when rotor 2 wraps around, rotor 3 moves 1.
    """
    if plugboard is None:
        plugboard = {}

    output = []  # we'll collect the encoded letters here
    pos1, pos2, pos3 = start1, start2, start3  # current rotor positions

    for char in text:
        # We only encode letters A-Z. Anything else (like spaces) is skipped.
        if char not in ALPHABET:
            continue

        # Pass one letter through the machine.
        encoded = enigma_letter(char, rotor1, rotor2, rotor3, reflector, pos1, pos2, pos3, plugboard)
        output.append(encoded)

        # Step the rotors forward like a rolling counter (odometer).
        pos1 += 1
        if pos1 == 26:
            pos1 = 0
            pos2 += 1
        if pos2 == 26:
            pos2 = 0
            pos3 += 1
        if pos3 == 26:
            pos3 = 0

    return ''.join(output)  # join the list into a single string

def build_plugboard(pairs):
    """
    Make the plugboard mapping from pairs like ['AZ', 'BY', 'CX'].
    Each pair means: swap those two letters both ways (A<->Z, B<->Y, C<->X).
    """
    plugboard = {}
    for pair in pairs:
        # Ignore anything that isn't exactly 2 characters long.
        if len(pair) != 2:
            continue
        a, b = pair[0].upper(), pair[1].upper()
        # Only add if both are real letters.
        if a in ALPHABET and b in ALPHABET:
            plugboard[a] = b
            plugboard[b] = a
    return plugboard

if __name__ == "__main__":
    print("=== Enhanced Enigma I Simulator ===")
    # Ask the user for a message and make sure it's uppercase letters.
    text = input("Enter UPPERCASE text: ").strip().upper()

    # Ask for the starting positions (numbers 0-25).
    try:
        start1 = int(input("Rotor I start position (0-25): "))
        start2 = int(input("Rotor II start position (0-25): "))
        start3 = int(input("Rotor III start position (0-25): "))
    except:
        # If the user types something that's not a number, just use 0,0,0.
        start1, start2, start3 = 0, 0, 0

    # The plugboard pairs look like 'AZ BY CX'. Split into ['AZ','BY','CX'] and build mapping.
    raw_pairs = input("Enter plugboard pairs (e.g., AZ BY CX): ").strip().upper().split()
    plugboard = build_plugboard(raw_pairs)

    # Run the machine with our chosen rotors and reflector.
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
