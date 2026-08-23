# Day 10 - The Hollow Shell
## Room: <https://tryhackme.com/room/hh-thehollowshell-ddb582ac>

Hello Hackers!

Welcome to Day 10 of the TryHackMe Hacker Holidays 2026 writeups.

The initial clues point toward shells, listening, and uploading a file to the beachfront display portal:

> `You find it on the beach: pretty, ordinary, the kind of thing nobody thinks to check. Slip something inside and hold it to your ear.`

> `The Byte Lotus beachfront lets guests personalise their in-room display by uploading a shell — a little souvenir pack of shoreline ambiance. Staff publish them through the Shoreline Display portal, and once a shell is "held to the room's ear" it plays its shore. Slip past what the portal forgets to check, and the shell answers with a shell of your own.`

The web application does not run on port 80. It is available on port `5000`.

Reviewing the source code revealed credentials:

```text
concierge:StayNoticed2024!
```

The portal allows ZIP file uploads, suggesting a possible ZIP Slip vulnerability.

We tested for path traversal using:

```bash
curl 10.48.160.100:5000/shells/../app.py --path-as-is
```

This dumped the application source code and revealed the hooks used by the upload functionality.

We then wrote `exploit.py` to create the malicious ZIP file. The ZIP Slip vulnerability allowed us to place a file in the `hooks` directory.

The hooks run automatically after the upload, as explained under the upload section of the site. This caused our uploaded shell to execute and gave us a reverse shell.

The flag was:

> `THM{...}`

Happy Hacking!
