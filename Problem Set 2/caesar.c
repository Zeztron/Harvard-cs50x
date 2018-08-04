// This program encrypts messages using Caesar's cipher.

#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Conditional statement checking to see if command-line argument is acceptable.
    if (argc != 2)
    {
        printf("Missing command-line argument...\n");
        printf("Please try again. :)\n");
        return 1;
    }

    // Insert key.
    int key = atoi(argv[1]);




    // Check to see if key is non-negative.
    if (key < 0)
    {
        printf("Key must be a positive number\n");
        return 1;
    }
    else
    {
        //Prompt user for the message to encrypt.
        string message = get_string("plaintext: ");
        //Printing out the ciphertext outsie of the for loop.
        printf("ciphertext: ");

        for (int i = 0, n = strlen(message); i < n; i++)
            {
                // Uppercase
                if (isupper(message[i]))
                {
                    printf("%c", toupper((((message[i] - 65) + key) % 26) + 65));
                }
                // Lower
                else if (islower(message[i]))
                {
                    printf("%c", tolower((((message[i] - 97) + key) % 26) + 65));
                }
                // Other
                else
                {
                    printf("%c", message[i]);
                }
            }
    }

    // Exit
    printf("\n");
    return 0;
}
