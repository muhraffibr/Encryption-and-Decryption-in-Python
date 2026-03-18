# ==========================================================
# BLOCK CIPHER SEDERHANA
# Operasi: CBC XOR + Substitute (XOR Key) + Rotate
# Block size : 1 byte (8 bit)
# Format-Preserving: huruf->huruf, angka->angka, lainnya tetap
# Tanpa library eksternal
# ==========================================================


# =========================
# FUNGSI ROTATE
# =========================
def rotate_left(val):
    return ((val << 1) & 0xFF) | ((val >> 7) & 1)

def rotate_right(val):
    return ((val >> 1) & 0xFF) | ((val & 1) << 7)


# =========================
# FORMAT-PRESERVING SHIFT
# =========================
def fpe_shift(char, shift, decrypt=False):
    """
    Geser karakter dalam alfabet/angkanya sendiri.
    Huruf besar : A-Z (26), huruf kecil : a-z (26), angka : 0-9 (10).
    Karakter lain dikembalikan apa adanya.
    """
    if char.isupper():
        base, size = ord('A'), 26
    elif char.islower():
        base, size = ord('a'), 26
    elif char.isdigit():
        base, size = ord('0'), 10
    else:
        return char

    offset = shift % size
    if decrypt:
        offset = (-offset) % size

    return chr((ord(char) - base + offset) % size + base)


# =========================
# UTILITAS TAMPILAN BINER
# =========================
def to_binary_list(data):
    return ["{:08b}".format(x) for x in data]

def to_hex_string(data):
    return "".join("{:02X}".format(b) for b in data)

def from_hex_string(hex_str):
    hex_str = hex_str.strip().replace(" ", "")
    if len(hex_str) % 2 != 0:
        return None
    try:
        return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
    except ValueError:
        return None


# =========================
# VALIDASI INPUT
# =========================
def validasi_key(key):
    if not key:
        print("[ERROR] Key tidak boleh kosong!")
        return False
    return True

def validasi_plaintext(plaintext):
    if not plaintext:
        print("[ERROR] Plaintext tidak boleh kosong!")
        return False
    return True

def validasi_hex(hex_str):
    hex_str = hex_str.strip().replace(" ", "")
    if not hex_str:
        print("[ERROR] Ciphertext tidak boleh kosong!")
        return False
    if len(hex_str) % 2 != 0:
        print("[ERROR] Panjang hex harus genap!")
        return False
    for i in range(0, len(hex_str), 2):
        token = hex_str[i:i+2]
        try:
            val = int(token, 16)
            if not (0 <= val <= 255):
                print(f"[ERROR] Nilai '{token}' di luar rentang 00-FF!")
                return False
        except ValueError:
            print(f"[ERROR] '{token}' bukan hex yang valid!")
            return False
    return True


# =========================
# ENKRIPSI
# =========================
def encrypt(plaintext, key, iv):
    plaintext_bytes = [ord(c) for c in plaintext]
    key_bytes       = [ord(c) for c in key]

    ciphertext_bytes = []
    ciphertext_chars = []
    prev = iv

    print("\n{:<6} {:<8} {:<10} {:<10} {:<10} {:<10} {:<8}".format(
        "Blok", "Char", "ASCII(bin)", "CBC XOR", "Substitute", "Rotate L", "Output"))
    print("-" * 72)

    for i in range(len(plaintext_bytes)):
        block = plaintext_bytes[i]
        char  = plaintext[i]

        ascii_bin = "{:08b}".format(block)

        # CBC XOR
        block = block ^ prev
        cbc_bin = "{:08b}".format(block)

        # Substitute (XOR dengan key)
        key_val = key_bytes[i % len(key_bytes)]
        block   = block ^ key_val
        sub_bin = "{:08b}".format(block)

        # Rotate Left
        block   = rotate_left(block)
        rot_bin = "{:08b}".format(block)

        ciphertext_bytes.append(block)
        prev = block

        # Format-Preserving Shift
        out_char = fpe_shift(char, block, decrypt=False)
        ciphertext_chars.append(out_char)

        print("{:<6} {:<8} {:<10} {:<10} {:<10} {:<10} {:<8}".format(
            i + 1, repr(char), ascii_bin, cbc_bin, sub_bin, rot_bin, repr(out_char)))

    return ciphertext_bytes, "".join(ciphertext_chars)


# =========================
# DEKRIPSI
# =========================
def decrypt(ciphertext_bytes, ciphertext_chars, key, iv):
    key_bytes = [ord(c) for c in key]

    plaintext_chars = []
    prev = iv

    print("\n{:<6} {:<8} {:<10} {:<10} {:<10} {:<10} {:<8}".format(
        "Blok", "Char", "Cipher(bin)", "Rotate R", "Rev-Sub", "Rev-CBC", "Output"))
    print("-" * 72)

    for i in range(len(ciphertext_bytes)):
        block      = ciphertext_bytes[i]
        char       = ciphertext_chars[i]
        cipher_bin = "{:08b}".format(block)

        # Rotate Right
        block   = rotate_right(block)
        rot_bin = "{:08b}".format(block)

        # Reverse Substitute
        key_val = key_bytes[i % len(key_bytes)]
        block   = block ^ key_val
        sub_bin = "{:08b}".format(block)

        # Reverse CBC
        block   = block ^ prev
        cbc_bin = "{:08b}".format(block)

        prev = ciphertext_bytes[i]

        # Reverse Format-Preserving Shift (pakai cipher byte sebelum dibalik)
        shift     = ciphertext_bytes[i]
        out_char  = fpe_shift(char, shift, decrypt=True)
        plaintext_chars.append(out_char)

        print("{:<6} {:<8} {:<10} {:<10} {:<10} {:<10} {:<8}".format(
            i + 1, repr(char), cipher_bin, rot_bin, sub_bin, cbc_bin, repr(out_char)))

    return "".join(plaintext_chars)


# =========================
# MENU ENKRIPSI
# =========================
def menu_enkripsi():
    print("\n=== ENKRIPSI ===")
    plaintext = input("Masukkan plaintext : ")
    key       = input("Masukkan key       : ")

    if not validasi_plaintext(plaintext) or not validasi_key(key):
        return

    cipher_bytes, cipher_chars = encrypt(plaintext, key, IV)

    print("\nPlaintext            :", plaintext)
    print("Plaintext (biner)    :", to_binary_list([ord(c) for c in plaintext]))

    print("\nCiphertext (teks)    :", cipher_chars)
    print("Ciphertext (desimal) :", cipher_bytes)
    print("Ciphertext (biner)   :", to_binary_list(cipher_bytes))
    print("Ciphertext (hex)     :", to_hex_string(cipher_bytes))


# =========================
# MENU DEKRIPSI
# =========================
def menu_dekripsi():
    print("\n=== DEKRIPSI ===")
    cipher_chars = input("Masukkan ciphertext (teks) : ")
    hex_input    = input("Masukkan ciphertext (hex)  : ").strip()
    key          = input("Masukkan key               : ")

    if not validasi_plaintext(cipher_chars) or not validasi_hex(hex_input) or not validasi_key(key):
        return

    cipher_bytes = from_hex_string(hex_input)

    if len(cipher_bytes) != len(cipher_chars):
        print("[ERROR] Panjang ciphertext teks dan hex tidak sesuai!")
        return

    decrypted = decrypt(cipher_bytes, cipher_chars, key, IV)

    print("\nHasil dekripsi       :", decrypted)
    print("Hasil dekripsi (bin) :", to_binary_list([ord(c) for c in decrypted]))


# =========================
# PROGRAM UTAMA
# =========================
IV = 170  # 10101010 (fix)

while True:
    print("\n" + "=" * 65)
    print("       BLOCK CIPHER - CBC XOR + Substitute + Rotate")
    print("        Format-Preserving (huruf/angka/simbol)")
    print("=" * 65)
    print(f"  IV   : {IV} (biner: {IV:08b}) [fix]")
    print("=" * 65)
    print("  [1]  Enkripsi")
    print("  [2]  Dekripsi")
    print("  [0]  Keluar")
    print("=" * 65)

    pilihan = input("Pilih menu : ").strip()

    if pilihan == "1":
        menu_enkripsi()
    elif pilihan == "2":
        menu_dekripsi()
    elif pilihan == "0":
        print("\nProgram selesai.")
        break
    else:
        print("[ERROR] Pilihan tidak valid. Masukkan 1, 2, atau 0.")
