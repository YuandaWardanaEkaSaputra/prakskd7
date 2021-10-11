import numpy as np
from egcd import egcd  # Jika belum ada install modul dengan pip install egcd

alphabet = "abcdefghijklmnopqrstuvwxyz"

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def matrix_mod_inv(matrix, modulus):
   #saya menemukan modulus matriks terbalik dengan
   # Langkah 1) Temukan determinan
   # Langkah 2) Temukan nilai determinan dalam modulus tertentu (biasanya panjang alfabet)
   # Langkah 3) Ambil bahwa det_inv kali matriks det*inverted (ini kemudian akan menjadi adjoint) di mod 26
     

    det = int(np.round(np.linalg.det(matrix)))  # Langkah 1)
    det_inv = egcd(det, modulus)[1] % modulus  # Langkah 2)
    matrix_modulus_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )  # Langkah 3)

    return matrix_modulus_inv


def encrypt(message, K):
    encrypted = ""
    message_in_numbers = []

    for letter in message:
        message_in_numbers.append(letter_to_index[letter])

    split_P = [
        message_in_numbers[i : i + int(K.shape[0])]
        for i in range(0, len(message_in_numbers), int(K.shape[0]))
    ]

    for P in split_P:
        P = np.transpose(np.asarray(P))[:, np.newaxis]

        while P.shape[0] != K.shape[0]:
            P = np.append(P, letter_to_index[" "])[:, np.newaxis]

        numbers = np.dot(K, P) % len(alphabet)
        n = numbers.shape[0]  # panjang dari enkripsi dalam nomor

        # Petakan kembali untuk mendapatkan teks terenkripsi
        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]

    return encrypted


def decrypt(cipher, Kinv):
    decrypted = ""
    cipher_in_numbers = []

    for letter in cipher:
        cipher_in_numbers.append(letter_to_index[letter])

    split_C = [
        cipher_in_numbers[i : i + int(Kinv.shape[0])]
        for i in range(0, len(cipher_in_numbers), int(Kinv.shape[0]))
    ]

    for C in split_C:
        C = np.transpose(np.asarray(C))[:, np.newaxis]
        numbers = np.dot(Kinv, C) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            decrypted += index_to_letter[number]

    return decrypted


def main():
    #pesan yang ingin di enkripsi dan dekripsi
    message = "yuandawardanaeka"
    
    K = np.matrix([[3, 1], [6, 5]])
    Kinv = matrix_mod_inv(K, len(alphabet))

    encrypted_message = encrypt(message, K)
    decrypted_message = decrypt(encrypted_message, Kinv)

    print("Plaintext: " + message)
    print("Hasil Enkripsi: " + encrypted_message)
    print("Hasil Dekripsi: " + decrypted_message)


main()