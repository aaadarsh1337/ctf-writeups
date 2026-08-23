# Day 5 - The Beach Bar
## Room: <https://tryhackme.com/room/hh-thebeachbar-7d3c9e21>

Hello Hackers!

Welcome to Day 5 of the TryHackMe Hacker Holidays 2026 writeups.

This challenge starts with a staff login page. Inspecting the page source reveals a staff note containing default credentials for the demo DJ account:

> `dj:dj`

Using these credentials successfully logs us into the application.

The application includes a playlist upload feature. Since the playlist is processed as YAML using Python, we can test whether unsafe YAML deserialization is enabled.

The attached payload executes a reverse shell when it is processed. After starting a listener and uploading the malicious playlist, we receive a shell on the target machine.

The user flag is:

> `THM{...}`

Next, we inspect the running processes:

```bash
ps aux
```

One of the processes exposes a password in its command-line arguments. Reusing this password allows us to switch to the root user.

The password is:

> `SunsetSpritz2024!`

After obtaining root access, we can read the root flag:

> `THM{...}`

This room demonstrates the risks of default credentials, unsafe YAML deserialization, reverse shells, and credential reuse.

Happy Hacking!
