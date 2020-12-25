import os 

def decrypt(card_pubkey, door_pubkey):
    subject, loop_size, encryption_key = 7, 1, 1

    while loop_size != card_pubkey:
        loop_size = (loop_size * subject) % 20201227
        encryption_key = (encryption_key * door_pubkey) % 20201227

    return encryption_key
    

def main():
    # User input
    key_file = input("Enter file containing public keys: ")

    with open(os.path.realpath(key_file), "r") as in_keys:
        card_pubkey, door_pubkey = [int(key.strip()) for key in in_keys]

    # Part 1
    encrypt_key = decrypt(card_pubkey, door_pubkey)
    print(f"The encryption key is: {encrypt_key}")


if __name__ == "__main__":
    main()