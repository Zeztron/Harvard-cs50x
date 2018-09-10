#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <cs50.h>



int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Input should be exactly one argument!\n");
        return 1;
    }

    //open the card.raw file and check for NULL

    char* infile = argv[1];
    FILE* card_ptr = fopen(infile, "r");
    if (card_ptr == NULL)
    {
        fprintf(stderr, "File not found!");
        return 2;
    }

    // read in the 512 bytes from card.raw
    typedef uint8_t  BYTE;

    BYTE buffer[512];
    bool found_first_jpeg = false;
    FILE* new_jpeg_ptr = NULL;
    int file_counter = 0;
    while (fread(buffer, 1, 512, card_ptr) != 0x00)
    {
        // if header is found of bytes
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer [3] & 0xf0) == 0xe0)
        {
            //if the first jpeg is found
            if (!found_first_jpeg)
            {
                // change the boolean value
                found_first_jpeg = true;

                // write in the bytes into a separate file
                //1) open the file
                char filename[8];
                sprintf(filename, "%03i.jpg", file_counter++);
                new_jpeg_ptr = fopen(filename, "w");
                if (new_jpeg_ptr == NULL)
                    return 3;
                // 2) write the file into new_jpeg_ptr
                fwrite(buffer, 1, 512, new_jpeg_ptr);
            }
            else
            {
                //close the previous file
                fclose(new_jpeg_ptr);

                // write in the bytes into a separate file
                //1) open the file
                char filename[8];
                sprintf(filename, "%03i.jpg", file_counter++);
                new_jpeg_ptr = fopen(filename, "w");
                if (new_jpeg_ptr == NULL)
                    return 4;
                // 2) write the file into new_jpeg_ptr
                fwrite(buffer, 1, 512, new_jpeg_ptr);
            }
        }
        else
        {
            // if we found the first jpeg
            if (found_first_jpeg)
            {
                // continue to write the bytes
                fwrite(buffer, 1, 512, new_jpeg_ptr);
            }
        }


    }

    //close all files and free the memory used
    fclose(new_jpeg_ptr);
    fclose(card_ptr);
    return 0;

}
