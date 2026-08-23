# Day 12 - After Hours
## Room: <https://tryhackme.com/room/hh-afterhours-b090d1f0>

Hello Hackers!

Welcome to Day 12 of the TryHackMe Hacker Holidays 2026 writeups.

This challenge involved analysing a suspicious `OBJECTS.DATA` file and identifying data hidden inside it.

We started by running `strings` against `OBJECTS.DATA` to extract readable text from the file:

```bash
strings OBJECTS.DATA
```

Among the extracted strings, we found a Base64-encoded value. Base64 is an encoding method rather than encryption, so we decoded the value to inspect what it contained.

After decoding it, we found a program that referenced something called `ConfigData`. This indicated that the next stage of the challenge was likely stored inside that configuration data.

We located `ConfigData` and decoded it from Base64 as well. The decoded output was not immediately readable because it was compressed using zlib.

We decompressed the data using zlib. Alternatively, the same result could be achieved in CyberChef by using the **From Base64** operation followed by **Raw Inflate**.

Once the data was decompressed, we analysed the resulting program using ILSpy. This allowed us to inspect the program’s structure and review the relevant code and stored values.

While analysing the program in ILSpy, we found the flag:

> `THM{...}`

Happy Hacking!
