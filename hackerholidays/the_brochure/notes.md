# Day 0 - The Brochure
## Room: <https://tryhackme.com/room/hh-thebrochure-081f3e36>

Hello Hackers!
Welcome to this series of writeups for all the rooms in the TryHackMe Hacker Holidays event 2026

It is an OSINT challenge

Opening an image, it seems to be a brochure for The Byte Lotus Resort

Lets try searching for their instagram. Found

<https://www.instagram.com/thebytelotusresort/>

The "following" list reveals the account fot **veratheconcierge**

The posts have a base64 encoded string

> VEhNe1YzckBzX2FDQzB1bnRfaDRzX2IzM25fZjB1bmQhfQ==

Decoding it reveals the flag

> THM{V3r@s_aCC0unt_h4s_b33n_f0und!}

Happy Hacking!
