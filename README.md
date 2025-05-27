# Enigma-Machine
This is a virtual Enigma Machine coded in Python, its only the first version but it is a working version nonetheless


# 🧠 Enigma Simulator with Plugboard & Custom Rotor Positions

Welcome to the **Enigma Simulator**! This program is like a digital version of the famous **WWII encryption machine** used to send secret messages. It turns your message into a secret code—and only someone with the same settings can turn it back!

---

## 💡 What Does This Program Do?

It **encrypts** (hides) your message so that only someone with the same settings can **decrypt** (unhide) it again.

You can use it to:
- Send a message to a friend
- Practice cryptography
- See how people used to hide secrets before the internet!

---

## 🛠 How It Works (In Simple Terms)

1. **Type your message** (only UPPERCASE letters, like "HELLO").
2. **Pick your rotor starting positions** (3 numbers from 0–25).
3. **Choose plugboard pairs** (letter swaps like A↔Z, B↔Y, etc.).

That's it! The program scrambles your message using:
- ROTORS: Like spinning wheels that change each letter.
- REFLECTOR: Bounces the message back.
- PLUGBOARD: Swaps certain letters before/after the machine.

When you run the program with the same settings again, it will decrypt your message!

---

## 🎮 How To Use It

1. Run the file: `enigma_simulator_with_plugboard.py`
2. Enter your message (UPPERCASE only):  
   `HELLO`
3. Enter starting rotor positions (example):  
   `Rotor I: 0`  
   `Rotor II: 0`  
   `Rotor III: 0`
4. Enter plugboard pairs (optional):  
   `AZ BY CX`  
   (This swaps A↔Z, B↔Y, C↔X)

The program will give you the **encrypted message**!

To decrypt it: just run the program again and enter the same settings.

---

## 🔁 Example

If you encrypt "HELLO" with:
- Rotor positions: `0 0 0`
- Plugboard: `AZ BY`

You might get something like:  
`GJMPX`

To get "HELLO" back, just use the same settings and input `GJMPX`.

---

## ✅ Tips

- Always remember your settings (write them down).
- Use ALL CAPS for your message.
- Plugboard is optional, but adds more security!

Have fun encrypting and decrypting like a real WWII codebreaker! 🕵️‍♂️🔐
