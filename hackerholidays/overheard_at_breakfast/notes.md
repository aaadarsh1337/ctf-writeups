# Day 6 - Overheard at Breakfast
## Room: <https://tryhackme.com/room/hh-overheardatbreakfast-6f01793c>

Hello Hackers!

Welcome to Day 6 of the TryHackMe Hacker Holidays 2026 writeups.

This is an OSINT challenge.

We are given the email address:

> `lambobytelotushotel@gmail.com`

Performing a reverse email lookup on **epoeos.com** reveals a Gravatar account.

The account starts with a **G**, confirming that it is a Gravatar profile.

Looking up the email address on Gravatar reveals an account containing a Base64-encoded string:

> `VEhNe1MzY3JlVF9QcjBmaWwzX0g0c19iMzNuX0lkZW50MWZpM2R9`

Decoding the string reveals the flag:

> `THM{...}`

Happy Hacking!
