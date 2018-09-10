import cs50
import sys

def main():
    # checking if command line is acceptable.
    if len(sys.argv) != 2:
        print("Missing command-line argument.")
        exit(1)

    # Insert Key
    key = int(sys.argv[1])
    print("plaintext: ", end = "")
    plaintext = cs50.get_string()


    # Print out cypher-text
    print("ciphertext: ", end = "")
    for c in plaintext:
        if (c.islower()):
            #(c + key) % 26

            print(chr((ord(c) - ord('a') + key) % 26 + ord('a')) , end = "")

        elif (c.isupper()):
            print(chr((ord(c) - ord('A') + key) % 26 + ord('A')) , end = "")

        else:
            print(c , end = "")

    print()





if __name__ == "__main__":
    main()
