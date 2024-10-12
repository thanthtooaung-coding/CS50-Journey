#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int is_jpeg_header(uint8_t buffer[]);

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");

    // Create a buffer for a block of data
    uint8_t buffer[BLOCK_SIZE];
    int jpeg_count = 0;
    FILE *outptr = NULL;
    char filename[8];

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, BLOCK_SIZE, card) == 512)
    {
        // Check if it's a new JPEG
        if (is_jpeg_header(buffer))
        {
            // Close previous file if open
            if (outptr != NULL)
            {
                fclose(outptr);
            }

            // Create JPEGs from the data
            sprintf(filename, "%03i.jpg", jpeg_count);
            outptr = fopen(filename, "w");
            if (outptr == NULL)
            {
                fclose(card);
                printf("Could not create %s.\n", filename);
                return 1;
            }
            jpeg_count++;
        }

        // Write to output file if we've found a JPEG
        if (outptr != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, outptr);
        }
    }
    if (outptr != NULL)
    {
        fclose(outptr);
    }
    fclose(card);

    return 0;
}

int is_jpeg_header(uint8_t buffer[])
{
    return buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
           (buffer[3] & 0xf0) == 0xe0;
}
