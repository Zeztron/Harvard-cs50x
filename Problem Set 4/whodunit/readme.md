# Questions

## What's `stdint.h`?

Header file in the C standard library that contain new definition of integer types that have speficied widths

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

To specify the width of the int types.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

1, 4, 4, 2

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

B and M

## What's the difference between `bfSize` and `biSize`?

bfSize is the entire file's size in bytes. biSize is the size of BITMAPINFOHEADER in bytes

## What does it mean if `biHeight` is negative?

Vertical orientation of the image is top down.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

WORD biBitCount;

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

There might be no output file to point to.

## Why is the third argument to `fread` always `1` in our code?

So it reads the values 1 byte at a time.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

Moves to a specific lcation in the file to seek.

## What is `SEEK_CUR`?

Seek value from the current location.

## Whodunit?

Professor Plum
